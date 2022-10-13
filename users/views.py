from django.shortcuts import render
from yaml import serialize
from .models import (
    User,
    UserOTP,
    SMSLog,
    SMSToken,
)
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    UserSerializer,
    CreateUserSerializer,
    UserOTPSerializer,
    VerifyOTPSerializer,
    UserLoginSerializer,
)
from .utils import generate_otp, send_otp
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout, authenticate

# Create your views here.

class UsersListView(generics.ListAPIView):
    """
        List all users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserView(generics.RetrieveUpdateDestroyAPIView):
    """
        Retrieve, update or delete a user instance.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        Retrieve, update or delete a user instance.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)
        

class UserCreateView(generics.CreateAPIView):
    """
        Create a new user
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data
        phone: str = data.get('phone')
        user: User = User.objects.filter(phone=phone).first()
        if user is not None:
            return Response({'message': 'User with this phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            full_name = data.get('full_name')
            otp = generate_otp()
            message = f"UzPitak...\nSizning kodingiz: {otp}"
            # user.save()
            try:
                send_otp(phone, message)
                otp_count = SMSLog.objects.filter(phone=phone).first()
                if otp_count:
                    otp_count.count += 1
                    otp_count.message = message
                    otp_count.save()
                else:
                    otp_count = SMSLog.objects.create(phone=phone, count=1, message=message)
                    otp_count.save()
                # SMSLog.objects.create(phone=phone, message=message, count=otp_count)
                user = User.objects.create_user(phone=phone, full_name=full_name, otp=otp, password=otp, is_verified=False)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


class VerifyOTPView(APIView):
    serializer_class = VerifyOTPSerializer
    def validate(self, data):
        phone = data.get('phone')
        otp = data.get('otp')
        if phone is None:
            raise ValidationError({'phone': _('Telefon kiritilishi shart')})
        if otp is None:
            raise ValidationError({'otp': _('OTP kiritilishi shart')})
        
    def post(self, request, *args, **kwargs):
        data = request.data
        self.validate(data)
        phone = data.get('phone')
        otp = data.get('otp')
        user = User.objects.filter(phone=phone).first()
        if user is None:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if user.otp != otp:
            return Response({'message': 'Wrong OTP'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_verified and user.otp == otp:
            print(f"User {user} is verified")
            print(f"User {user.is_authenticated}")
            user.is_verified = True
            user.save()
            auth_user = authenticate(phone=phone, password=otp)
            print(f"User {auth_user} is authenticated")
            login(request, auth_user)
            return Response({'message': 'User verified successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'User already verified'}, status=status.HTTP_400_BAD_REQUEST)
        # return Response({'message': 'User verified successfully'}, status=status.HTTP_200_OK) 

class LoginView(APIView):
    serializer_class = UserLoginSerializer
    def validate(self, data):
        phone = data.get('phone')
        if phone is None:
            raise ValidationError({'phone': _('Telefon kiritilishi shart')})
       

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = request.data
        self.validate(data)
        phone = data.get('phone')
        user = User.objects.filter(phone=phone).first()
        if user is None:
            return Response({'message': 'User not found', 'status': False}, status=status.HTTP_404_NOT_FOUND)
        if not user.is_verified:
            return Response({'message': 'User is not verified', 'status': False}, status=status.HTTP_400_BAD_REQUEST)
        if user.is_verified:
            user = authenticate(phone=phone, password=user.otp)
            if user is not None:
                login(request, user)
                return Response({'message': 'User logged in successfully', 'status': True}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Wrong credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Wrong credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.is_verified = False
        logout(request)
        return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)



