import psycopg2 as pg
import random

# Append a million records into the timeline.
# 10% will be deletions
# 10% will be updates

M = int(1E6)

def append_tl(db, total_ops=1*M):
    c = db.cursor()
    for i in range(total_ops):
        c.execute("insert into tl(r_id, c, deleted) values (%s,%s,%s)",
                (i, random.randint(0, 100), False))
        if i % 1000 == 0:
            db.commit()
            print("%d" % i)
    db.commit()

db = pg.connect(dbname="", port=5433)
append_tl(db)
