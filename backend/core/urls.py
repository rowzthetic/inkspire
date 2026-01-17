# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib import admin
# from django.urls import include, path
# from rest_framework_simplejwt.views import TokenRefreshView

# # ✅ FIXED IMPORT: Now pointing to 'views.py', not 'serializers.py'
# from apps.users.views import CustomTokenObtainPairView

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     # --- Authentication & Users ---
#     path("api/auth/", include("apps.users.urls")),
#     # --- Feature Apps ---
#     path("api/appointment/", include("apps.appointment.urls")),
#     path("api/price/", include("apps.price.urls")),
#     path("api/library/", include("library.urls")),
#     # --- JWT Token Endpoints ---
#     path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
#     path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),


# ]


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

# ✅ FIXED IMPORTS: Added Dashboard Views here
from apps.users.views import (
    ArtistDashboardView,
    CustomTokenObtainPairView,
    ManagePortfolioView,
    UpdateScheduleView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # --- Authentication & Users ---
    # This includes your login/register/verify-otp
    path("api/auth/", include("apps.users.urls")),
    # --- 👇 NEW DASHBOARD ENDPOINTS (Required for Artist Dashboard) ---
    path("api/auth/dashboard/", ArtistDashboardView.as_view(), name="artist-dashboard"),
    path(
        "api/auth/dashboard/schedule/",
        UpdateScheduleView.as_view(),
        name="update-schedule",
    ),
    path(
        "api/auth/dashboard/portfolio/",
        ManagePortfolioView.as_view(),
        name="manage-portfolio",
    ),
    path(
        "api/auth/dashboard/portfolio/<int:pk>/",
        ManagePortfolioView.as_view(),
        name="delete-portfolio",
    ),
    # --- Feature Apps ---
    path("api/appointment/", include("apps.appointment.urls")),
    path("api/price/", include("apps.price.urls")),
    path("api/library/", include("library.urls")),
    # --- JWT Token Endpoints ---
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
