import psycopg2 as pg
from time import time

def timeit(f, *args):
    start = time()
    f(*args)
    duration = time() - start
    return duration

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
from matplotlib import pyplot as pl

db = pg.connect(dbname="", port=5433)
c = db.cursor()
c.execute('select max(op_id) from tl')
max_op_id = c.fetchone()[0]
n = 100
runtime = []
for i in range(n):
    delete_snapshot(db)
    end_op_id = max_op_id // n * i
    x = timeit(create_snapshot, db, end_op_id)
    runtime.append(x)
    print(i, x)

pl.figure()
pl.plot(runtime)
pl.savefig('runtime.png')


