from django.contrib import admin
from .models import JobListing

@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'job_type', 'experience_required', 'is_active', 'posted_at']
    list_filter = ['is_active', 'job_type', 'category', 'experience_required']
    search_fields = ['title', 'company', 'location', 'required_skills']
    list_editable = ['is_active']
