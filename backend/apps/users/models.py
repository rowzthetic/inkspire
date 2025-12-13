from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import BaseModel

class User(AbstractUser, BaseModel):
    # --- BASIC LOGIN ---
    email = models.EmailField(unique=True)
    is_artist = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # --- ARTIST PROFILE DETAILS ---
    # 1. Visuals
    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
        help_text="Artist's avatar or logo",
    )

    # 2. Professional Info
    bio = models.TextField(
        blank=True, null=True, help_text="Short description about yourself"
    )
    years_of_experience = models.PositiveIntegerField(
        null=True, blank=True, help_text="How long have you been tattooing?",
    )

    # 3. Work Details
    shop_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    instagram_link = models.URLField(
        blank=True, null=True, help_text="Link to portfolio"
    )

    # 4. Money
    hourly_rate = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Standard hourly charge",
    )
    minimum_charge = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Minimum price for a tattoo",
    )

    # 5. Styles (Simple text list for now)
    styles = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Comma-separated styles (e.g. Realism, Traditional, Dotwork)",
    )

    # --- DJANGO CONFIG ---
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        if self.is_artist and self.shop_name:
            return f"{self.username} ({self.shop_name})"
        return self.email
