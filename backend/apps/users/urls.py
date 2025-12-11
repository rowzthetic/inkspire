from django.urls import path

from .views import (
    ArtistDetailView,  # <--- New import
    ArtistListView,
    LoginView,
    LogoutView,
    RegisterView,
    UserView,
)

urlpatterns = [
    # Auth
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/", UserView.as_view(), name="current-user"),
    # Marketplace
    path("artists/", ArtistListView.as_view(), name="artist-list"),
    path("artists/<uuid:pk>/", ArtistDetailView.as_view(), name="artist-detail"),
]
