# # from django.contrib.auth import authenticate, get_user_model
# # from rest_framework import serializers
# # from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# # from rest_framework_simplejwt.views import TokenObtainPairView
# # from .models import User, PortfolioImage, WorkSchedule

# # User = get_user_model()


# # # 1. User Serializer (For viewing profiles)
# # class UserSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = User
# #         fields = (
# #             "id",
# #             "username",
# #             "email",
# #             "is_artist",
# #             "phone_number",
# #             # --- NEW ARTIST FIELDS ---
# #             "profile_image",
# #             "bio",
# #             "years_of_experience",
# #             "shop_name",
# #             "city",
# #             "instagram_link",
# #             "hourly_rate",
# #             "minimum_charge",
# #             "styles",
# #         )


# # # 2. Registration Serializer (For Sign Up)
# # class UserRegistrationSerializer(serializers.ModelSerializer):
# #     password = serializers.CharField(write_only=True)

# #     class Meta:
# #         model = User
# #         fields = [
# #             "username",
# #             "email",
# #             "password",
# #             "phone_number",
# #             "is_artist",
# #             "shop_name",
# #             "city",
# #             "instagram_link",
# #         ]
# #         extra_kwargs = {
# #             "phone_number": {"required": True},
# #             "email": {"required": True},
# #         }

# #     def validate(self, data):
# #         # 2. Custom Validation: Enforce Artist Fields if is_artist is True
# #         if data.get("is_artist", False):
# #             required_artist_fields = ["shop_name", "city", "instagram_link"]
# #             missing_fields = [
# #                 field for field in required_artist_fields if not data.get(field)
# #             ]

# #             if missing_fields:
# #                 raise serializers.ValidationError(
# #                     {
# #                         field: "This field is required for artist accounts."
# #                         for field in missing_fields
# #                     }
# #                 )

# #         return data

# #     def create(self, validated_data):
# #         # Standard creation with password hashing
# #         password = validated_data.pop("password", None)
# #         user = self.Meta.model(**validated_data)
# #         if password is not None:
# #             user.set_password(password)
# #         user.save()
# #         return user


# # # 3. Login Serializer (Stays the same)
# # class UserLoginSerializer(serializers.Serializer):
# #     email = serializers.EmailField()
# #     password = serializers.CharField(write_only=True)

# #     def validate(self, data):
# #         email = data.get("email")
# #         password = data.get("password")

# #         if email and password:
# #             user = authenticate(
# #                 request=self.context.get("request"),
# #                 email=email,
# #                 password=password,
# #             )
# #             if not user:
# #                 raise serializers.ValidationError("Invalid email or password.")
# #         else:
# #             raise serializers.ValidationError('Must include "email" and "password".')

# #         data["user"] = user
# #         return data


# # class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
# #     @classmethod
# #     def get_token(cls, user):
# #         token = super().get_token(user)

# #         # Add custom claims to the token payload (optional, useful for decoding on client)
# #         token["email"] = user.email
# #         token["is_artist"] = user.is_artist
# #         return token

# #     def validate(self, attrs):
# #         # This method controls the actual JSON response body
# #         data = super().validate(attrs)

# #         # Add extra response data
# #         data["user_id"] = self.user.id
# #         data["email"] = self.user.email
# #         data["username"] = self.user.username
# #         data["is_artist"] = self.user.is_artist

# #         # Handle ImageField safely (return URL or null)
# #         if self.user.profile_image:
# #             data["profile_image"] = self.user.profile_image.url
# #         else:
# #             data["profile_image"] = None

# #         return data


# # class CustomTokenObtainPairView(TokenObtainPairView):
# #     serializer_class = CustomTokenObtainPairSerializer


# # # added

# # class PortfolioImageSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = PortfolioImage
# #         fields = ['id', 'image', 'created_at']

# # class WorkScheduleSerializer(serializers.ModelSerializer):
# #     day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)

# #     class Meta:
# #         model = WorkSchedule
# #         fields = ['id', 'day_of_week', 'day_name', 'is_active', 'start_time', 'end_time', 'break_start', 'break_end']

# # class ArtistDashboardSerializer(serializers.ModelSerializer):
# #     portfolio = PortfolioImageSerializer(many=True, read_only=True)
# #     schedule = WorkScheduleSerializer(many=True, read_only=True)

# #     class Meta:
# #         model = User
# #         fields = ['id', 'username', 'email', 'bio', 'city', 'shop_name', 'styles', 'profile_image', 'portfolio', 'schedule']

# from django.contrib.auth import authenticate
# from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView

# from .models import PortfolioImage, User, WorkSchedule

