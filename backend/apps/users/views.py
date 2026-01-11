# # from django.conf import settings
# # from django.contrib.auth import get_user_model, login, logout
# # from django.core.mail import send_mail
# # from django.template.loader import render_to_string
# # from django.utils import timezone
# # from rest_framework import filters, generics, permissions, status
# # from rest_framework.response import Response
# # from rest_framework.views import APIView

# # # --- Serializers ---
# # from apps.users.serializers import (
# #     ArtistDashboardSerializer,
# #     PortfolioImageSerializer,
# #     SendOTPSerializer,
# #     UserRegistrationSerializer,
# #     UserSerializer,
# #     VerifyOTPSerializer,
# #     WorkScheduleSerializer,
# # )

# # # --- Utils ---
# # # Ensure you have these functions in apps/users/utils.py
# # from apps.users.utils import generate_otp, get_otp_expiry

# # # --- Models ---
# # from .models import PortfolioImage, WorkSchedule

# # User = get_user_model()

# # # ==========================================
# # # AUTHENTICATION VIEWS (OTP BASED)
# # # ==========================================


# # class RegisterView(APIView):
# #     permission_classes = [permissions.AllowAny]

# #     def post(self, request):
# #         serializer = UserRegistrationSerializer(data=request.data)
# #         if serializer.is_valid():
# #             # 1. Create the user (Inactive by default)
# #             user = serializer.save()
# #             user.is_active = False

# #             # 2. Generate OTP
# #             otp_code = generate_otp()
# #             user.otp = otp_code
# #             user.otp_expiry = get_otp_expiry()
# #             user.save()

# #             # --- SCENARIO A: Artist (Manual Approval) ---
# #             if user.is_artist:
# #                 # Artists still get OTP to verify email, but remain inactive until admin approves?
# #                 # Or you can skip OTP for artists and send "Pending" email.
# #                 # Assuming here we want them to verify email first:
# #                 pass

# #             # --- SCENARIO B: Regular User & Artist Email Verification ---
# #             print(f"DEBUG OTP: {otp_code}")  # For testing without email setup

# #             try:
# #                 send_mail(
# #                     "Verify your Inkspire Account",
# #                     f"Welcome {user.username}! Your verification code is: {otp_code}",
# #                     settings.DEFAULT_FROM_EMAIL,
# #                     [user.email],
# #                     fail_silently=False,
# #                 )
# #             except Exception as e:
# #                 print(f"Email Error: {e}")
# #                 return Response(
# #                     {"warning": "User created, but email failed to send."}, status=201
# #                 )

# #             return Response(
# #                 {
# #                     "message": "Registration successful! OTP sent to email.",
# #                     "email": user.email,
# #                 },
# #                 status=status.HTTP_201_CREATED,
# #             )

# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # class VerifyOTPView(APIView):
# #     """
# #     Verifies the OTP. If correct, activates the user and logs them in.
# #     """

# #     permission_classes = [permissions.AllowAny]

# #     def post(self, request):
# #         serializer = VerifyOTPSerializer(data=request.data)
# #         if serializer.is_valid():
# #             email = serializer.validated_data["email"]
# #             otp_input = serializer.validated_data["otp"]

# #             try:
# #                 user = User.objects.get(email=email)
# #             except User.DoesNotExist:
# #                 return Response({"error": "User not found"}, status=404)

# #             # Check OTP
# #             if user.otp != otp_input:
# #                 return Response({"error": "Invalid OTP"}, status=400)

# #             # Check Expiry
# #             if user.otp_expiry and timezone.now() > user.otp_expiry:
# #                 return Response({"error": "OTP has expired"}, status=400)

# #             # Activate User
# #             user.is_active = True
# #             user.otp = None
# #             user.otp_expiry = None
# #             user.save()

# #             # Login the user
# #             login(request, user)

# #             return Response(
# #                 {
# #                     "message": "Verification successful! You are now logged in.",
# #                     "user": UserSerializer(user).data,
# #                 },
# #                 status=200,
# #             )

# #         return Response(serializer.errors, status=400)


# # class LoginWithOTPView(APIView):
# #     """
# #     Initiates login by sending an OTP to existing users.
# #     """

# #     permission_classes = [permissions.AllowAny]

# #     def post(self, request):
# #         serializer = SendOTPSerializer(data=request.data)
# #         if serializer.is_valid():
# #             email = serializer.validated_data["email"]
# #             try:
# #                 user = User.objects.get(email=email)
# #             except User.DoesNotExist:
# #                 return Response({"error": "User not found."}, status=404)

# #             otp = generate_otp()
# #             user.otp = otp
# #             user.otp_expiry = get_otp_expiry()
# #             user.save()

