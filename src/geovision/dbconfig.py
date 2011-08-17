import os
from socket import gethostname

login_user = os.environ['USER']
RUNNING_ON_USERS = (gethostname() == 'users') 
if RUNNING_ON_USERS: 
	if login_user != 'tmtynkky':
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
	else:
		DATABASES = {
			'default': {
				'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
				'NAME': 'geovision', # Or path to database file if using sqlite3.
				'USER': login_user, # Not used with sqlite3.
				'PASSWORD': '', # Not used with sqlite3.
				'HOST': '/home/tmtynkky/geovision-postgres/',
				'PORT': '4394'
			}
		}

else: # Use a local SQLite database if not on users
	DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': 'testdb.sqlite', # Or path to database file if using sqlite3.
		'USER': '', # Not used with sqlite3.
		'PASSWORD': '', # Not used with sqlite3.
		'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
		'PORT': '' # Set to empty string for default. Not used with sqlite3.
	}
}

