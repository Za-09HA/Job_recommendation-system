from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Auth
    path('auth/register/',    views.RegisterAPIView.as_view(),  name='api_register'),
    path('auth/login/',       views.LoginAPIView.as_view(),     name='api_login'),
    path('auth/refresh/',     TokenRefreshView.as_view(),       name='api_token_refresh'),

    # Jobs
    path('jobs/',             views.JobListAPIView.as_view(),   name='api_job_list'),
    path('jobs/<int:pk>/',    views.JobDetailAPIView.as_view(), name='api_job_detail'),

    # Recommendations
    path('recommendations/',  views.recommendations_api,        name='api_recommendations'),

    # Profile
    path('profile/',          views.ProfileAPIView.as_view(),   name='api_profile'),

    # Feedback
    path('feedback/',         views.FeedbackAPIView.as_view(),  name='api_feedback'),

    # Stats
    path('stats/',            views.dashboard_stats,            name='api_stats'),
]
