from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import User, UserOTP, SMSLog, SMSToken
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'full_name', 'is_verified', 'is_deleted', 'is_superuser', 'otp')
    list_filter = ('is_verified', 'is_deleted', 'is_superuser')
    search_fields = ('phone', 'full_name')
    ordering = ('-id',)
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('phone', 'full_name', 'phone2', 'otp', 'is_verified', )
        }),
        ('Qo\'shimcha ma\'lumotlar', {
            'fields': ('password', 'is_deleted', 'is_superuser', 'is_staff')
        }),
        
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'full_name', 'phone2', 'otp', 'is_verified', 'is_deleted', ),
        }),
    )
    filter_horizontal = ()

    class Meta:
        model = User


@admin.register(UserOTP)
class UserOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'is_verified', 'is_deleted')
    list_filter = ('is_verified', 'is_deleted')
    search_fields = ('user', 'otp')
    ordering = ('-id',)

    class Meta:
        model = UserOTP

@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = ('phone', 'message', 'count', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('phone', 'message')
    ordering = ('-id',)

    class Meta:
        model = SMSLog

@admin.register(SMSToken)
class SMSTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('user', 'token')
    ordering = ('-id',)

    class Meta:
        model = SMSToken

