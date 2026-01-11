# from pathlib import Path

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

# # Quick-start development settings - unsuitable for production
# SECRET_KEY = "django-insecure-^9+uezzcxq8u0&8e4y6sqm=^zgqk0z1o)dutsvi+5i=-!8l5td"
# DEBUG = True
# ALLOWED_HOSTS = []

# # Application definition
# INSTALLED_APPS = [
#     # user apps
#     "apps.appointment",
#     "apps.users",
#     "apps.price",
#     "apps.shop",
#     # django
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",
#     # third party
#     "rest_framework",
#     "corsheaders",
#     "rest_framework_simplejwt",
#     # "django_filters", # Uncomment if you installed 'pip install django-filter'
# ]

# MIDDLEWARE = [
#     "corsheaders.middleware.CorsMiddleware",  # cors headers
#     "django.middleware.security.SecurityMiddleware",
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]

# ROOT_URLCONF = "core.urls"

# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         # UPDATE THIS LINE: Point to the 'templates' folder
#         "DIRS": [BASE_DIR / "templates"],
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.request",
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = "core.wsgi.application"

# # Database
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# # Password validation
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
#     },
# ]

# # Internationalization
# LANGUAGE_CODE = "en-us"
# TIME_ZONE = "UTC"
# USE_I18N = True
# USE_TZ = True

# # Static files (CSS, JavaScript, Images)
# STATIC_URL = "static/"

# # Media Files (For User Uploads / Shop Images)
# MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR / "media"

# # CORS Settings (Frontend Connection)
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
# ]

# CORS_ALLOWED_CREDENTIALS = True
# CORS_ALLOWED_HEADERS = (
#     "accept",
#     "accept-encoding",
#     "authorization",
#     "content-type",
#     "dnt",
#     "origin",
#     "user-agent",
#     "x-csrftoken",
#     "x-requested-with",
# )

# # Custom User Model
# AUTH_USER_MODEL = "users.User"

# if DEBUG:
#     EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# else:
#     """
#     """
#     # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#     # EMAIL_HOST = 'smtp.gmail.com'
#     # EMAIL_PORT = 587
#     # EMAIL_USE_TLS = True
#     # EMAIL_HOST_USER = 'your-email@gmail.com'
#     # EMAIL_HOST_PASSWORD = 'your-app-password'


# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     )
# }


# APPEND_SLASH = False


# # added
# # Email Configuration (Gmail)
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = "rojeshmaharjan2002@gmail.com"  # <--- Your actual Gmail address
# EMAIL_HOST_PASSWORD = "eag uoqy oixo kqft"
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = "django-insecure-^9+uezzcxq8u0&8e4y6sqm=^zgqk0z1o)dutsvi+5i=-!8l5td"
DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    # user apps
    "apps.appointment",
    "apps.users",
    "apps.price",
    "apps.shop",
    "library",  # <--- ADDED THIS (Fixes your error)
    # django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # cors headers
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

# Media Files (For User Uploads / Shop Images)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# CORS Settings (Frontend Connection)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOWED_CREDENTIALS = True
CORS_ALLOWED_HEADERS = (
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)

# Custom User Model
AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}

APPEND_SLASH = False

# ==========================================
# EMAIL SETTINGS (REAL GMAIL)
# ==========================================
# If you want to switch back to Console (testing without internet),
# comment out the lines below and uncomment the Console Backend line.

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  # <--- Use this for dev/testing only

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = "rojeshmaharjan2002@gmail.com"
# EMAIL_HOST_PASSWORD = "eagu oqyo ixok qft"  # (I kept your app password here)
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
