import datetime
from sql import fetch

def schedule_bfr(dt,tm):
    x=tm
    while True:
        try:
            x=(datetime.datetime.combine(datetime.datetime.today(), x) + datetime.timedelta(minutes=-15))
            if x.date() != datetime.datetime.today().date():
                return False
            x=x.time()
            res=fetch(f"SELECT * FROM list WHERE date='{dt}'AND time='{x}'")
            if len(res)==0:
                return x
        except ValueError:
            return False


def schedule_afr(dt,tm):
    x=tm
    while True:
        try:
            x=(datetime.datetime.combine(datetime.datetime.today(), x) + datetime.timedelta(minutes=15))
            if x.date() != datetime.datetime.today().date():
                return False
            x=x.time()
            res=fetch(f"SELECT * FROM list WHERE date='{dt}'AND time='{x}'")
            if len(res)==0:
                return x
        except ValueError:
            return False

def arr(dt,tm):
    bfr=schedule_bfr(dt,tm)
    afr=schedule_afr(dt,tm)
    l=[]
    if bfr:
        l.append(bfr)
    if afr:
        l.append(afr)
    return l