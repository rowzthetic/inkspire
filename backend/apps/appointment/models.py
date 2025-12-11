from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.price.constatnts import PLACEMENT_CHOICES
from core.models import BaseModel


class Appointment(BaseModel):
    # --- CHOICES ---
    STATUS_CHOICES = [
        ("pending", "Pending Approval"),
        ("confirmed", "Confirmed"),
        ("reschedule", "Reschedule Requested"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    SESSION_TYPE_CHOICES = [
        ("consultation", "Consultation (15-30 mins)"),
        ("tattoo", "Tattoo Session"),
        ("touchup", "Touch-up"),
    ]

    # --- 1. WHO ---
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client_appointments",
    )
    artist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="artist_appointments",
        limit_choices_to={"is_artist": True},
    )

    # --- 2. WHEN ---
    appointment_datetime = models.DateTimeField()
    estimated_duration_hours = models.PositiveIntegerField(
        default=1, help_text="Estimated session length in hours"
    )

    # --- 3. WHAT ---
    session_type = models.CharField(
        max_length=20,
        choices=SESSION_TYPE_CHOICES,
        default="tattoo",
    )
    tattoo_style = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. Traditional, Realism, Fine Line",
    )
    placement = models.CharField(
        max_length=100,
        choices=PLACEMENT_CHOICES,
    )
    size_description = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. Palm-size, Full Sleeve",
    )
    description = models.TextField(
        help_text="Detailed description of the design idea",
    )

    # --- 4. VISUALS (New) ---
    # Requires 'Pillow' library installed
    reference_image = models.ImageField(
        upload_to="references/%Y/%m/",
        blank=True,
        null=True,
        help_text="Upload a reference photo for the artist",
    )

    # --- 5. FINANCIALS (New) ---
    price_quote = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Artist's price quote for the session",
    )
    deposit_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Required deposit amount",
    )
    is_deposit_paid = models.BooleanField(default=False)

    # --- 6. ADMIN/STATUS ---
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    # Private notes for the artist (Customer never sees this)
    artist_notes = models.TextField(
        blank=True,
        help_text="Private notes for the artist (e.g. needle sizes, ink colors)",
    )

    # If rejected, why? (Visible to customer if status is cancelled)
    rejection_reason = models.TextField(
        blank=True, null=True, help_text="Reason for cancellation/rejection"
    )

    def clean(self):
        # Prevent Booking Yourself
        if self.customer == self.artist:
            raise ValidationError("You cannot book an appointment with yourself.")

        # Prevent Past Dates (Optional, depends on your business logic)
        # if self.appointment_datetime < timezone.now():
        #     raise ValidationError("Cannot book appointments in the past.")

    def __str__(self):
        return f"{self.get_session_type_display()} - {self.customer} w/ {self.artist} ({self.appointment_datetime.strftime('%Y-%m-%d %H:%M')})"


class ArtistAvailability(BaseModel):
    WEEKDAY_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    artist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="availability_rules",
        limit_choices_to={"is_artist": True},
    )

    blocked_date = models.DateField(
        null=True,
        blank=True,
        help_text="Specific date to close",
    )

    recurring_weekday = models.IntegerField(
        choices=WEEKDAY_CHOICES,
        null=True,
        blank=True,
        help_text="Block this day of the week every week",
    )

    reason = models.CharField(
        max_length=100, default="Unavailable", help_text="e.g. Shop Closed, Holiday"
    )

    def __str__(self):
        if self.blocked_date:
            return f"{self.artist} closed on {self.blocked_date}"
        return f"{self.artist} closed every {self.get_recurring_weekday_display()}"
