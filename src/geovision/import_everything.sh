python manage.py reset viz meta
# drop predefined indexes to speed up importing
psq -ac 'DROP INDEX "viz_blast_read_id";
	DROP INDEX "viz_blast_read_id_like";
	DROP INDEX "viz_blast_db_entry_id";
	DROP INDEX "viz_blast_db_entry_id_like";
	DROP INDEX "viz_blastecs_db_entry_id_like";
	ALTER TABLE viz_dbuniprotecs DROP CONSTRAINT viz_dbuniprotecs_db_id_fkey;
	;' || exit 1
time ./import_all_enzyme.sh || exit 1
time ./import_all_samples.sh || exit 1
time ./import_all_db.sh || exit 1
time ./import_all_blast.sh || exit 1
time ./import_all_ecs.sh || exit 1
time psq -1ac "CREATE INDEX viz_blast_read_id ON viz_blast (read_id) WITH (fillfactor = 100);
CREATE INDEX viz_blast_db_entry_id ON viz_blast (db_entry_id) WITH (fillfactor = 100);
CREATE INDEX viz_blast_bitscore ON viz_blast (bitscore) WITH (fillfactor = 100);
CREATE INDEX viz_blast_evalue ON viz_blast (error_value) WITH (fillfactor = 100);
CREATE INDEX viz_dbuniprotecs_ec ON viz_dbuniprotecs(ec) WITH (fillfactor = 100) WHERE ec != '?';
CREATE INDEX viz_blastecs_bitscore ON viz_blastecs (bitscore) WITH (fillfactor = 100);
CREATE INDEX viz_blastecs_ec ON viz_blastecs (ec) WITH (fillfactor=100);

	ANALYZE viz_read;
	ANALYZE viz_dbentry;
	ANALYZE viz_blast;
	ANALYZE viz_dbuniprotecs;
	ANALYZE meta_enzymename;"
psq -ac "
INSERT INTO viz_blastecs (ec, db_entry_id, bitscore, error_value) 
SELECT e.ec, b.db_entry_id, MAX(b.bitscore), MIN(b.error_value) 
FROM viz_dbuniprotecs e 
INNER JOIN viz_blast b ON (b.db_entry_id = e.db_id) 
WHERE e.ec != '?' AND b.database_name = 'uniprot' 
GROUP BY e.ec, b.db_entry_id;
ANALYZE viz_blastecs;" 
