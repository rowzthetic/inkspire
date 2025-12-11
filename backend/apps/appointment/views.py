from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Appointment, ArtistAvailability
from .serializers import (
    AppointmentSerializer,
    ArtistAvailabilitySerializer,
)


# 1. CREATE BOOKING
class AppointmentCreateView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


# 2. LIST APPOINTMENTS
class AppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Logic: Artists see jobs assigned to them; Customers see jobs they booked
        if getattr(user, "is_artist", False):
            return Appointment.objects.filter(
                artist=user,
            ).order_by("-appointment_datetime")

        return Appointment.objects.filter(
            customer=user,
        ).order_by("-appointment_datetime")


# 3. CANCEL APPOINTMENT
class AppointmentCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        # Find the appointment (or return 404)
        appointment = get_object_or_404(Appointment, pk=pk)

        # Security Check: Only the owner (customer) or the artist can cancel it
        if request.user != appointment.customer and request.user != appointment.artist:
            return Response(
                {"error": "You do not have permission to cancel this appointment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        appointment.status = "cancelled"
        appointment.save()

        return Response(
            {"message": "Appointment cancelled successfully."},
            status=status.HTTP_200_OK,
        )


# 4. CHECK AVAILIBILTY
class CheckAvailabilityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        artist_id = request.query_params.get("artist_id")
        date_str = request.query_params.get("date")  # YYYY-MM-DD

        if not artist_id or not date_str:
            return Response({"error": "Missing artist_id or date"}, status=400)

        check_date = parse_date(date_str)
        if not check_date:
            return Response({"error": "Invalid date"}, status=400)

        specific_block = ArtistAvailability.objects.filter(
            artist_id=artist_id,
            blocked_date=check_date,
        ).first()

        if specific_block:
            return Response(
                {
                    "is_available": False,
                    "reason": specific_block.reason,
                },
                status=200,
            )

        recurring_block = ArtistAvailability.objects.filter(
            artist_id=artist_id,
            recurring_weekday=check_date.weekday(),
        ).first()

        if recurring_block:
            return Response(
                {
                    "is_available": False,
                    "reason": recurring_block.reason,
                },
                status=200,
            )

        appointments = Appointment.objects.filter(
            artist_id=artist_id,
            appointment_datetime__date=check_date,
        ).exclude(status="cancelled")

        busy_slots = []
        for appt in appointments:
            start_time = appt.appointment_datetime
            end_time = start_time + timedelta(hours=appt.estimated_duration_hours)
            busy_slots.append(
                {
                    "start": start_time.strftime("%H:%M"),
                    "end": end_time.strftime("%H:%M"),
                }
            )

        return Response(
            {
                "is_available": True,
                "busy_slots": busy_slots,
            },
            status=200,
        )


# 5. Managing artist availibilty
class ManageAvailabilityView(generics.ListCreateAPIView):
    serializer_class = ArtistAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show the artist their own rules
        return ArtistAvailability.objects.filter(artist=self.request.user)


class DeleteAvailabilityView(generics.DestroyAPIView):
    serializer_class = ArtistAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ArtistAvailability.objects.filter(artist=self.request.user)
