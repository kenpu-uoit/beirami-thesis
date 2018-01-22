all:
	python make_mycampus_timeline.py

clean:
	echo "drop table timeline;" | psql
	echo "drop table schedule;" | psql
	echo "drop sequence id;" | psql

load:
	psql < csci_201801.dump
