import psycopg2 as pg
from time import time

def timeit(f, *args):
    start = time()
    f(*args)
    duration = time() - start
    print(">> %.2f ms" % (duration * 1000))

def delete_snapshot(db):
    c = db.cursor()
    c.execute('drop table if exists snapshot')
    c.close()

def create_snapshot(db, end_op_id):
    c = db.cursor()
    c.execute('''
        CREATE TABLE snapshot AS
        SELECT * FROM (
            SELECT
                r_id,
                first_value(c) over w as c,
                first_value(deleted) over w as del,
                (max(op_id) over w) - (min(op_id) over w) + 1 as freq
            FROM tl WHERE op_id <= %s
            WINDOW w AS (PARTITION BY r_id ORDER BY op_id DESC)) T
        ''', [end_op_id])
    c.close()

import sys
db = pg.connect(dbname="")
delete_snapshot(db)
timeit(create_snapshot, db, int(sys.argv[1]))
