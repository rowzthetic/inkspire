from django.contrib.auth import login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import filters, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

# Import serializers
from apps.users.serializers import (
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)

# Import the token generator
from apps.users.utils import account_activation_token

User = get_user_model()


# --- AUTHENTICATION VIEWS ---

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # 1. Create the user but DEACTIVATE them immediately
            user = serializer.save()
            user.is_active = False
            user.save()

            # 2. Setup Email Data
            # For local testing, we hardcode the domain if get_current_site fails
            domain = 'localhost:5173' 
            mail_subject = 'Activate your Inkspire account.'
            
            # Generate unique ID and Token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            
            # 3. Create the Email Body
            message = render_to_string('emails/activate_account.html', {
                'user': user,
                'domain': domain,
                'uid': uid,
                'token': token,
            })
            
            # 4. Send the Email
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()

            return Response(
                {"message": "Registration successful! Please check your email to activate your account."}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccountView(APIView):
    """
    This view handles the link clicked by the user in their email.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            # Decode the User ID
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Check if the token is valid for this user
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Account activated successfully! You can now login."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Activation link is invalid or expired!"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            
            # Check if they have activated their account
            if not user.is_active:
                return Response({"error": "Account not active. Please check your email."}, status=status.HTTP_403_FORBIDDEN)

            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(
            {"message": "Successfully logged out"},
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
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(is_artist=True)

    filter_backends = [filters.SearchFilter]
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
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(is_artist=True)