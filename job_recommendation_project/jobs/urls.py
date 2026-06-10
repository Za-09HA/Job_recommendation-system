from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('jobs/', views.job_list_view, name='job_list'),
    path('jobs/<int:pk>/', views.job_detail_view, name='job_detail'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('api-docs/', views.api_docs_view, name='api_docs'),
]
