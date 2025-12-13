from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


# 1. User Serializer (For viewing profiles)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_artist",
            "phone_number",
            # --- NEW ARTIST FIELDS ---
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


# 2. Registration Serializer (For Sign Up)
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "is_artist",
            "phone_number",
            # Allow artists to fill these out during signup
            "bio",
            "shop_name",
            "city",
            "styles",
            "years_of_experience",
        )

    def create(self, validated_data):
        # 1. Pop the password so we can hash it properly
        password = validated_data.pop("password")

        # 2. Pop standard auth fields
        username = validated_data.pop("username")
        email = validated_data.pop("email")

        # 3. Create the user using Django's helper
        # **validated_data passes all remaining fields (is_artist, bio, phone, etc.) automatically
        user = User.objects.create_user(
            username=username, email=email, password=password, **validated_data
        )
        return user


# 3. Login Serializer (Stays the same)
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                email=email,
                password=password,
            )
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        data["user"] = user
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the token payload (optional, useful for decoding on client)
        token["email"] = user.email
        token["is_artist"] = user.is_artist
        return token

    def validate(self, attrs):
        # This method controls the actual JSON response body
        data = super().validate(attrs)

        # Add extra response data
        data["user_id"] = self.user.id
        data["email"] = self.user.email
        data["username"] = self.user.username
        data["is_artist"] = self.user.is_artist

        # Handle ImageField safely (return URL or null)
        if self.user.profile_image:
            data["profile_image"] = self.user.profile_image.url
        else:
            data["profile_image"] = None

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
