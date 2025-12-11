from django.contrib.auth import get_user_model, login, logout
from rest_framework import filters, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

# Import serializers
from apps.users.serializers import (
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)

User = get_user_model()


# --- AUTHENTICATION VIEWS ---
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(
            data=request.data,
            context={
                "request": request,
            },
        )
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            # Creates the session cookie
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(
            {
                "message": "Successfully logged out",
            },
            status=status.HTTP_200_OK,
        )


class UserView(APIView):
    """
    Get the currently logged-in user's profile.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# --- ARTIST MARKETPLACE VIEWS ---
class ArtistListView(generics.ListAPIView):
    """
    Returns a list of all artists.
    Supports search functionality for a Marketplace.
    Example: /api/auth/artists/?search=Realism
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can browse artists
    queryset = User.objects.filter(is_artist=True)

    # Enable Search
    filter_backends = [filters.SearchFilter]
    # Fields users can search by:
    search_fields = [
        "username",
        "bio",
        "styles",
        "city",
        "shop_name",
    ]


class ArtistDetailView(generics.RetrieveAPIView):
    """
    Get a SINGLE artist's full profile by ID.
    Example: /api/auth/artists/5/
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(is_artist=True)
