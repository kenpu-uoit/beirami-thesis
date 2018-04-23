from Crypto.PublicKey import RSA

def make_key():
    return RSA.generate(1024)


class TrudbAccess:
    def __init__(self, db, key):
        self.key = key
        self.pk = key.publickey().exportKey()
        self.db = db
        self.ent_id = register_entity(self.pk)

    def start(self):
        self.rolling_hash = new_rolling_hash(get_current_hash(db))
        self.tx_id = new_tx_id()

    def insert(self, row_id, data):
        db_insert("timeline", 
                tx_id=self.tx_id, 
                row_id=row_id, 
                deleted=False, 
                data=data)
        self.update_rolling_hash(row_id, False, data)

    def update(self, row_id, data):
        return self.insert(row_id, data)

    def delete(self, row_id):
        db_insert("timeline",
                tx_id=self.tx_id,
                row_id=row_id,
                deleted=True,
                data=None)
        self.update_rolling_hash(row_id, True)

    def commit(self):
        db_insert("signatures",
                tx_id=self.tx_id,
                hash=self.rolling_hash,
                sig=sign(self.rolling_hash, self.key),
                pubkey=self.pk)
        db.commit()

    def rollback(self):
        db.rollback()

    def snapshot(self, table, t):
        ss_name = "snapshot_%s" % t
        if table_exists(self.db, ss_name):
            raise Exception("Already exists")
        else:
            sql = """
                  create table {name} as
                  select * from (
                      select row_id, 
                             first_value(data) over w as data,
                             first_value(deleted) over w as deleted,
                             (max(tx_id) over w) - (min(tx_id) over w) + 1 as freq,
                      from timeline
                      where tx_id <= %s
                  """.format(name=ss_name)
            cursor = db.cursor()
            cursor.execute(sql, [t])
            raise Exception("How do we sign the snapshot?")

class TrudbVerify:
    def __init__(self):
        pass

    def verifyTimeline(self, table, t):
        pass

    def verifySnapshot(self, snapshot):
        pass


