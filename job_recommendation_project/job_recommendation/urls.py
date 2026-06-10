from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobs.urls')),
    path('accounts/', include('accounts.urls')),
    path('recommendations/', include('recommendations.urls')),
    path('feedback/', include('feedback.urls')),
    path('api/v1/', include('api.urls')),
    path('recruiter/', include('recruiter.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
