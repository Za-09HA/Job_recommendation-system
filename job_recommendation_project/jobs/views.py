from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import JobListing, CATEGORY_CHOICES, JOB_TYPE_CHOICES
from recommendations.engine import get_recommendations
from accounts.models import UserProfile
from feedback.models import UserFeedback, JobApplication

def home_view(request):
    featured_jobs = JobListing.objects.filter(is_active=True)[:6]
    total_jobs = JobListing.objects.filter(is_active=True).count()
    categories = CATEGORY_CHOICES
    return render(request, 'jobs/home.html', {
        'featured_jobs': featured_jobs,
        'total_jobs': total_jobs,
        'categories': categories,
    })

def job_list_view(request):
    jobs = JobListing.objects.filter(is_active=True)
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    job_type = request.GET.get('job_type', '')
    location = request.GET.get('location', '')
    experience = request.GET.get('experience', '')

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) | Q(company__icontains=query) |
            Q(required_skills__icontains=query) | Q(description__icontains=query)
        )
    if category:
        jobs = jobs.filter(category=category)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if experience:
        jobs = jobs.filter(experience_required=experience)

    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'categories': CATEGORY_CHOICES,
        'job_types': JOB_TYPE_CHOICES,
        'filters': {'q': query, 'category': category, 'job_type': job_type,
                    'location': location, 'experience': experience},
    })

def job_detail_view(request, pk):
    job = get_object_or_404(JobListing, pk=pk, is_active=True)
    user_feedback = None
    similar_jobs = JobListing.objects.filter(
        category=job.category, is_active=True
    ).exclude(pk=pk)[:4]
    if request.user.is_authenticated:
        user_feedback = UserFeedback.objects.filter(
            user=request.user, job=job
        ).first()
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'similar_jobs': similar_jobs,
        'user_feedback': user_feedback,
    })

@login_required
def dashboard_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    all_jobs = JobListing.objects.filter(is_active=True)
    recommendations = []
    if profile.skills or profile.preferred_roles:
        recommendations = get_recommendations(profile, all_jobs)[:8]
    applied_count = UserFeedback.objects.filter(user=request.user, action='apply').count()
    liked_count = UserFeedback.objects.filter(user=request.user, action='like').count()
    recent_jobs = all_jobs[:5]
    # Get recent applications with status
    recent_applications = JobApplication.objects.filter(
        user=request.user
    ).select_related('job').order_by('-updated_at')[:5]
    # Unread messages count
    from feedback.models import ApplicationMessage
    unread_count = ApplicationMessage.objects.filter(
        application__user=request.user,
        is_read=False
    ).exclude(sender=request.user).count()
    return render(request, 'jobs/dashboard.html', {
        'profile': profile,
        'recommendations': recommendations,
        'applied_count': applied_count,
        'liked_count': liked_count,
        'recent_jobs': recent_jobs,
        'total_jobs': all_jobs.count(),
        'recent_applications': recent_applications,
        'unread_count': unread_count,
    })

def api_docs_view(request):
    return render(request, 'api_docs.html')
