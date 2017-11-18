.PHONY: all init_db append_tl

init_db:
	psql < sql/init-db.sql

append_tl:
	PYTHONPATH=./python python python/append-tl.py


