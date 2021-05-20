from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "entries"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        ordering = ['-created_at']
        constraints = [
            UniqueConstraint(fields=['user', 'entry'], name='unique_like')
        ]


class ForbiddenWord(models.Model):
    word = models.CharField(max_length=64, unique=True)
