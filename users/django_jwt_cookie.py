from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.sessions.backends.signed_cookies import SessionStore

from rest_framework_simplejwt.tokens import RefreshToken