# #             print(f"DEBUG LOGIN OTP: {otp}")
# #             send_mail(
# #                 "Inkspire Login Code",
# #                 f"Your login code is: {otp}",
# #                 settings.DEFAULT_FROM_EMAIL,
# #                 [email],
# #                 fail_silently=False,
# #             )
# #             return Response({"message": "OTP sent to email", "email": email})
# #         return Response(serializer.errors, status=400)


# # class LogoutView(APIView):
# #     def post(self, request):
# #         logout(request)
# #         return Response(
# #             {"message": "Successfully logged out"}, status=status.HTTP_200_OK
# #         )


# # class UserView(APIView):
# #     permission_classes = [permissions.IsAuthenticated]

# #     def get(self, request):
# #         serializer = UserSerializer(request.user)
# #         return Response(serializer.data)


# # # ==========================================
# # # ARTIST & DASHBOARD VIEWS (Kept same)
# # # ==========================================
# # # ... (Keep your ArtistListView, ArtistDetailView, ArtistDashboardView, etc. here)
# # class ArtistListView(generics.ListAPIView):
# #     serializer_class = UserSerializer
# #     permission_classes = [permissions.AllowAny]
# #     queryset = User.objects.filter(is_artist=True)
# #     filter_backends = [filters.SearchFilter]
# #     search_fields = ["username", "bio", "styles", "city", "shop_name"]


# # class ArtistDetailView(generics.RetrieveAPIView):
# #     serializer_class = UserSerializer
# #     permission_classes = [permissions.AllowAny]
# #     queryset = User.objects.filter(is_artist=True)


# # class ArtistDashboardView(APIView):
# #     permission_classes = [permissions.IsAuthenticated]

# #     def get(self, request):
# #         user = request.user
# #         if not user.is_artist:
# #             return Response({"error": "Only artists have dashboards"}, status=403)
# #         for i in range(7):
# #             WorkSchedule.objects.get_or_create(artist=user, day_of_week=i)
# #         serializer = ArtistDashboardSerializer(user)
# #         data = serializer.data
# #         data["revenue"] = 0
# #         return Response(data)


# # class UpdateScheduleView(APIView):
# #     permission_classes = [permissions.IsAuthenticated]

# #     def post(self, request):
# #         for day_data in request.data:
# #             day_obj = WorkSchedule.objects.get(
# #                 artist=request.user, day_of_week=day_data["day_of_week"]
# #             )
# #             serializer = WorkScheduleSerializer(day_obj, data=day_data, partial=True)
# #             if serializer.is_valid():
# #                 serializer.save()
# #         return Response({"message": "Schedule updated successfully!"})


# # class ManagePortfolioView(APIView):
# #     permission_classes = [permissions.IsAuthenticated]

# #     def post(self, request):
# #         serializer = PortfolioImageSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save(artist=request.user)
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# #     def delete(self, request, pk):
# #         image = PortfolioImage.objects.filter(id=pk, artist=request.user).first()
# #         if image:
# #             image.delete()
# #             return Response({"message": "Image deleted"})
# #         return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)


# from django.conf import settings
# from django.contrib.auth import get_user_model, login, logout
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils import timezone
# from rest_framework import filters, generics, permissions, status
# from rest_framework.response import Response
# from rest_framework.views import APIView

# # ✅ ADDED MISSING IMPORTS HERE
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.views import TokenObtainPairView

# # --- Serializers ---
# from apps.users.serializers import (
#     ArtistDashboardSerializer,
#     CustomTokenObtainPairSerializer,  # This comes from serializers.py
#     PortfolioImageSerializer,
#     SendOTPSerializer,
#     UserRegistrationSerializer,
#     UserSerializer,
#     VerifyOTPSerializer,
#     WorkScheduleSerializer,
# )

# # --- Utils ---
# from apps.users.utils import generate_otp, get_otp_expiry

# # --- Models ---
# from .models import PortfolioImage, WorkSchedule

# User = get_user_model()

# # ==========================================
# # AUTHENTICATION VIEWS (OTP BASED)
# # ==========================================


# class RegisterView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             # 1. Create the user (Inactive by default)
#             user = serializer.save()
#             user.is_active = False

#             # 2. Generate OTP
#             otp_code = generate_otp()
#             user.otp = otp_code
#             user.otp_expiry = get_otp_expiry()
#             user.save()

#             # --- SCENARIO A: Artist (Manual Approval) ---
#             if user.is_artist:
#                 pass

#             # --- SCENARIO B: Regular User & Artist Email Verification ---
#             print(f"DEBUG OTP: {otp_code}")

