from random import choice
from eskiz_sms import EskizSMS
from django.conf import settings

eskiz_conf = EskizSMS(
    **settings.ESKIZ_SMS
)

def generate_otp() -> str:
    """
        Generate 4 digit OTP
    """
    return ''.join([choice(choice('0123456789')) for _ in range(4)])

def send_otp(phone: str, message: str) -> None:
    """
        Send OTP message to user
    """
    eskiz_conf.send_sms(mobile_phone=phone.replace('+', ''), message=message, from_whom='4546', callback_url='http://0000.uz/test.php')
    print(f"SMS {phone} raqamiga yuborildi")