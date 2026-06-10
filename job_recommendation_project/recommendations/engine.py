"""
NexaJobs ML Recommendation Engine
===================================
Combines three techniques:
  1. Content-Based Filtering  - TF-IDF + Cosine Similarity on profile vs job text
  2. Collaborative Filtering  - "Users like you also liked" using feedback data
  3. Skill-Match Boosting     - Exact keyword overlap bonus + experience/location fit
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import numpy as np


def build_user_text(profile):
    parts = []
    if profile.skills:
        parts.append((profile.skills + ' ') * 3)
    if profile.preferred_roles:
        parts.append((profile.preferred_roles + ' ') * 2)
    if profile.resume_text:
        parts.append(profile.resume_text[:800])
    if profile.experience_level:
        parts.append(profile.experience_level.replace('_', ' '))
    if profile.preferred_location:
        parts.append(profile.preferred_location)
    return ' '.join(parts)


def build_job_text(job):
    parts = [
        str(job.title) * 3,
        str(job.required_skills) * 2,
        str(job.description)[:500],
        job.category.replace('_', ' '),
        job.job_type.replace('_', ' '),
        job.experience_required.replace('_', ' '),
        job.location, job.company,
    ]
    return ' '.join(parts)


def content_based_scores(user_profile, jobs):
    user_text = build_user_text(user_profile)
    if not user_text.strip():
        return {job.id: 0.5 for job in jobs}
    job_texts = [build_job_text(j) for j in jobs]
    corpus = [user_text] + job_texts
    try:
        vec = TfidfVectorizer(stop_words='english', ngram_range=(1, 2),
                              max_features=8000, sublinear_tf=True)
        matrix = vec.fit_transform(corpus)
        scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()
        return {job.id: float(scores[i]) for i, job in enumerate(jobs)}
    except Exception:
        return {job.id: 0.5 for job in jobs}


def skill_boost(user_profile, job):
    user_skills = {s.lower().strip() for s in user_profile.get_skills_list()}
    job_skills  = {s.lower().strip() for s in job.get_skills_list()}
    if not job_skills or not user_skills:
        return 0.0
    overlap = user_skills & job_skills
    return round(len(overlap) / len(job_skills) * 0.30, 4)


def context_boost(user_profile, job):
    boost = 0.0
    exp_map = {'fresher': 0, 'junior': 1, '1_2': 1, 'mid': 2, '3_5': 2, 'senior': 3, '5_plus': 3}
    u_exp = exp_map.get(user_profile.experience_level, 0)
    j_exp = exp_map.get(job.experience_required, 0)
    if u_exp >= j_exp:
        boost += 0.08
    if user_profile.preferred_location:
        if user_profile.preferred_location.lower() in job.location.lower():
            boost += 0.07
        if 'remote' in job.location.lower():
            boost += 0.04
    return boost


def collaborative_scores(user, jobs):
    try:
        from feedback.models import UserFeedback
        ACTION_WEIGHT = {'like': 1.0, 'save': 0.8, 'apply': 1.2, 'skip': -0.3}

        user_positive = set(UserFeedback.objects.filter(
            user=user, action__in=['like', 'apply', 'save']
        ).values_list('job_id', flat=True))
        if not user_positive:
            return {}

        related = UserFeedback.objects.filter(
            job_id__in=user_positive
        ).exclude(user=user).select_related('user')

        similar_users = defaultdict(dict)
        for fb in related:
            similar_users[fb.user_id][fb.job_id] = ACTION_WEIGHT.get(fb.action, 0)

        if not similar_users:
            return {}

        user_sim = {
            uid: len(set(js.keys()) & user_positive) / max(len(user_positive), 1)
            for uid, js in similar_users.items()
        }

        seen = set(UserFeedback.objects.filter(user=user).values_list('job_id', flat=True))
        unseen = {j.id for j in jobs} - seen

        scores = defaultdict(float)
        for fb in UserFeedback.objects.filter(user_id__in=user_sim.keys(), job_id__in=unseen):
            scores[fb.job_id] += ACTION_WEIGHT.get(fb.action, 0) * user_sim.get(fb.user_id, 0)

        if not scores:
            return {}
        max_s = max(scores.values()) or 1
        return {jid: s / max_s for jid, s in scores.items()}
    except Exception:
        return {}


def get_recommendations(user_profile, job_queryset):
    """Returns list of (JobListing, score_percent:int) sorted best-first."""
    jobs = list(job_queryset)
    if not jobs:
        return []

    cb_scores = content_based_scores(user_profile, jobs)
    cf_scores = {}
    if hasattr(user_profile, 'user') and user_profile.user_id:
        cf_scores = collaborative_scores(user_profile.user, jobs)

    final = {}
    for job in jobs:
        cb  = cb_scores.get(job.id, 0.0)
        cf  = cf_scores.get(job.id, 0.0)
        skb = skill_boost(user_profile, job)
        ctx = context_boost(user_profile, job)
        cf_weight = 0.20 if cf > 0 else 0.0
        cb_weight = 1.0 - cf_weight
        final[job.id] = min(1.0, (cb * cb_weight) + (cf * cf_weight) + skb + ctx)

    ranked = sorted(jobs, key=lambda j: final.get(j.id, 0), reverse=True)
    return [(job, int(final.get(job.id, 0) * 100)) for job in ranked]


def get_match_percentage(user_profile, job):
    user_skills = {s.lower().strip() for s in user_profile.get_skills_list()}
    job_skills  = {s.lower().strip() for s in job.get_skills_list()}
    if not job_skills:
        return 50
    return int(len(user_skills & job_skills) / len(job_skills) * 100)
