from django.db import connection
from django.db.models import ForeignKey
from subprocess import Popen, PIPE
import signal

def dict_from_kwargs(**kwargs):
	return kwargs

def sigterm_handler(signum, frame):
	raise RuntimeError('got SIGTERM')

class BulkInserter():
	CSV_DELIMITER = '$'
	@classmethod
	def db_is_postgres(cls):
		return connection.vendor == 'postgresql'

	def db_get_pk_nextval(self):
		idfields = filter(lambda f: f.name == 'id', self.model_class._meta.fields)
		if len(idfields) == 0:
			self.has_seq = False
			return 0
		try:
			cursor = connection.cursor()
			cursor.execute("SELECT nextval('%s_id_seq');" % self.model_class._meta.db_table)
			return cursor.fetchone()[0]
		except Exception:
			raise RuntimeError("should not happen, check your models!")
#			self.has_seq = False
#			return 0

	def db_set_pk_nextval(self, value):
		if self.has_seq:
			connection.cursor().execute(
				"SELECT setval('%s_id_seq', %%s);" % self.model_class._meta.db_table,
				[value])

	def get_psql_argv(self):
		return ('psql',
				'-h', connection.settings_dict['HOST'],
				'-p', connection.settings_dict['PORT'],
				'-d', connection.settings_dict['NAME'],
				'-c', "COPY %s FROM STDIN DELIMITER '%s';" % (self.model_class._meta.db_table, self.CSV_DELIMITER))

	def __init__(self, model_class, use_postgres_if_possible=True, use_dict=False):
		self.use_dict = use_dict
		self.has_seq = True
		self.model_class = model_class
		self.obj_to_csv = eval(self.obj_to_csv_code())
		self.use_postgres = self.db_is_postgres() and use_postgres_if_possible
		self.status_check_counter = 0
		if self.use_postgres:
			self.next_id = self.db_get_pk_nextval()
			self.psql_popen = Popen(self.get_psql_argv(), shell=False, stdin=PIPE, stderr=PIPE, stdout=PIPE, bufsize=8 * 2**20)
			self.check_psql_status()
		else:
			self.next_id = 1

		# Add a signal handler for TERM so that kill'ing a parser script causes it to rollback properly.
		signal.signal(signal.SIGTERM, sigterm_handler)

	def check_psql_status(self, finished=False):
		status = self.psql_popen.poll() if not finished else self.psql_popen.wait()
		if (status is not None and not finished) or (status != 0 and finished):
			for line in self.psql_popen.stdout:
				print line,
			for line in self.psql_popen.stderr:
				print line,
			raise RuntimeError('psql subprocess died unexceptedly with code %d' % status)

	def write_to_psql(self, line):
		try:
			self.psql_popen.stdin.write(line)
		except IOError:
			self.check_psql_status()
		self.status_check_counter += 1
		if self.status_check_counter >= 100000:
			self.status_check_counter = 0
			self.check_psql_status()

	def get_id(self):
		return self.next_id

	def get_next_id(self):
		id = self.next_id
		self.next_id += 1
		return id

	def save(self, modelobj):
		if not self.use_postgres:
			modelobj.save()
		else:
			self.write_to_psql(self.obj_to_csv(self, modelobj))
			

	def field_to_csv_code(self, field):
		if field.name == 'id':
			return "self.get_next_id()"
		if isinstance(field, ForeignKey):
			return "obj['%s_id']" % field.name if self.use_dict else 'obj.%s_id' % field.name
			#return str(obj_dict[field.name].id if is_dict else obj_dict[field.column])
		return "obj['%s']" % field.name if self.use_dict else 'obj.%s' % field.name

	def obj_to_csv_code(self): # return '%s^%s^%s^%s\n' % (self.next_id(), m.fieldA, m.fieldB.id)
		fields = self.model_class._meta.fields
		fmtstr = self.CSV_DELIMITER.join(('%s' for _ in fields))
		formatargs = ', '.join((self.field_to_csv_code(field) for field in fields))

		return "lambda self, obj: '%s\\n' %% (%s)" % (fmtstr, formatargs)

	@classmethod
	def escape_csv(cls, data):
		return data.replace(cls.CSV_DELIMITER, "\\" + cls.CSV_DELIMITER)

	def close(self):
		if self.use_postgres:
			self.write_to_psql("\\.\n")
			self.db_set_pk_nextval(self.next_id)
			self.psql_popen.stdin.close()
			self.check_psql_status(True)

	def rollback(self):
		try:
			self.psql_popen.send_signal(signal.SIGINT)
		except Exception:
			pass
