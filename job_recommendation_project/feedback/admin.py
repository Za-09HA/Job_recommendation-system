from django.contrib import admin
from .models import UserFeedback, JobApplication

@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ['user','job','action','created_at']
    list_filter = ['action','created_at']

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['user','job','full_name','email','status','applied_at']
    list_filter = ['status','applied_at']
    list_editable = ['status']
    search_fields = ['full_name','email','job__title','user__username']
    readonly_fields = ['applied_at','updated_at']
