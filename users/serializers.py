from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    User, 
    UserOTP,
    SMSLog,
    SMSToken,
)
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
        User Serializer
    """
    class Meta:
        model = User
        fields = ['id', 'phone', 'full_name', 'phone2', 'is_verified', 'is_deleted']


class CreateUserSerializer(serializers.ModelField):
    class Meta:
        model = User
        fields = ['phone', 'full_name', 'phone2', 'is_verified', 'otp', 'is_deleted']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    
class UserOTPSerializer(serializers.ModelSerializer):
    """
        User OTP Serializer
    """
    class Meta:
        model = UserOTP
        fields = ['user', 'otp', 'is_verified', 'is_deleted']

    