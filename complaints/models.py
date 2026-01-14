from django.db import models
from django.contrib.auth.models import User

class Complaint(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
        ("Rejected", "Rejected"),
    ]

    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Critical", "Critical"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    description = models.TextField()
    reply = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

        # New psychological fields
    stress_score = models.FloatField(default=0.0)
    emotion_label = models.CharField(max_length=50, blank=True)
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="Low"
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return f"{self.user.username} Profile"