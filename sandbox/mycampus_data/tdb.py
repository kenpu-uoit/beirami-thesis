SYSTEM_SNAPSHOTS = "system_snapshots"

SCHEMA = 'am_thesis'

def name(x):
    return "%s.%s" % (SCHEMA, x)

def basename(x):
    return "%s__base" % x

def timelinename(x):
    return "%s__timeline" % x

def get_timeline_name(relname):
    return "%s__t" % relname

def get_id(db):
    c = db.cursor()
    c.execute("select nextval('%s')" % name('id'))
    result = c.fetchone()[0]
    c.close()
    return result

def get_attributes(db, table):
    c = db.cursor()
    c.execute('select * from %s limit 1' % name(table))
    result = [col.name for col in c.description]
    c.close()
    return result

def create_snapshot(db, relname, timestamp):
    id = get_id(db)
    snapshot_name = "%s__%s" % (relname, id)
    attrs = [x for x in get_attributes(db, basename(relname)) if not x == "id"]

    c = db.cursor()

    #
    # Create snapshot table
    #

    first_value_clause = ",\n".join(
            "first_value({c}) over w as {c}".format(c=x) for x in attrs)

    sql = """
            create table if not exists {snapshot_name} as
            select * from (
                select
                    id,
                    {latest_attributes},
                    first_value(__flag__) over w as flag
                    from {timeline_table}
                    where __t__ <= %s
                    window w as (partition by id order by __t__ desc)) T
            """.format(snapshot_name=name(snapshot_name),
                    timeline_table=name(timelinename(relname)),
                    latest_attributes=first_value_clause)
    c.execute(sql, [timestamp])

    #
    # Record the snapshot
    #
    c.execute("insert into am_thesis.system_snapshots values(%s,%s,%s)",
            (snapshot_name, relname, timestamp))

    db.commit()

