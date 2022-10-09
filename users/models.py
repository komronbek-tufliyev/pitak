from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator



# Create your models here.

class User(AbstractUser):
    username = None
    phone_regex = RegexValidator(regex=r'^[+]998[0-9]{2}[0-9]{7}$', message="Faqat +998xxxxxxxxx formatida raqam kiriting")
    phone = models.CharField(_('Telefon raqam'), validators=[phone_regex], max_length=13, unique=True)
    phone2 = models.CharField(validators=[phone_regex], max_length=13, unique=True, blank=True, null=True)
    full_name = models.CharField(_('To\'liq ism'), max_length=255, blank=True, null=True)
    key = models.CharField(max_length=255, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    password = models.CharField(_('Parol'), max_length=128, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    def get_phone(self):
        return self.phone

    def get_phone2(self):
        return self.phone2

    @property
    def isVerified(self):
        return self.is_verified

    @property
    def isDeleted(self):
        return self.is_deleted

        
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('-id',)

class UserOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_otp')
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.otp

    @property
    def isVerified(self):
        return self.is_verified

    @property
    def isDeleted(self):
        return self.is_deleted

    class Meta:
        verbose_name = _('User OTP')
        verbose_name_plural = _('User OTPs')
        ordering = ('-id',)


class SMSLog(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sms')
    phone = models.CharField(max_length=13, blank=True, null=True)
    count = models.IntegerField(default=0)
    message = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    @property
    def isDeleted(self):
        return self.is_deleted

    class Meta:
        verbose_name = _('SMS Log')
        verbose_name_plural = _('SMS Logs')
        ordering = ('-id',)


class SMSToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_token')
    token = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.token

    @property
    def isDeleted(self):
        return self.is_deleted

    class Meta:
        verbose_name = _('SMS Token')
        verbose_name_plural = _('SMS Tokens')
        ordering = ('-id',)