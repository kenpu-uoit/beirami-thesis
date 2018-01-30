import tdb
import psycopg2 as pg
import datetime

db = pg.connect(dbname='kenpu')
t = datetime.datetime.now()
t = "2018-01-05 00:00:00-05"

tdb.create_snapshot(db, 'schedule', t)
