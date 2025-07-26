#/website/models.py

from django.db import models
from django.contrib.auth.models import User

# Model representing a note category
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Model representing a single note (record)
class Record(models.Model):
    # Status color choices
    STATUS_COLOR_CHOICES = [
        ('white', 'No status'),
        ('yellow', 'To do'),
        ('red', 'Urgent'),
        ('green', 'Completed'),
        ('blue', 'In progress'),
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, default="New note")
    content = models.TextField(default="No content")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    status_color = models.CharField(max_length=20, choices=STATUS_COLOR_CHOICES, default='white')
    is_priority = models.BooleanField(default=False)
    reminder = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


