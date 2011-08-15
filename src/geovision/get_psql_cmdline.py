# psql.py - prints a command line suitable for running psql.
# Used by import scripts
from django.db import connection
print('psql -h %s -p %s -d %s' % (connection.settings_dict['HOST'],
	connection.settings_dict['PORT'], connection.settings_dict['NAME']))
