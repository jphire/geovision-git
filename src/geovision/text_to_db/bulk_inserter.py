from django.db import connection
from subprocess import Popen, PIPE
from django.db.models import ForeignKey

class BulkInserter():
	CSV_DELIMITER = '^'
	@classmethod
	def db_is_postgres(cls):
		return connection.vendor == 'postgresql'

	def db_get_pk_nextval(self):
		try:
			cursor = connection.cursor()
			cursor.execute("SELECT nextval('%s_id_seq');" % self.model_class._meta.db_table)
			return cursor.fetchone()[0]
		except Exception:
			self.has_seq = False
			return 0

	def db_set_pk_nextval(self, value):
		if self.has_seq:
			connection.cursor().execute(
				"SELECT setval('%s_id_seq', %%s);" % self.model_class._meta.db_table,
				[value])

	def get_psql_argv(self):
		return ('psql', '-c',
			"COPY %s FROM STDIN DELIMITER '%s';" %
				(self.model_class._meta.db_table, self.CSV_DELIMITER))

	def __init__(self, model_class, use_postgres_if_possible=True):
		self.has_seq = True
		self.model_class = model_class
		self.use_postgres = self.db_is_postgres() and use_postgres_if_possible
		if self.use_postgres:
			self.next_id = self.db_get_pk_nextval()
			self.psql_popen = Popen(self.get_psql_argv(), shell=False, stdin=PIPE, bufsize=65536)
			self.check_psql_status()
		else:
			self.next_id = 1

	def check_psql_status(self, finished=False):
		status = self.psql_popen.poll() if not finished else self.psql_popen.wait()
		if (status is not None and not finished) or (status != 0 and finished):
			raise RuntimeError('psql subprocess died unexceptedly with code %d' % status)

	def write_to_psql(self, line):
		self.psql_popen.stdin.write(line)
		self.psql_popen.stdin.write("\n")
		self.check_psql_status()

	def get_next_id(self):
		id = self.next_id
		self.next_id += 1
		return id

	def save(self, modelobj):
		if not self.use_postgres:
			modelobj.save()
		else:
			id = self.get_next_id()
			self.write_to_psql(self.obj_to_csv(modelobj, id))
			modelobj.id = id
			

	def field_to_csv(self, modelobj, field, id):
		if field.name == 'id':
			return str(id)
		is_dict = isinstance(modelobj, dict)
		obj_dict = modelobj if is_dict else modelobj.__dict__
		if isinstance(field, ForeignKey):
			return str(obj_dict[field.name].id if is_dict else obj_dict[field.column])
		field_value = obj_dict[field.name]
		return self.escape_csv(str(field_value))

	def obj_to_csv(self, modelobj, id):
		return self.CSV_DELIMITER.join(
			(self.field_to_csv(modelobj, f, id) for f in self.model_class._meta.fields))

	@classmethod
	def escape_csv(cls, data):
		return data.replace(cls.CSV_DELIMITER, "\\" + cls.CSV_DELIMITER)

	def close(self):
		if self.use_postgres:
			self.write_to_psql("\\.")
			self.db_set_pk_nextval(self.next_id)
			self.psql_popen.stdin.close()
			self.check_psql_status(True)
