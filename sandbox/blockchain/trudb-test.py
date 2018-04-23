import trudb
import psycopg2 as pg

key = trudb.make_key()
db = pg.connect(dbname="kenpu", port=5433)
