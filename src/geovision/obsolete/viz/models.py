class Result(models.Model): # Query_seq_id Target_seq_id Evident_type E.C._number p_value Bit_score
	read = models.CharField(max_length=64)
	db_entry = models.CharField(max_length=32)
	evident_type = models.CharField(max_length=2)
	ec_number = models.CharField(max_length = 32)
	error_value = models.FloatField()
	bitscore = models.FloatField()
