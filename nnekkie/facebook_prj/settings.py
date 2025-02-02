from pathlib import Path
import os

from .env import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default=None)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/c
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# config('DJANGO_DEBUG', default=None)

ALLOWED_HOSTS = ['*']

ALLOWED_HOST = config('ALLOWED_HOST', cast=str, default="")
if ALLOWED_HOST :
    ALLOWED_HOSTS.append(ALLOWED_HOST.strip())


ASGI_APPLICATION = 'facebook_prj.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}



# Application definition
INTERNAL_IPS = [
    '127.0.0.1',
    'corsheaders.middleware.CorsMiddleware',
]

INSTALLED_APPS = [
    # 'django_light',
    'admin_tools_stats',  # this must be BEFORE 'admin_tools' and 'django.contrib.admin'
    'django_nvd3',
    # 'admin_tools',
    # 'pagem',
    'debug_toolbar',
    'jazzmin', 
    'storages',
    'haystack',
    'whoosh',
    'django.contrib.admindocs',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    # 'django_comments',
    # 'rest_framework',
    # 'rest_framework.authtoken',
    'corsheaders',
    'djoser',
    'blog',
    'core',
    'userauths',
    'addon',
    'error',
    'fundraiser',
    'event',
    'forum',
    'grc',
    'product',
    'purchases',

    
    'vendor',

    # THird Party Apps
    'mathfilters',
    'pwa',
    'channels',
    "widget_tweaks",
    'crispy_forms',
    'django_social_share',

    #allauth
    'allauth',
    'allauth.account',
    'allauth.mfa',

    # Optional -- requires install using `django-allauth[socialaccount]`.
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.linkedin',
    'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.google'

]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000"
]
SITE_ID = 7

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # 'pagem.middleware.maintenance_middleware',
   
]

ROOT_URLCONF = 'facebook_prj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.my_context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'facebook_prj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


PRJ_DIR = BASE_DIR.parent
WHOOSH_INDEX = os.path.join(BASE_DIR, 'whoosh/')
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': WHOOSH_INDEX,
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor' 
# from .db import * #no qa

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTHENTICATION_BACKENDS = [

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',

]

# Other Configs
AUTH_USER_MODEL = 'userauths.User'


LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_EMAIL_REQUIRED=True #recommended
# ACCOUNT_CHANGE_EMAIL=False
# ACCOUNT_MAX_EMAIL_ADDRESSES = 6
ACCOUNT_SEESION_REMEMBER = True
ACCOUNT_CHANGE_EMAIL=True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS=1
ACCOUNT_EMAIL_NOTIFICATIONS=True
ACCOUNT_EMAIL_VERIFICATION="mandatory" #recommend
ACCOUNT_LOGIN_BY_CODE_ENABLED=True
ACCOUNT_LOGIN_BY_CODE_MAX_ATTEMPTS=4
ACCOUNT_LOGIN_BY_CODE_TIMEOUT = 10000
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION=False
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE=True
ACCOUNT_LOGIN_ON_PASSWORD_RESET=False
LOGOUT_REDIRECT_URL="/"
ACCOUNT_SESSION_REMEMBER=False
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE=False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE=True
ACCOUNT_USERNAME_BLACKLIST = ['admin','webcog','youtube']
ACCOUNT_UNIQUE_EMAIL=True #recommended
ACCOUNT_USERNAME_MIN_LENGTH=4
ACCOUNT_USERNAME_REQUIRED=True
 


