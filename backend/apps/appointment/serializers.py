from rest_framework import serializers

from apps.appointment.models import Appointment, ArtistAvailability


class AppointmentSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source="artist.username", read_only=True)
    customer_name = serializers.CharField(source="customer.username", read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "customer_name",
            "artist",
            "artist_name",
            "appointment_datetime",
            "estimated_duration_hours",
            "session_type",
            "tattoo_style",
            "placement",
            "size_description",
            "description",
            "status",
            "created_at",
            # --- NEW FIELDS ---
            "reference_image",  # Handles Image Uploads
            "price_quote",
            "deposit_amount",
            "is_deposit_paid",
            "rejection_reason",
            # 'artist_notes' is intentionally left out or should be strictly handled
            # so customers don't see private artist notes.
            # If you want the artist to see them in this list, add 'artist_notes' here.
        ]

        # IMPORTANT: These fields are Read-Only for the person booking.
        # A customer cannot decide their own price or approve their own booking.
        read_only_fields = [
            "status",
            "created_at",
            "customer_name",
            "price_quote",
            "deposit_amount",
            "is_deposit_paid",
            "rejection_reason",
        ]

    def create(self, validated_data):
        # Automatically attach the logged-in user as the customer
        user = self.context["request"].user
        return Appointment.objects.create(customer=user, **validated_data)


class ArtistAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistAvailability
        fields = ["id", "blocked_date", "recurring_weekday", "reason"]

    def create(self, validated_data):
        user = self.context["request"].user
        return ArtistAvailability.objects.create(artist=user, **validated_data)