# # ==========================================
# # 1. BASE USER SERIALIZERS
# # ==========================================


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = (
#             "id",
#             "username",
#             "email",
#             "is_artist",
#             "is_active",
#             "phone_number",
#             "profile_image",
#             "bio",
#             "years_of_experience",
#             "shop_name",
#             "city",
#             "instagram_link",
#             "hourly_rate",
#             "minimum_charge",
#             "styles",
#         )


# class UserRegistrationSerializer(serializers.ModelSerializer):
#     """
#     Serializer for OTP-based Sign Up.
#     REMOVED: Password field (since we use OTP).
#     """

#     class Meta:
#         model = User
#         fields = [
#             "username",
#             "email",
#             "phone_number",
#             "is_artist",
#             "shop_name",
#             "city",
#             "instagram_link",
#         ]
#         extra_kwargs = {
#             "phone_number": {"required": True},
#             "email": {"required": True},
#         }

#     def validate(self, data):
#         if data.get("is_artist", False):
#             required_artist_fields = ["shop_name", "city", "instagram_link"]
#             missing_fields = [f for f in required_artist_fields if not data.get(f)]
#             if missing_fields:
#                 raise serializers.ValidationError(
#                     {f: "Required for artists" for f in missing_fields}
#                 )
#         return data

#     def create(self, validated_data):
#         # We set an unusable password because users login via OTP, not password
#         user = self.Meta.model(**validated_data)
#         user.set_unusable_password()
#         user.save()
#         return user


# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     # Password removed from here if you want pure OTP login,
#     # but kept momentarily if you still support password login elsewhere.


# # ==========================================
# # 2. OTP & TOKEN SERIALIZERS
# # ==========================================


# class SendOTPSerializer(serializers.Serializer):
#     email = serializers.EmailField()


# class VerifyOTPSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     otp = serializers.CharField(max_length=6)


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token["email"] = user.email
#         token["is_artist"] = user.is_artist
#         return token

#     def validate(self, attrs):
#         data = super().validate(attrs)
#         data["user_id"] = self.user.id
#         data["email"] = self.user.email
#         data["username"] = self.user.username
#         data["is_artist"] = self.user.is_artist
#         data["profile_image"] = (
#             self.user.profile_image.url if self.user.profile_image else None
#         )
#         return data


# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer


# # ==========================================
# # 3. ARTIST DASHBOARD SERIALIZERS
# # ==========================================


# class PortfolioImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PortfolioImage
#         fields = ["id", "image", "created_at"]


# class WorkScheduleSerializer(serializers.ModelSerializer):
#     day_name = serializers.CharField(source="get_day_of_week_display", read_only=True)

#     class Meta:
#         model = WorkSchedule
#         fields = [
#             "id",
#             "day_of_week",
#             "day_name",
#             "is_active",
#             "start_time",
#             "end_time",
#             "break_start",
#             "break_end",
#         ]


# class ArtistDashboardSerializer(serializers.ModelSerializer):
#     portfolio = PortfolioImageSerializer(many=True, read_only=True)
#     schedule = WorkScheduleSerializer(many=True, read_only=True)

#     class Meta:
#         model = User
#         fields = [
#             "id",
#             "username",
#             "email",
#             "bio",
#             "city",
#             "shop_name",
#             "styles",
#             "profile_image",
#             "portfolio",
#             "schedule",
#         ]


from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

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
            "profile_image",
            "bio",
            "years_of_experience",
            "shop_name",
            "city",
            "instagram_link",
            "hourly_rate",
            "minimum_charge",
            "styles",
        )


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for OTP-based Sign Up.
    REMOVED: Password field (since we use OTP).
    """

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone_number",
            "is_artist",
            "shop_name",
            "city",
            "instagram_link",
        ]
        extra_kwargs = {
            "phone_number": {"required": True},
            "email": {"required": True},
        }

    def validate(self, data):
        if data.get("is_artist", False):
            required_artist_fields = ["shop_name", "city", "instagram_link"]
            missing_fields = [f for f in required_artist_fields if not data.get(f)]
            if missing_fields:
                raise serializers.ValidationError(
                    {f: "Required for artists" for f in missing_fields}
                )
        return data

    def create(self, validated_data):
        # We set an unusable password because users login via OTP, not password
        user = self.Meta.model(**validated_data)
        user.set_unusable_password()
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # Password removed from here if you want pure OTP login,
    # but kept momentarily if you still support password login elsewhere.


# ==========================================
# 2. OTP & TOKEN SERIALIZERS
# ==========================================


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


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


# ==========================================
# 3. ARTIST DASHBOARD SERIALIZERS
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
            "profile_image",
            "portfolio",
            "schedule",
        ]
