import psycopg2 as pg
import os
import datetime

INSERTED = 0
UPDATED = 1
DELETED = 2

def init_db(flush=False):
    db = pg.connect(dbname=os.environ.get('USER'))
    if flush:
        c = db.cursor()
        c.execute("""
            create table am_thesis.schedule__timeline as
            select nextval('am_thesis.id') as __key__,
                   S.*,
                   current_timestamp as __t__,
                   0 as __flag__
                   from am_thesis.schedule__base S
                   limit 0
            """)
        c.execute("alter table am_thesis.schedule__timeline add primary key (__key__)")
        db.commit()
    return db

def get_schedule_attributes(db):
    c = db.cursor()
    c.execute('select * from am_thesis.schedule__base limit 1')
    result = [col.name for col in c.description]
    c.close()
    return result

def get_offers(db):
    c = db.cursor()
    c.execute("""
        select distinct semester, code
        from am_thesis.schedule__base
    """)
    offers = c.fetchall()
    c.close()
    return offers

def get_offer_tuples(db, offer):
    c = db.cursor()
    (semester, code) = offer
    c.execute("""
        select * from am_thesis.schedule__base
        where semester=%s and code=%s
    """, (semester, code))
    result = c.fetchall()
    c.close()
    return result

class Clock(object):
    def __init__(self):
        self.counter = datetime.datetime(2018, 1, 1)
    def get_next(self):
        now = self.counter
        self.counter += datetime.timedelta(days=1)
        return now

def insert_timeline(db, tuples, t, flag):
    c = db.cursor()

    attr = get_schedule_attributes(db)

    insert_query = """
        insert into am_thesis.schedule__timeline
        values (nextval('am_thesis.id'), %s)
    """ % ",".join("%s" for i in range(len(attr) + 2))

    for row in tuples:
        values = list(row) + [t, flag]
        c.execute(insert_query, values)

    db.commit()


if __name__ == '__main__':
    db = init_db(True)
    clock = Clock()
    for offer in get_offers(db):
        t = clock.get_next()

        print("Creating (%s) at %s" % (offer, t))

        tuples = get_offer_tuples(db, offer)
        insert_timeline(db, tuples, t, flag=INSERTED)
