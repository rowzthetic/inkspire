from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import PortfolioImage, User, WorkSchedule

# ==========================================
# 1. BASE USER SERIALIZERS
# ==========================================


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_artist",
            "is_active",
            "phone_number",
            "profile_picture",
            "bio",
            "shop_name",
            "city",
            "instagram_link",
        )


# ==========================================
# 2. REGISTRATION SERIALIZER (Sign Up)
# ==========================================


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for Sign Up (With Password & OTP).
    """

    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "phone_number",
            "is_artist",
            "shop_name",
            "city",
            "instagram_link",
        ]
        extra_kwargs = {
            "phone_number": {"required": False, "allow_blank": True},
            "shop_name": {"required": False, "allow_blank": True},
            "city": {"required": False, "allow_blank": True},
            "instagram_link": {"required": False, "allow_blank": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()


# ==========================================
# 3. OTP SERIALIZERS
# ==========================================


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


# ==========================================
# 4. JWT LOGIN SERIALIZER (Fixes Redirection)
# ==========================================


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims to the token payload
        token["email"] = user.email
        token["is_artist"] = user.is_artist
        return token

    def validate(self, attrs):
        # 1. Allow Login with Email OR Username
        username_or_email = attrs.get("username")

        if username_or_email and "@" in username_or_email:
            User = get_user_model()
            try:
                user_obj = User.objects.get(email=username_or_email)
                attrs["username"] = user_obj.username
            except User.DoesNotExist:
                pass  # Let standard validation handle the failure

        # 2. Standard Validation
        try:
            data = super().validate(attrs)
        except Exception as e:
            raise e

        # 3. ✅ Add User Details to Response (Fixes Frontend Redirect)
        data["user_id"] = self.user.id
        data["email"] = self.user.email
        data["username"] = self.user.username
        data["is_artist"] = self.user.is_artist  # This is the key field!

        # Handle Profile Image safely
        if hasattr(self.user, "profile_picture") and self.user.profile_picture:
            data["profile_picture"] = self.user.profile_picture.url
        elif hasattr(self.user, "profile_image") and self.user.profile_image:
            # Fallback if your model uses 'profile_image' instead of 'profile_picture'
            data["profile_picture"] = self.user.profile_image.url
        else:
            data["profile_picture"] = None

        return data


# ==========================================
# 5. ARTIST DASHBOARD SERIALIZERS
# ==========================================


class PortfolioImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioImage
        fields = ["id", "image", "created_at"]


class WorkScheduleSerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source="get_day_of_week_display", read_only=True)

    class Meta:
        model = WorkSchedule
        fields = [
            "id",
            "day_of_week",
            "day_name",
            "is_active",
            "start_time",
            "end_time",
            "break_start",
            "break_end",
        ]


class ArtistDashboardSerializer(serializers.ModelSerializer):
    portfolio = PortfolioImageSerializer(many=True, read_only=True)
    schedule = WorkScheduleSerializer(many=True, read_only=True)
    # If your PortfolioImage model uses a different related_name (e.g., 'portfolio_images'),
    # you might need: portfolio_images = PortfolioImageSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "bio",
            "city",
            "shop_name",
            "styles",
            "profile_picture",
            "portfolio",  # Make sure this matches related_name in models.py
            "schedule",
        ]
