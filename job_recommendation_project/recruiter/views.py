from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from jobs.models import JobListing
from feedback.models import JobApplication, ApplicationMessage
from accounts.emails import send_application_status_email, send_hiring_greeting_email
from .forms import JobPostForm


def recruiter_required(view_func):
    """Decorator: user must be logged in and be a recruiter."""
    @login_required
    def wrapper(request, *args, **kwargs):
        profile = getattr(request.user, 'profile', None)
        if not profile or not profile.is_recruiter:
            messages.error(request, 'This page is for recruiters only.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


@recruiter_required
def recruiter_dashboard(request):
    jobs = JobListing.objects.filter(posted_by=request.user).order_by('-posted_at')
    total_jobs = jobs.count()
    active_jobs = jobs.filter(is_active=True).count()
    total_applications = JobApplication.objects.filter(job__posted_by=request.user).count()
    pending_applications = JobApplication.objects.filter(
        job__posted_by=request.user, status='submitted'
    ).count()
    recent_applications = JobApplication.objects.filter(
        job__posted_by=request.user
    ).select_related('user', 'job').order_by('-applied_at')[:5]

    return render(request, 'recruiter/dashboard.html', {
        'jobs': jobs,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'recent_applications': recent_applications,
    })


@recruiter_required
def post_job(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            if not job.company and profile.company_name:
                job.company = profile.company_name
            job.save()
            messages.success(request, f'Job "{job.title}" posted successfully!')
            return redirect('recruiter_dashboard')
    else:
        form = JobPostForm(initial={'company': profile.company_name})
    return render(request, 'recruiter/post_job.html', {'form': form})


@recruiter_required
def edit_job(request, pk):
    job = get_object_or_404(JobListing, pk=pk, posted_by=request.user)
    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f'Job updated successfully!')
            return redirect('recruiter_dashboard')
    else:
        form = JobPostForm(instance=job)
    return render(request, 'recruiter/post_job.html', {'form': form, 'job': job})


@recruiter_required
def delete_job(request, pk):
    job = get_object_or_404(JobListing, pk=pk, posted_by=request.user)
    job.delete()
    messages.success(request, f'Job "{job.title}" deleted.')
    return redirect('recruiter_dashboard')


@recruiter_required
def toggle_job(request, pk):
    job = get_object_or_404(JobListing, pk=pk, posted_by=request.user)
    job.is_active = not job.is_active
    job.save()
    status = 'activated' if job.is_active else 'deactivated'
    messages.success(request, f'Job "{job.title}" {status}.')
    return redirect('recruiter_dashboard')


@recruiter_required
def job_applications(request, pk):
    job = get_object_or_404(JobListing, pk=pk, posted_by=request.user)
    applications = JobApplication.objects.filter(job=job).select_related('user').order_by('-applied_at')
    return render(request, 'recruiter/job_applications.html', {
        'job': job,
        'applications': applications,
    })


@recruiter_required
def update_application_status(request, pk, status):
    application = get_object_or_404(JobApplication, pk=pk, job__posted_by=request.user)
    valid_statuses = ['submitted', 'under_review', 'shortlisted', 'rejected', 'hired']
    if status not in valid_statuses:
        messages.error(request, 'Invalid status.')
        return redirect('job_applications', pk=application.job.pk)

    old_status = application.status
    application.status = status
    application.save()

    # Send email notification to applicant
    if old_status != status:
        try:
            if status == 'hired':
                # Send professional greeting/interview invitation email
                recruiter_profile = request.user.profile
                send_hiring_greeting_email(application.user, application.job, recruiter_profile)
                # Also send the standard status update email
                send_application_status_email(application.user, application.job, status)
            elif status in ['shortlisted', 'rejected']:
                send_application_status_email(application.user, application.job, status)
        except Exception as e:
            print(f"Email error: {e}")

    messages.success(request, f'Application status updated to {status.replace("_", " ").title()}.')
    return redirect('job_applications', pk=application.job.pk)


@recruiter_required
def view_application(request, pk):
    application = get_object_or_404(JobApplication, pk=pk, job__posted_by=request.user)
    # Mark messages as read
    application.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    if request.method == 'POST':
        text = request.POST.get('message', '').strip()
        if text:
            ApplicationMessage.objects.create(
                application=application,
                sender=request.user,
                message=text
            )
            # Notify applicant
            try:
                from accounts.emails import send_message_notification
                send_message_notification(application.user, request.user, application.job, text)
            except Exception:
                pass
            messages.success(request, 'Message sent to applicant!')
            return redirect('view_application', pk=pk)

    return render(request, 'recruiter/view_application.html', {'application': application})
