from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from jobs.models import JobListing
from accounts.models import UserProfile
from .engine import get_recommendations, get_match_percentage

@login_required
def recommendations_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    all_jobs = JobListing.objects.filter(is_active=True)
    ranked = get_recommendations(profile, all_jobs)
    results = []
    for job, score in ranked[:20]:
        match_pct = get_match_percentage(profile, job)
        results.append({'job': job, 'score': score, 'match_pct': match_pct})
    return render(request, 'recommendations/recommendations.html', {
        'results': results,
        'profile': profile,
    })
