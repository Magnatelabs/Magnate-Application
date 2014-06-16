import os


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = [
    ("Jimi Williams", "jimi.m.williams@gmail.com"),
    # ("Your Name", "your_email@example.com"),
]

MANAGERS = ADMINS

AUTH_USER_MODEL = 'auth.User'


if not 'DATABASE_URL' in os.environ: # fall back on local
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "magnate",
            "USER": "sergey",
            "PASSWORD": "",
            "HOST": "",
            "PORT": "",
        }
    }
else:
    import dj_database_url # heroku, postgresql
    DATABASES = {
        "default": dj_database_url.config(),
    }


# Always run tests with sqlite3 so it does not take forever.
# http://stackoverflow.com/questions/6353124/running-django-tests-with-sqlite
import sys

TESTING=False
if 'test' in sys.argv or 'test_coverage' in sys.argv: #Covers regular testing and django-coverage
    TESTING=True
    SOUTH_TESTS_MIGRATE=False
    SKIP_SOUTH_TESTS = True
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
#        'TEST_NAME': os.path.join(os.path.dirname(__file__), 'test.db'),
#        'NAME': 'mytestdatabase',
    }


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "America/New_York"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/site_media/media/"

# Absolute path to the directory static files should be collected to.
# Don"t put anything in this directory yourself; store your static files
# in apps" "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/site_media/static/"

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PACKAGE_ROOT, "static"),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = "_#w7j*v5%2$kn^@hz$n%wqrx3&i95dpnh4z9w@r1!)2znv!u14"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "account.context_processors.account",
    "pinax_theme_bootstrap.context_processors.theme",
    "zinnia.context_processors.version",
#    "zinnia.context_processors.media",
    "dashboard.contexts.magnate_user_info",
    "statistics.contexts.website_stats",
]


MIDDLEWARE_CLASSES = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "app_magnate.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "app_magnate.wsgi.application"

TEMPLATE_DIRS = [
    os.path.join(PACKAGE_ROOT, "templates"),
]

INSTALLED_APPS = [

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.comments",    # for Zinnia

    # theme
    "pinax_theme_bootstrap",
    "django_forms_bootstrap",
    
    # external
    "account",
    "avatar",
    "metron",
    "eventlog",
    "waitinglist",
    "billing",
    "brabeion",
    "analytical",
    "admin_enhancer",

    "forum",

    # project
    "app_magnate",

    #migrations
    "south",

    #created 
#    "startedQuestionnaire", (renamed)
    "social",
    "companyinfo",
    "getstartedquestions",
    "siteErrors",
    "status_awards",
    "dashboard",
    "donations",
    'tagging',          # for Zinnia
    'django_xmlrpc',    # for Zinnia
    'mptt',             # for Zinnia
    "zinnia", 
 # Zinnia (an external blogging app) MUST BE included AFTER dashboard, as dashboard overrides a Zinnia template, base.html.
    "glue_zinnia",
    "bonus_awards",
    "study",
    "statistics",
    "rewards",

]


# Note that by using this test runner to exclude particular apps, we are reverting to the pre-Django 1.5 method of test discovery
TEST_RUNNER = 'django_test_exclude.runners.ExcludeTestSuiteRunner'
TEST_EXCLUDE=[ "django.contrib", "zinnia", "account", "waitinglist", "brabeion", "analytical", "tagging"]


# Disable Django caching for now. Note that django-avatar uses django caching to cache the avatars.
# Do not keep the local memory cache, as it is unique for each process, thus might be switching back and forth between the old and the new avatars...
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'heroku-style': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'heroku-style'
        },
#        'default': {
#            'level': 'DEBUG',
#            'class': 'logging.handlers.RotatingFileHandler',
#            'filename': 'logs/mylog.log',
#            'maxBytes': 1024*1024*5, #5 MB
#            'backupCount': 5,
#            'formatter': 'standard',
#        },
#        'request_handler': {
#            'level': 'DEBUG',
#            'class': 'logging.handlers.RotatingFileHandler',
#            'filename': 'logs/django_request.log',
#            'maxBytes': 1024*1024*5, #5 MB
#            'backupCount': 5,
#            'formatter': 'standard',
#        },
    },
    'loggers': {

        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}



#Default logging below
#LOGGING = {
#    "version": 1,
#    "disable_existing_loggers": False,
#    "filters": {
#        "require_debug_false": {
#            "()": "django.utils.log.RequireDebugFalse"
#        }
#    },
#    "handlers": {
#        "mail_admins": {
#            "level": "ERROR",
#            "filters": ["require_debug_false"],
#            "class": "django.utils.log.AdminEmailHandler"
#        }
#    },
#    "loggers": {
#        "django.request": {
#            "handlers": ["mail_admins"],
#            "level": "ERROR",
#            "propagate": True,
#        },
#    }
#}

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ACCOUNT_OPEN_SIGNUP = False 
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_SIGNUP_REDIRECT_URL = "dashboard"
ACCOUNT_LOGIN_REDIRECT_URL = "dashboard"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2

