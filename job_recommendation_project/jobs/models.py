from django.contrib.auth.models import User
from django.db import models

JOB_TYPE_CHOICES = [
    ('full_time','Full Time'),('part_time','Part Time'),
    ('contract','Contract'),('internship','Internship'),('remote','Remote'),
]

EXPERIENCE_REQUIRED = [
    ('fresher','Fresher'),('1_2','1-2 Years'),('3_5','3-5 Years'),('5_plus','5+ Years'),
]

CATEGORY_CHOICES = [
    ('software','Software Engineering'),('data','Data Science & ML'),
    ('design','Design & UX'),('product','Product Management'),
    ('devops','DevOps & Cloud'),('mobile','Mobile Development'),
    ('backend','Backend Development'),('frontend','Frontend Development'),
    ('fullstack','Full Stack Development'),('cybersecurity','Cybersecurity'),
    ('other','Other'),
]

class JobListing(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    company_logo = models.URLField(blank=True, default='')
    description = models.TextField()
    required_skills = models.TextField(help_text="Comma-separated skills")
    location = models.CharField(max_length=150)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='software')
    experience_required = models.CharField(max_length=10, choices=EXPERIENCE_REQUIRED, default='fresher')
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    source_url = models.URLField(blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='posted_jobs')
    is_active = models.BooleanField(default=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_skills_list(self):
        return [s.strip() for s in self.required_skills.split(',') if s.strip()]

    def salary_display(self):
        if self.salary_min and self.salary_max:
            return f"${self.salary_min:,} - ${self.salary_max:,}"
        elif self.salary_min:
            return f"From ${self.salary_min:,}"
        return "Competitive"

    def __str__(self):
        return f"{self.title} at {self.company}"

    class Meta:
        ordering = ['-posted_at']
