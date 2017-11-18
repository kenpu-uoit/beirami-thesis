.PHONY: all init_db append_tl snapshot

init_db:
	psql < sql/init-db.sql

append_tl:
	PYTHONPATH=./python python python/append-tl.py

snapshot:
	PYTHONPATH=./python python python/snapshot.py

