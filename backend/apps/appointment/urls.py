from django.urls import path

from .views import (
    AppointmentCancelView,
    AppointmentCreateView,
    AppointmentListView,
    CheckAvailabilityView,
    DeleteAvailabilityView,
    ManageAvailabilityView,
)

urlpatterns = [
    # POST to book
    path(
        "book/",
        AppointmentCreateView.as_view(),
        name="book-appointment",
    ),
    # GET to see your history
    path(
        "list/",
        AppointmentListView.as_view(),
        name="list-appointments",
    ),
    # PATCH to cancel
    # /api/appointment/booking/cancel/550e8400-e29b.../
    path(
        "cancel/<uuid:pk>/",
        AppointmentCancelView.as_view(),
        name="cancel-appointment",
    ),
    #  GET to check availabilty for the artist
    # /api/appointment/availability/?artist=550e8400-e29b..?date=2020-01-01
    path(
        "availability/",
        CheckAvailabilityView.as_view(),
        name="check-availability",
    ),
    path(
        "availability/manage/",
        ManageAvailabilityView.as_view(),
        name="manage-availability",
    ),
    path(
        "availability/delete/<uuid:pk>/",
        DeleteAvailabilityView.as_view(),
        name="delete-availability",
    ),
]
