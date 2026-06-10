from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from jobs.models import JobListing
from .models import UserFeedback, JobApplication, ApplicationMessage
from .forms import JobApplicationForm
from accounts.emails import send_application_confirmation, send_message_notification


@login_required
def apply_view(request, job_id):
    job = get_object_or_404(JobListing, pk=job_id, is_active=True)
    existing = JobApplication.objects.filter(user=request.user, job=job).first()
    if existing:
        messages.info(request, f'You already applied for {job.title}.')
        return redirect('application_detail', pk=existing.pk)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES, user=request.user, job=job)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.job = job
            if not request.FILES.get('resume_pdf'):
                profile = getattr(request.user, 'profile', None)
                if profile and profile.resume_pdf:
                    application.resume_pdf = profile.resume_pdf
                else:
                    form.add_error('resume_pdf', 'Please upload a resume PDF.')
                    return render(request, 'feedback/apply.html', {'form': form, 'job': job})
            application.save()
            UserFeedback.objects.update_or_create(
                user=request.user, job=job,
                defaults={'action': 'apply'}
            )
            try:
                send_application_confirmation(request.user, job)
            except Exception:
                pass
            messages.success(request, f'🎉 Application submitted for {job.title}!')
            return redirect('application_detail', pk=application.pk)
    else:
        form = JobApplicationForm(user=request.user, job=job)
    return render(request, 'feedback/apply.html', {'form': form, 'job': job})


@login_required
def application_detail_view(request, pk):
    application = get_object_or_404(JobApplication, pk=pk, user=request.user)
    msgs = application.messages.all()

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
            # Notify recruiter
            try:
                recruiter = application.job.posted_by
                if recruiter:
                    send_message_notification(recruiter, request.user, application.job, text)
            except Exception:
                pass
            messages.success(request, 'Message sent!')
            return redirect('application_detail', pk=pk)

    return render(request, 'feedback/application_detail.html', {
        'application': application,
        'msgs': msgs,
    })


@login_required
def my_applications_view(request):
    applications = JobApplication.objects.filter(user=request.user).select_related('job')
    return render(request, 'feedback/my_applications.html', {'applications': applications})


@login_required
@require_POST
def submit_feedback(request, job_id, action):
    job = get_object_or_404(JobListing, pk=job_id)
    if action == 'apply':
        return redirect('apply', job_id=job_id)
    UserFeedback.objects.update_or_create(
        user=request.user, job=job,
        defaults={'action': action}
    )
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok', 'action': action})
    return redirect('job_detail', pk=job_id)


@login_required
def saved_jobs_view(request):
    saved = UserFeedback.objects.filter(user=request.user, action='save').select_related('job')
    applied = JobApplication.objects.filter(user=request.user).select_related('job')
    liked = UserFeedback.objects.filter(user=request.user, action='like').select_related('job')
    return render(request, 'feedback/saved_jobs.html', {
        'saved': saved, 'applied': applied, 'liked': liked,
    })