WAITINGLIST_SURVEY_INVITE_FROM_EMAIL = "jolumwilliams@yoursite.com"

AUTHENTICATION_BACKENDS = [
    #"account.auth_backends.UsernameAuthenticationBackend",
    'django.contrib.auth.backends.ModelBackend'
]

MERCHANT_TEST_MODE = True         # Toggle for live transactions
if 'MERCHANT_TEST_MODE' in os.environ:
    MERCHANT_TEST_MODE = (os.environ['MERCHANT_TEST_MODE'].lower() != 'false')
MERCHANT_SETTINGS = {
    "authorize_net": {
        "LOGIN_ID" : os.environ.get('AUTHORIZE_NET_LOGIN_ID', '986FnPdX4Gz3'),
        "TRANSACTION_KEY" : os.environ.get('AUTHORIZE_NET_TRANSACTION_KEY', '898btjU9L9yUr4N3'),
        "MD5_HASH": os.environ.get('AUTHORIZE_NET_MD5_HASH', 'djsiojfeoiejfoi'),
    }
}

ZINNIA_ENTRY_BASE_MODEL='glue_zinnia.models.EntryCheck'

ELDARION_BASE_BADGE_AWARD_MODEL='status_awards.models.MagnateBadgeAward'

#This is for the ratings
#AGON_NUM_OF_RATINGS = 5
AGON_RATINGS_CATEGORY_CHOICES = {"sites.Site": {"fun": "none at all"} }


MAGNATE_PUBLIC_ENTRY_BLURB_WORD_LIMIT = 25
MAGNATE_PRIVATE_ENTRY_BLURB_WORD_LIMIT = 20

#static
MAGNATE_ICON_BY_ENTRY_TYPE = {'default': "img/img_icon16.png", 'badge': "img/img_icon16.png", 'update':"img/img_icon17.png", 'article': "img/img_icon18.png", 'donation': "img/img_icon19.png", }

#static for private posts
MAGNATE_PRIVATE_ICON_BY_ENTRY_TYPE = {'default': "img/tglogo.jpg", 'badge': "img/tglogo.jpg", 'donation': "img/tgdollar.jpg", }

# static
MAGNATE_NO_STATUS_PIC_URL = 'status_awards/no_status_badge.png'

# How frequently members can give a star rating.
# using datetime.timedelta format: days=1, seconds=3, hours=2, etc.
MAGNATE_CAN_STAR_RATE_EVERY = 'seconds=5'


#django-analytical settings
CLICKY_SITE_ID = '100664353'
CRAZY_EGG_ACCOUNT_NUMBER = '00204380'
GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-46652906-1'


from osqa_settings import *



SITE_SRC_ROOT = PROJECT_ROOT

# OSQA moduel system
MODULES_PACKAGE = 'forum_modules'
MODULES_FOLDER = os.path.join(SITE_SRC_ROOT, MODULES_PACKAGE)
DISABLED_MODULES = ['project_badges', 'updates', 'default_badges'] #'recaptcha', 'project_bages']

MODULE_LIST = filter(lambda m: getattr(m, 'CAN_USE', True), [
        __import__('forum_modules.%s' % f, globals(), locals(), ['forum_modules'])
        for f in os.listdir(MODULES_FOLDER)
        if os.path.isdir(os.path.join(MODULES_FOLDER, f)) and
           os.path.exists(os.path.join(MODULES_FOLDER, "%s/__init__.py" % f)) and
           not f in DISABLED_MODULES
])


# OSQA style; overriding our TEMPLATE_LOADERS!
TEMPLATE_LOADERS = list(template_loaders) if DEBUG else [ ('django.template.loaders.cached.Loader', template_loaders) ]

if not TESTING:      # The tests are not ready for the forum.user user model
  MIDDLEWARE_CLASSES += [
  'forum.middleware.extended_user.ExtendedUser',
  # 'forum.middleware.anon_user.ConnectToSessionMessagesMiddleware',
  #    'forum.middleware.request_utils.RequestUtils',
  #    'forum.middleware.cancel.CancelActionMiddleware',
  #    'forum.middleware.admin_messages.AdminMessagesMiddleware',
  #    'forum.middleware.custom_pages.CustomPagesFallbackMiddleware',
  #    'django.middleware.transaction.TransactionMiddleware',
  #    'forum.middleware.django_cookies.CookiePostHandlerMiddleware',
   ]

TEMPLATE_CONTEXT_PROCESSORS += [
    'forum.context.application_settings',
    'forum.user_messages.context_processors.user_messages',
]
INSTALLED_APPS += [
    'django.contrib.humanize',
]
