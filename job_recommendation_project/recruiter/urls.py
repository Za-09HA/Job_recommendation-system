from django.urls import path
from . import views

urlpatterns = [
    path('', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('post-job/', views.post_job, name='post_job'),
    path('edit-job/<int:pk>/', views.edit_job, name='edit_job'),
    path('delete-job/<int:pk>/', views.delete_job, name='delete_job'),
    path('toggle-job/<int:pk>/', views.toggle_job, name='toggle_job'),
    path('applications/<int:pk>/', views.job_applications, name='job_applications'),
    path('application/<int:pk>/', views.view_application, name='view_application'),
    path('application/<int:pk>/status/<str:status>/', views.update_application_status, name='update_application_status'),
]
