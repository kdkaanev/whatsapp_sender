from .base import *

DEBUG = False

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=['https://yourdomain.com'])

CORS_TRUSTED_ORIGINS = env.list('CORS_TRUSTED_ORIGINS', default=['https://yourdomain.com'])

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = False  # Set to True in production
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')