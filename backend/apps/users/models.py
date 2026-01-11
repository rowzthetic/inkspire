from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Existing fields
    is_artist = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )

    # Artist specific fields
    bio = models.TextField(blank=True)
    styles = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    shop_name = models.CharField(max_length=100, blank=True)
    instagram_link = models.URLField(blank=True, null=True)

    # ✅ OTP Fields (These are correct here)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username


class PortfolioImage(models.Model):
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name="portfolio")
    image = models.ImageField(upload_to="portfolio/")
    created_at = models.DateTimeField(auto_now_add=True)


class WorkSchedule(models.Model):
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    day_of_week = models.IntegerField()  # 0=Monday, 6=Sunday
    is_active = models.BooleanField(default=True)
    start_time = models.TimeField(default="09:00")
    end_time = models.TimeField(default="17:00")
