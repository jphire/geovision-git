# encoding= utf-8
# Django settings for geovision project.
import os
import sys
from socket import gethostname

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_FILE_PATH = PROJECT_PATH + '/text_to_db/testfiles/'


DEBUG = True
TEMPLATE_DEBUG = DEBUG

MANAGERS = (
		  ('Tuomas Tynkkynen', 'tuomas.tynkkynen@helsinki.fi'),
		  ('Lasse Tyrväinen', 'lasse.tyrvainen@helsinki.fi'),
		  ('Janne Laukkanen', 'jjlaukka@cs.helsinki.fi'),
		  ('Aurora Tulilaulu', 'tulilaulu@gmail.com')
		 )

ADMINS = ()
DATABASES = None

LOGIN_URL = '/login'

login_user = os.environ['USER']
RUNNING_ON_USERS = (gethostname() == 'users') 
if RUNNING_ON_USERS: # Postgres settings if running on users.cs, the user/database tmtynkky is used for tests
#	pwfile = open(os.environ['HOME'] + '/.psql_password') # Read the password from the file created by wanna-postgres
#	pw = pwfile.readline().strip()
#	pwfile.close()
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
			'NAME': 'tkt_gvis', # Or path to database file if using sqlite3.
			'USER': login_user, # Not used with sqlite3.
			'PASSWORD': '', # Not used with sqlite3.
			'HOST': '/home/tkt_gvis/pg_data/',
			'PORT': '58786'
		}
	}
else: # Use a local SQLite database if not on users
	DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': PROJECT_PATH + '/testdb.sqlite', # Or path to database file if using sqlite3.
		'USER': '', # Not used with sqlite3.
		'PASSWORD': '', # Not used with sqlite3.
		'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
		'PORT': '' # Set to empty string for default. Not used with sqlite3.
	}
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Helsinki'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (os.path.join(PROJECT_PATH, 'static'),)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
					   'django.contrib.staticfiles.finders.FileSystemFinder',
					   'django.contrib.staticfiles.finders.AppDirectoriesFinder',
					   #	'django.contrib.staticfiles.finders.DefaultStorageFinder',
					   )

# Make this unique, and don't share it with anybody.
SECRET_KEY = '&-tl4g_69(uvd3dwz-k9ud5$#w4ev(g5bw8%g)7nvtgqh$cfev'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
					'django.template.loaders.filesystem.Loader',
					'django.template.loaders.app_directories.Loader',
					#	 'django.template.loaders.eggs.Loader',
					)

MIDDLEWARE_CLASSES = (
					  'django.middleware.common.CommonMiddleware',
					  'django.contrib.sessions.middleware.SessionMiddleware',
					  'django.middleware.csrf.CsrfViewMiddleware',
					  'django.contrib.auth.middleware.AuthenticationMiddleware',
					  'django.contrib.messages.middleware.MessageMiddleware',
					  )
if RUNNING_ON_USERS:
	MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INTERNAL_IPS = ('127.0.0.1',)
ROOT_URLCONF = 'geovision.urls'

TEMPLATE_DIRS = (
								 os.path.join(PROJECT_PATH, 'templates'),
				 # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
				 # Always use forward slashes, even on Windows.
				 # Don't forget to use absolute paths, not relative paths.
				 )

INSTALLED_APPS = (
				  'viz',
				  'userdb',
				  'meta',
				  'text_to_db',

				  'django.contrib.auth',
				  'django.contrib.contenttypes',
				  'django.contrib.sessions',
				  'django.contrib.sites',
				  'django.contrib.messages',
				  'django.contrib.staticfiles',
				  'django_nose',
				  # Uncomment the next line to enable the admin:
				  'django.contrib.admin',
				  # Uncomment the next line to enable admin documentation:
				  # 'django.contrib.admindocs',

				  # Uncomment this to enable Testmaker (http://ericholscher.com/blog/2008/jul/26/testmaker-002-even-easier-automated-testing-django/)
				  # 'test_utils',
				  )
AUTH_PROFILE_MODULE = "userdb.UserProfile"

if RUNNING_ON_USERS:
	INSTALLED_APPS += ('debug_toolbar',)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'class': 'django.utils.log.AdminEmailHandler'
		}
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True,
		},
	}
}

DEBUG_TOOLBAR_PANELS = (
	'debug_toolbar.panels.timer.TimerDebugPanel',
	'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
	'debug_toolbar.panels.headers.HeaderDebugPanel',
	'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
	'debug_toolbar.panels.template.TemplateDebugPanel',
	'debug_toolbar.panels.sql.SQLDebugPanel',
)

DEBUG_TOOLBAR_CONFIG = {
	'INTERCEPT_REDIRECTS': False,
	'SHOW_TOOLBAR_CALLBACK': (lambda _: True),
	'HIDE_DJANGO_SQL': True,
}