#             try:
#                 send_mail(
#                     "Verify your Inkspire Account",
#                     f"Welcome {user.username}! Your verification code is: {otp_code}",
#                     settings.DEFAULT_FROM_EMAIL,
#                     [user.email],
#                     fail_silently=False,
#                 )
#             except Exception as e:
#                 print(f"Email Error: {e}")
#                 return Response(
#                     {"warning": "User created, but email failed to send."}, status=201
#                 )

#             return Response(
#                 {
#                     "message": "Registration successful! OTP sent to email.",
#                     "email": user.email,
#                 },
#                 status=status.HTTP_201_CREATED,
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class VerifyOTPView(APIView):
#     """
#     Verifies the OTP. If correct, activates the user and logs them in.
#     """

#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         try:
#             email = request.data.get("email")
#             otp_input = request.data.get("otp")

#             # 1. Validate Input
#             if not email or not otp_input:
#                 return Response(
#                     {"error": "Email and OTP are required"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             # 2. Find User Safely
#             try:
#                 user = User.objects.get(email=email)
#             except User.DoesNotExist:
#                 return Response(
#                     {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
#                 )

#             # 3. Check OTP
#             if user.otp != otp_input:
#                 return Response(
#                     {"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
#                 )

#             # 4. Check Expiry
#             if user.otp_expiry and timezone.now() > user.otp_expiry:
#                 return Response(
#                     {"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST
#                 )

#             # 5. Success! Activate User
#             user.is_active = True
#             user.otp = None
#             user.otp_expiry = None
#             user.save()

#             # 6. Generate Tokens (JWT) & Return Data
#             refresh = RefreshToken.for_user(user)

#             return Response(
#                 {
#                     "message": "Account verified successfully",
#                     "refresh": str(refresh),
#                     "access": str(refresh.access_token),
#                     "user": {
#                         "id": user.id,
#                         "username": user.username,
#                         "email": user.email,
#                         "is_artist": user.is_artist,
#                     },
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         except Exception as e:
#             print(f"CRITICAL ERROR IN VERIFY OTP: {str(e)}")
#             return Response(
#                 {"error": "Internal Server Error. Please try again."},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )


# class LoginWithOTPView(APIView):
#     """
#     Initiates login by sending an OTP to existing users.
#     """

#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = SendOTPSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data["email"]
#             try:
#                 user = User.objects.get(email=email)
#             except User.DoesNotExist:
#                 return Response({"error": "User not found."}, status=404)

#             otp = generate_otp()
#             user.otp = otp
#             user.otp_expiry = get_otp_expiry()
#             user.save()

#             print(f"DEBUG LOGIN OTP: {otp}")
#             send_mail(
#                 "Inkspire Login Code",
#                 f"Your login code is: {otp}",
#                 settings.DEFAULT_FROM_EMAIL,
#                 [email],
#                 fail_silently=False,
#             )
#             return Response({"message": "OTP sent to email", "email": email})
#         return Response(serializer.errors, status=400)


# class LogoutView(APIView):
#     def post(self, request):
#         logout(request)
#         return Response(
#             {"message": "Successfully logged out"}, status=status.HTTP_200_OK
#         )


# class UserView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         serializer = UserSerializer(request.user)
#         return Response(serializer.data)


# # ==========================================
# # ARTIST & DASHBOARD VIEWS
# # ==========================================


# class ArtistListView(generics.ListAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [permissions.AllowAny]
#     queryset = User.objects.filter(is_artist=True)
#     filter_backends = [filters.SearchFilter]
#     search_fields = ["username", "bio", "styles", "city", "shop_name"]


# class ArtistDetailView(generics.RetrieveAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [permissions.AllowAny]
#     queryset = User.objects.filter(is_artist=True)


# class ArtistDashboardView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         if not user.is_artist:
#             return Response({"error": "Only artists have dashboards"}, status=403)
#         for i in range(7):
#             WorkSchedule.objects.get_or_create(artist=user, day_of_week=i)
#         serializer = ArtistDashboardSerializer(user)
#         data = serializer.data
#         data["revenue"] = 0
#         return Response(data)


# class UpdateScheduleView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         for day_data in request.data:
#             day_obj = WorkSchedule.objects.get(
#                 artist=request.user, day_of_week=day_data["day_of_week"]
#             )
#             serializer = WorkScheduleSerializer(day_obj, data=day_data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#         return Response({"message": "Schedule updated successfully!"})


# class ManagePortfolioView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         serializer = PortfolioImageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(artist=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         image = PortfolioImage.objects.filter(id=pk, artist=request.user).first()
#         if image:
#             image.delete()
#             return Response({"message": "Image deleted"})
#         return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)


