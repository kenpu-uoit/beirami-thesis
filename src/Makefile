.PHONY: all init_db append_tl snapshot

init_db:
	psql < sql/init-db.sql
	mkdir -p ./output

append_tl:
	PYTHONPATH=./python python python/append-tl.py | tee output/append_time.csv

snapshot:
	PYTHONPATH=./python python python/snapshot.py

clean:
	rm -rf ./output
