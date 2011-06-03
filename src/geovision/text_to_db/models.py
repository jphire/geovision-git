from django.db import models

class BulkInserterTestDummy(models.Model):
	pass

class BulkInserterTestModel(models.Model):
	int_field = models.IntegerField()
	char_field = models.CharField(max_length=16)
	fk_field = models.ForeignKey(BulkInserterTestDummy)
