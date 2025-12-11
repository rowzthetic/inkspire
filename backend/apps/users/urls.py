from django.urls import path
from .views import (
    ActivateAccountView, 
    ArtistDetailView,
    ArtistListView,
    LoginView,
    LogoutView,
    RegisterView,
    UserView,
)

urlpatterns = [
    # --- Authentication ---
    path("register/", RegisterView.as_view(), name="register"),
    
    # This captures the unique ID and Token from the email link
    path("activate/<uidb64>/<token>/", ActivateAccountView.as_view(), name="activate"),
    
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/", UserView.as_view(), name="current-user"),
    
    # --- Marketplace ---
    # Search artists: /api/auth/artists/?search=...
    path("artists/", ArtistListView.as_view(), name="artist-list"),
    
    # Get specific artist profile: /api/auth/artists/{uuid}/
    path("artists/<uuid:pk>/", ArtistDetailView.as_view(), name="artist-detail"),
]