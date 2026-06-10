from django.db import models
from django.contrib.auth.models import User
from jobs.models import JobListing

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']
        unique_together = ['user','job']

    def score_percent(self):
        return int(self.score * 100)

    def __str__(self):
        return f"{self.user.username} → {self.job.title} ({self.score:.2f})"
