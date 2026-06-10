from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q

from jobs.models import JobListing
from accounts.models import UserProfile
from feedback.models import UserFeedback
from recommendations.engine import get_recommendations, get_match_percentage
from .serializers import (
    JobListingSerializer, UserProfileSerializer,
    FeedbackSerializer, RegisterSerializer, UserSerializer
)


# ── Auth ─────────────────────────────────────────────────────────────────────

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Account created successfully!'
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# ── Jobs ─────────────────────────────────────────────────────────────────────

class JobListAPIView(generics.ListAPIView):
    serializer_class = JobListingSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'company', 'required_skills', 'description', 'location']
    ordering_fields = ['posted_at', 'salary_min', 'title']
    ordering = ['-posted_at']

    def get_queryset(self):
        qs = JobListing.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        job_type = self.request.query_params.get('job_type')
        experience = self.request.query_params.get('experience')
        location = self.request.query_params.get('location')
        if category:
            qs = qs.filter(category=category)
        if job_type:
            qs = qs.filter(job_type=job_type)
        if experience:
            qs = qs.filter(experience_required=experience)
        if location:
            qs = qs.filter(location__icontains=location)
        return qs

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx


class JobDetailAPIView(generics.RetrieveAPIView):
    queryset = JobListing.objects.filter(is_active=True)
    serializer_class = JobListingSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx


# ── Recommendations ───────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendations_api(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    all_jobs = JobListing.objects.filter(is_active=True)
    ranked = get_recommendations(profile, all_jobs)[:20]
    results = []
    for job, score in ranked:
        match_pct = get_match_percentage(profile, job)
        job_data = JobListingSerializer(job, context={'request': request}).data
        job_data['ai_score'] = round(score, 4)
        job_data['match_percent'] = match_pct
        results.append(job_data)
    return Response({'count': len(results), 'results': results})


# ── Profile ───────────────────────────────────────────────────────────────────

class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


# ── Feedback ──────────────────────────────────────────────────────────────────

class FeedbackAPIView(generics.ListCreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = UserFeedback.objects.filter(user=self.request.user)
        action = self.request.query_params.get('action')
        if action:
            qs = qs.filter(action=action)
        return qs

    def perform_create(self, serializer):
        job = serializer.validated_data['job']
        UserFeedback.objects.update_or_create(
            user=self.request.user, job=job,
            defaults={'action': serializer.validated_data['action']}
        )


# ── Stats ─────────────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return Response({
        'total_jobs': JobListing.objects.filter(is_active=True).count(),
        'applied': UserFeedback.objects.filter(user=request.user, action='apply').count(),
        'liked': UserFeedback.objects.filter(user=request.user, action='like').count(),
        'saved': UserFeedback.objects.filter(user=request.user, action='save').count(),
        'profile_complete': bool(profile.skills and profile.preferred_roles),
    })