# # ==========================================
# # JWT CUSTOM VIEW (Fixes Circular Import)
# # ==========================================


# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer


from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import filters, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# --- Serializers ---
from apps.users.serializers import (
    ArtistDashboardSerializer,
    PortfolioImageSerializer,
    SendOTPSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    VerifyOTPSerializer,
    WorkScheduleSerializer,
)

# --- Utils ---
# Ensure you have these functions in apps/users/utils.py
from apps.users.utils import generate_otp, get_otp_expiry

# --- Models ---
from .models import PortfolioImage, WorkSchedule

User = get_user_model()

# ==========================================
# AUTHENTICATION VIEWS (OTP BASED)
# ==========================================


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["is_artist"] = user.is_artist
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user_id"] = self.user.id
        data["email"] = self.user.email
        data["username"] = self.user.username
        data["is_artist"] = self.user.is_artist
        data["profile_image"] = (
            self.user.profile_image.url if self.user.profile_image else None
        )
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # 1. Create the user (Inactive by default)
            user = serializer.save()
            user.is_active = False

            # 2. Generate OTP
            otp_code = generate_otp()
            user.otp = otp_code
            user.otp_expiry = get_otp_expiry()
            user.save()

            # --- SCENARIO A: Artist (Manual Approval) ---
            if user.is_artist:
                # Artists still get OTP to verify email, but remain inactive until admin approves?
                # Or you can skip OTP for artists and send "Pending" email.
                # Assuming here we want them to verify email first:
                pass

            # --- SCENARIO B: Regular User & Artist Email Verification ---
            print(f"DEBUG OTP: {otp_code}")  # For testing without email setup

            try:
                send_mail(
                    "Verify your Inkspire Account",
                    f"Welcome {user.username}! Your verification code is: {otp_code}",
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email Error: {e}")
                return Response(
                    {"warning": "User created, but email failed to send."}, status=201
                )

            return Response(
                {
                    "message": "Registration successful! OTP sent to email.",
                    "email": user.email,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    """
    Verifies the OTP. If correct, activates the user and logs them in.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            otp_input = serializer.validated_data["otp"]

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)

            # Check OTP
            if user.otp != otp_input:
                return Response({"error": "Invalid OTP"}, status=400)

            # Check Expiry
            if user.otp_expiry and timezone.now() > user.otp_expiry:
                return Response({"error": "OTP has expired"}, status=400)

            # Activate User
            user.is_active = True
            user.otp = None
            user.otp_expiry = None
            user.save()

            # Login the user
            login(request, user)

            return Response(
                {
                    "message": "Verification successful! You are now logged in.",
                    "user": UserSerializer(user).data,
                },
                status=200,
            )

        return Response(serializer.errors, status=400)


class LoginWithOTPView(APIView):
    """
    Initiates login by sending an OTP to existing users.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=404)

            otp = generate_otp()
            user.otp = otp
            user.otp_expiry = get_otp_expiry()
            user.save()

            print(f"DEBUG LOGIN OTP: {otp}")
            send_mail(
                "Inkspire Login Code",
                f"Your login code is: {otp}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return Response({"message": "OTP sent to email", "email": email})
        return Response(serializer.errors, status=400)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(
            {"message": "Successfully logged out"}, status=status.HTTP_200_OK
        )


class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# ==========================================
# ARTIST & DASHBOARD VIEWS (Kept same)
# ==========================================
# ... (Keep your ArtistListView, ArtistDetailView, ArtistDashboardView, etc. here)
class ArtistListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(is_artist=True)
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "bio", "styles", "city", "shop_name"]


class ArtistDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(is_artist=True)


class ArtistDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_artist:
            return Response({"error": "Only artists have dashboards"}, status=403)
        for i in range(7):
            WorkSchedule.objects.get_or_create(artist=user, day_of_week=i)
        serializer = ArtistDashboardSerializer(user)
        data = serializer.data
        data["revenue"] = 0
        return Response(data)


class UpdateScheduleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        for day_data in request.data:
            day_obj = WorkSchedule.objects.get(
                artist=request.user, day_of_week=day_data["day_of_week"]
            )
            serializer = WorkScheduleSerializer(day_obj, data=day_data, partial=True)
            if serializer.is_valid():
                serializer.save()
        return Response({"message": "Schedule updated successfully!"})


class ManagePortfolioView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PortfolioImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(artist=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        image = PortfolioImage.objects.filter(id=pk, artist=request.user).first()
        if image:
            image.delete()
            return Response({"message": "Image deleted"})
        return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
