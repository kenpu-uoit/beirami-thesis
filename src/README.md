# Timeline Database

## Makefile

The makefile initializes the database, generates data and finally measures the performance of creating the most updated snapshots.
It has the following targets:

- `init_db`: initializes an empty database.  It will delete any existing data.
- `append_tl`: will append large number of tuples into the database.
- `snapshot`: will repeatedly generate snapshots at different stages, and it reports the time it takes to construct the snapshots. It will generate a `runtime.png` plot of the time it takes with increasing ranges.
