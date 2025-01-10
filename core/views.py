from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer, LoginSerializer, VerifyOtpSerializer , ResetPasswordSerializer , ChangePasswordSerializer , LogoutSerializer
from rest_framework.response import Response
from rest_framework import status


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "message": "Login successful",
                "token": serializer.validated_data["token"],
                "user": serializer.validated_data["user"],
            },
            status=status.HTTP_200_OK,
        )


class VerifyOtpView(APIView):
    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "message": "Otp verified successfully",
                "user": serializer.validated_data["user"],
                "token": serializer.validated_data["token"],
            },
            status=status.HTTP_200_OK,
        )
    
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "message": "Password reset successfully",
                "user": serializer.validated_data["user"],
                "token": serializer.validated_data["token"],
            },
            status=status.HTTP_200_OK,
        )
    
class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "message": "Password changed successfully",
                "user": serializer.validated_data["user"],
                "token": serializer.validated_data["token"],
            },
            status=status.HTTP_200_OK,
        )
    
class LogoutView(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "message": "Logout successful",
            },
            status=status.HTTP_200_OK,
        )
