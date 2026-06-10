from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/',          views.apply_view,              name='apply'),
    path('application/<int:pk>/',        views.application_detail_view, name='application_detail'),
    path('my-applications/',             views.my_applications_view,    name='my_applications'),
    path('submit/<int:job_id>/<str:action>/', views.submit_feedback,    name='submit_feedback'),
    path('saved/',                       views.saved_jobs_view,         name='saved_jobs'),
]
