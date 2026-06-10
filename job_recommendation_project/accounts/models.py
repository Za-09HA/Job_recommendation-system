from django.db import models
from django.contrib.auth.models import User

EXPERIENCE_CHOICES = [
    ('fresher','Fresher (0 years)'),('junior','Junior (1-2 years)'),
    ('mid','Mid-level (3-5 years)'),('senior','Senior (5+ years)'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_recruiter = models.BooleanField(default=False)
    company_name = models.CharField(max_length=200, blank=True)
    company_description = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills")
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='fresher')
    experience_years = models.IntegerField(default=0)
    preferred_roles = models.TextField(blank=True)
    preferred_location = models.CharField(max_length=100, blank=True)
    resume_pdf = models.FileField(upload_to='resumes/', blank=True, null=True)
    resume_text = models.TextField(blank=True, editable=False)  # auto-extracted from PDF
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    def get_preferred_roles_list(self):
        return [r.strip() for r in self.preferred_roles.split(',') if r.strip()]

    def extract_resume_text(self):
        """Extract text from uploaded PDF resume."""
        if not self.resume_pdf:
            return ''
        try:
            import pdfplumber, os
            path = self.resume_pdf.path
            text_parts = []
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text_parts.append(t)
            return ' '.join(text_parts)[:2000]
        except Exception as e:
            print(f"[PDF Extract] Error: {e}")
            return ''

    def __str__(self):
        return f"{self.user.username}'s Profile"
