from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#6366f1')  # hex color
    icon = models.CharField(max_length=50, default='book')     # nombre del icono
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    @property
    def total_study_seconds(self):
        return self.sessions.filter(ended_at__isnull=False).aggregate(
            total=models.Sum('duration_seconds')
        )['total'] or 0


class StudySession(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='sessions')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.subject.name} — {self.started_at.strftime('%Y-%m-%d %H:%M')}"

    def end_session(self):
        from django.utils import timezone
        self.ended_at = timezone.now()
        delta = self.ended_at - self.started_at
        self.duration_seconds = int(delta.total_seconds())
        self.save()