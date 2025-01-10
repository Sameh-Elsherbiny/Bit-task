from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from .models import User
from .utils import create_token


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(source="user.email")
    password = serializers.CharField(source="user.password", write_only=True)

    def validate(self, data):
        email = data.get("user").get("email")
        password = data.get("user").get("password")

        if not email or not password:
            raise serializers.ValidationError(_("email and password are required"))

        user = authenticate(email=email, password=password)

        if email:
            active = User.objects.filter(email=email, is_active=False).exists()

        if user is None or not user.is_active:
            data = {
                "message": _("Invalid email or password or user is inactive"),
                "is_active": not active,
            }
            raise serializers.ValidationError(data)

        data["user"] = user
        data["token"] = create_token(user)
        return data


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    action = serializers.ChoiceField(
        choices=["register", "reset_password", "change_email"]
    )
    new_email = serializers.EmailField(required=False)

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")
        action = data.get("action")
        new_email = data.get("new_email")

        try:
            if action == "register":
                user = User.objects.get(email=email, is_active=False)
            elif action == "reset_password":
                user = User.objects.get(email=email, is_active=True)
            elif action == "change_email":
                user = User.objects.get(email=email, is_active=True)
                user.email = new_email
                user.save()
            else:
                raise serializers.ValidationError(_("Invalid action"))
            token = create_token(user)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("User not found"))

        if user.otp != otp:
            raise serializers.ValidationError(_("OTP not verified"))

        user.is_active = True
        user.otp = None
        user.save()
        data["user"] = user
        data["token"] = token
        print(data)
        return data


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError({"message": _("Passwords do not match")})

        user = User.objects.filter(email=email, is_active=True).first()
        data["user"] = user
        data["token"] = create_token(user)
        return data

    def save(self):
        user = self.validated_data["user"]
        password = self.validated_data["password"]
        user.set_password(password)
        user.otp = None
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        if new_password != confirm_password:
            raise serializers.ValidationError({"message": _("Passwords do not match")})

        user = self.context.get("user")

        if not user.check_password(old_password):
            raise serializers.ValidationError(
                {"message": _("Old password is incorrect")}
            )

        data["user"] = user
        data["token"] = create_token(user)
        return data

    def save(self):
        user = self.validated_data["user"]
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "password", "image"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
            "image": {"required": False},
        }

    def create(self, validated_data):
        if user := User.objects.filter(email=validated_data.get("email")).first():
            raise serializers.ValidationError({"message": _("Email already exists")})
        password = validated_data.pop("password")
        confirm_password = validated_data.get("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError({"message": _("Passwords do not match")})
        user = User.objects.create(**validated_data)
        user.save()
        user.set_password(password)
        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data.pop("password")
        if "email" in validated_data:
            validated_data.pop("email")
        return super().update(instance, validated_data)


class LogoutSerializer(serializers.Serializer):

    def validate(self, attrs):
        user = self.context.get("user")
        return attrs

    def save(self):
        return True
