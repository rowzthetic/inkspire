# from django.urls import path
# from .views import ArtistDashboardView, UpdateScheduleView, ManagePortfolioView
# from .views import (
#     ActivateAccountView,
#     ArtistDetailView,
#     ArtistListView,
#     LoginView,
#     LogoutView,
#     RegisterView,
#     UserView,
# )

# urlpatterns = [
#     # --- Authentication ---
#     path("register/", RegisterView.as_view(), name="register"),
#     # This captures the unique ID and Token from the email link
#     path("activate/<uuid:token>/", ActivateAccountView.as_view(), name="activate"),
#     path("login/", LoginView.as_view(), name="login"),
#     path("logout/", LogoutView.as_view(), name="logout"),
#     path("user/", UserView.as_view(), name="current-user"),
#     # --- Marketplace ---
#     # Search artists: /api/auth/artists/?search=...
#     path("artists/", ArtistListView.as_view(), name="artist-list"),
#     # Get specific artist profile: /api/auth/artists/{uuid}/
#     path("artists/<uuid:pk>/", ArtistDetailView.as_view(), name="artist-detail"),
# ]


# # added


# urlpatterns = [
#     # ... existing ...
#     path('dashboard/', ArtistDashboardView.as_view(), name='artist-dashboard'),
#     path('dashboard/schedule/', UpdateScheduleView.as_view(), name='update-schedule'),
#     path('dashboard/portfolio/', ManagePortfolioView.as_view(), name='add-portfolio'),
#     path('dashboard/portfolio/<int:pk>/', ManagePortfolioView.as_view(), name='delete-portfolio'),
# ]


from django.urls import path

from .views import (
    # Dashboard Views
    ArtistDashboardView,
    ArtistDetailView,
    # Marketplace Views
    ArtistListView,
    LoginWithOTPView,
    LogoutView,
    ManagePortfolioView,
    # Auth Views (New OTP System)
    RegisterView,
    UpdateScheduleView,
    UserView,
    VerifyOTPView,
)

urlpatterns = [
    # --- Authentication (OTP System) ---
    path("register/", RegisterView.as_view(), name="register"),
    path("auth/send-otp/", LoginWithOTPView.as_view(), name="send-otp"),  # For Login
    path("auth/verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),  # For Verify
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/", UserView.as_view(), name="current-user"),
    # --- Marketplace (Public) ---
    # Search artists: /api/auth/artists/?search=...
    path("artists/", ArtistListView.as_view(), name="artist-list"),
    # Get specific artist profile: /api/auth/artists/{id}/
    path("artists/<int:pk>/", ArtistDetailView.as_view(), name="artist-detail"),
    # --- Artist Dashboard (Private) ---
    path("dashboard/", ArtistDashboardView.as_view(), name="artist-dashboard"),
    path("dashboard/schedule/", UpdateScheduleView.as_view(), name="update-schedule"),
    path("dashboard/portfolio/", ManagePortfolioView.as_view(), name="add-portfolio"),
    path(
        "dashboard/portfolio/<int:pk>/",
        ManagePortfolioView.as_view(),
        name="delete-portfolio",
    ),
]
