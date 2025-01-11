from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import User , Category
from .serializers import UserSerializer,CategorySerializer ,SendOTPSerializer, LoginSerializer, VerifyOtpSerializer , ResetPasswordSerializer , ChangePasswordSerializer , LogoutSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class LoginView(APIView):
    serializer_class = LoginSerializer
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
    serializer_class = ResetPasswordSerializer
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
    serializer_class = ChangePasswordSerializer
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "message": "Password changed successfully",
                "user": serializer.validated_data["user"],
                "token": serializer.validated_data["token"],
            },
            status=status.HTTP_200_OK,
        )
    

class SendOTPView(APIView):
    serializer_class = SendOTPSerializer
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "OTP sent successfully"}, status=status.HTTP_200_OK
        )
    
class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Category.objects.all().order_by('name')
    
   