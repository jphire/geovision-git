python manage.py reset viz
# drop predefined indexes to speed up importing
psq -c 'DROP INDEX "viz_blast_read_id";
	DROP INDEX "viz_blast_read_id_like";
	DROP INDEX "viz_blast_db_entry_id";
	DROP INDEX "viz_blast_db_entry_id_like";' || exit 1
time bash import_all_others.sh || exit 1
time bash import_all_samples.sh || exit 1
time bash import_all_db.sh || exit 1
time bash import_all_blast.sh || exit 1
time psq -c 'CREATE INDEX "viz_blast_read_id" ON "viz_blast" ("read_id");
	CREATE INDEX "viz_blast_db_entry_id" ON "viz_blast" ("db_entry_id");
	CREATE INDEX "viz_blast_bitscore" ON "viz_blast" ("bitscore");
	CREATE INDEX "viz_blast_evalue" ON "viz_blast" ("error_value");

	ANALYZE viz_read;
	ANALYZE viz_dbentry;
	ANALYZE viz_blast;
	ANALYZE viz_dbuniprotecs;
	ANALYZE viz_enzymename;'
