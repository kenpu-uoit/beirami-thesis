import psycopg2 as pg
import random
from Crypto.PublicKey import RSA
import hashlib
import datetime
import time

class User:
    def __init__(self, username):
        self.username = username
        self.key = RSA.generate(1024)
        self.pubkey = self.key.publickey().exportKey()

    def sign(self, data):
        sig = self.key.sign(data, 0)
        return sig[0]

    def verify(self, data, sig):
        return self.key.verify(data, (sig,))

def uhash(**K):
    m = hashlib.md5()
    for k in sorted(K.keys()):
        m.update(str(k).encode('utf8'))
        m.update(str(K[k]).encode('utf8'))
    return m.digest() 

# Append a million records into the timeline.
# 10% will be deletions
# 10% will be updates

M = int(1E4)

def append_tl(db, user, total_ops=1*M):
    cursor = db.cursor()
    prev_sig = ""
    start = time.time()
    print("iter,duration")
    for i in range(total_ops):
        r_id = i
        c = random.randint(0, 100)
        deleted = False
        data = uhash(r_id=r_id,
                c=c,
                deleted=deleted,
                prev_sig=prev_sig)
        sig = user.sign(data)
        cursor.execute("insert into tl(r_id, c, deleted, sig) values (%s,%s,%s, %s)",
                (r_id, c, deleted, sig))
        prev_sig = sig
        if i % 100 == 0 and i > 0:
            db.commit()
            duration = time.time() - start
            print("%d,%.2f" % (i, duration))
            start = time.time()
    db.commit()

user = User("username")
db = pg.connect(dbname="", port=5433)
append_tl(db, user)
