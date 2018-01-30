all: load timeline test

timeline:
	python make_mycampus_timeline.py

clean:
	echo "drop schema if exists am_thesis cascade" | psql

load:
	psql < csci_201801.dump
	psql < make_schedule.sql

test:
	python test.py
	echo "select * from am_thesis.system_snapshots" | psql
