from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    User, 
    UserOTP,
    SMSLog,
    SMSToken,
)
from django.utils.translation import gettext_lazy as _
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

    def login(self, validated_data):
        phone = validated_data['phone']
        password = validated_data['password']
        user = authenticate(phone=phone, password=password)
        if user:
            return user
        else:
            return False


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'full_name', 'phone2', 'is_verified', 'is_deleted']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        phone = data.get('phone')
        otp = data.get('otp')
        if phone and otp:
            user = User.objects.filter(phone=phone).first()
            if user:
                user_otp = UserOTP.objects.filter(user=user, otp=otp).first()
                if user_otp:
                    user.is_verified = True
                    user.save()
                    return user
                else:
                    raise serializers.ValidationError(_('Invalid OTP'))
            else:
                raise serializers.ValidationError(_('Invalid Phone Number'))
        else:
            raise serializers.ValidationError(_('Phone and OTP are required'))
    
class UserOTPSerializer(serializers.ModelSerializer):
    """
        User OTP Serializer
    """
    class Meta:
        model = UserOTP
        fields = ['user', 'otp', 'is_verified', 'is_deleted']

class UserLoginSerializer(serializers.ModelSerializer):
    """
        User Login Serializer
    """
    phone = serializers.CharField(max_length=13)
    otp = serializers.CharField(max_length=4, required=False)
    # password = serializers.CharField(max_length=128)

    class Meta:
        model = User
        fields = ['phone', 'otp']

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('otp')
        if phone and password:
            user = User.objects.filter(phone=phone).first()
            if user:
                if user.check_password(password):
                    return user
                else:
                    raise serializers.ValidationError(_('Invalid Password'))
            else:
                raise serializers.ValidationError(_('User does not exist'))
        else:
            raise serializers.ValidationError(_('Phone and Password are required'))




