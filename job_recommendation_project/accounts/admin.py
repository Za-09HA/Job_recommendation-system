from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_recruiter', 'company_name', 'experience_level', 'preferred_location']
    list_filter = ['is_recruiter', 'experience_level']
    search_fields = ['user__username', 'company_name', 'skills']
