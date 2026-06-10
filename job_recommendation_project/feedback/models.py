from django.db import models
from django.contrib.auth.models import User
from jobs.models import JobListing

class UserFeedback(models.Model):
    ACTION_CHOICES = [
        ('like','Liked'),('skip','Skipped'),('apply','Applied'),('save','Saved'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user','job']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} {self.action} {self.job.title}"


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    cover_letter = models.TextField()
    resume_pdf = models.FileField(upload_to='applications/resumes/')
    portfolio_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    years_of_experience = models.IntegerField(default=0)
    current_company = models.CharField(max_length=150, blank=True)
    expected_salary = models.CharField(max_length=50, blank=True)
    notice_period = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'job']
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.user.username} → {self.job.title} [{self.status}]"


class ApplicationMessage(models.Model):
    """Messages between recruiter and applicant on a specific application."""
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f"{self.sender.username} → {self.application} at {self.sent_at:%Y-%m-%d %H:%M}"