JAZZMIN_SETTINGS = {
    'site_title': 'Nnekkie Development Panel',
    'site_header': "Nnekkie",
    'site_brand': "The future of learning is social",
    'site_logo': 'images/bg.png',
    'login_logo': 'images/nk.png',
    "copyright":"Nnekkie",
    "search_model": ["userauths.user","core.post", "blog.blog", 'product.product',  'product.productattachment'],
    "user_avatar": 'images/me.jpeg',
    "welcome_sign": "Welcome to Nnekki, Login Now.",
    "show_admin_docs": True,
    "topmenu_links": [
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"app":"userauths"},
        {"app": "account"},
        {"app":"core"},
        {"app":"blog"},
        {"app":"product"},
        {"app":"purchases"},
        {"app":"admin_tools_stats"}
    ],
    "usermenu_links":[
        {"app":"userauths"}
    ],
    "order_with_respect_to": [
        "core",
        "core.post",
        "core.friend",
        "core.FriendRequest",
        "userauths",
        "addon",
    ],

    "icons": {
        "admin.LogEntry": "fas fa-file",

        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",

        "userauths.User": "fas fa-user",
        "userauths.Profile": "fas fa-address-card",

        "core.post": "fas fa-th",
        "core.Page": "fas fa-file-alt",
        "core.ReplyComment": "fas fa-reply",
        "core.group": "fas fa-layer-group",
        "core.groupchat": "fas fa-comments",
        "core.notification": "fas fa-bell",
        "core.Comment": "fas fa-comments",
        "core.Friend": "fas fa-user-friends",
        "core.FriendRequest": "fas fa-user-plus",
        "core.GroupChatMessage": "fas fa-comments",
        "product.Product": "fas fa-box",
        "product.ProductAttachment":"fas fa-paperclip",
        "SocialAccount.Socialaccount":"fas fa-user-circle",
        "SocialAccount.SocialApplicationTokens":"fas fa-key",
        "SocialAccount.socialapplications": "fas fa-plug",
        "sites.Site": "fas fa-globe",

        # extra
        "core.grouppost": "fas fa-newspaper",
        "core.grouppostcomment": "fas fa-comments",
        "core.personalchat": "fas fa-comment-dots",
        "core.replygrouppostcomment": "fas fa-reply-all",
        "core.snaps": "fas fa-camera",
        # extra 2
        "accounts.emailaddresses": "fas fa-envelope",
        "admin_tools_stats.cachedvalues": "fas fa-database",
        "admin_tools_stats.dashboardstats": "fas fa-chart-bar",
        "admin_tools_stats.dashboardstatscriteria": "fas fa-filter",
        "blog.blog": "fas fa-blog",
        "blog.comment": "fas fa-comments",
        "blog.followerrequest": "fas fa-user-plus",
        "blog.reply": "fas fa-reply",
        "flatpages.flatpage": "fas fa-file-alt",
    },

    "show_ui_builder": True
}
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": True,
    "brand_colour": "navbar-indigo",
    "accent": "accent-olive",
    "navbar": "navbar-indigo navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-indigo",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": True,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",
    "dark_mode_theme": "cyborg",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True
}
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': ['user', 'repo', 'read:org'],
          "VERIFIED_EMAIL": True,  # optional, but often necessary for OAuth2 apps
    },
}


PAYSTACK_SECRET_KEY = config('PAYSTACK_SECRET_KEY', default=None)
PAYSTACK_PUBLIC_KEY = config('PAYSTACK_PUBLIC_KEY', default=None)


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
PROTECTED_MEDIA_ROOT = BASE_DIR.parent / 'local-cdn' /'protected'
# from facebook_prj.storages.conf import * #noqa



STORAGES = {
    "default": {
        "BACKEND": "facebook_prj.storages.backends.MediaStorage",
    },
    'staticfiles':{
        "BACKEND": "facebook_prj.storages.backends.StaticStorage",
    }
}

# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.s3.S3Storage",
#     },
#     'staticfiles':{
#         "BACKEND": "storages.backends.s3.S3Storage",
#     }
# }



PWA_APP_NAME = 'Nnekkie - Eco-Friendly Social Learning'
PWA_APP_DESCRIPTION = "A sustainable and interactive platform for learning, offering courses, ebooks, and monetization with a focus on eco-conscious education."
PWA_APP_THEME_COLOR = '#FF5733'  # Example Nnekkie primary color
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': '/static/images/nk.png',
        'sizes': '160x160'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/images/nk.png',
        'sizes': '160x160'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/nk.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'
PWA_APP_SHORTCUTS = [
    {
        'name': 'Mart',
        'url': '/product/',
        'description': 'Nnekkie Mart'
    }
]
PWA_APP_SCREENSHOTS = [
    {
      'src': '/static/images/nk.png',
      'sizes': '750x1334',
      "type": "image/png"
    }
]



# EMAIL_BACKEND = 'django_ses.SESBackend'
# # AWS-SES_REGION_NAME = ''





