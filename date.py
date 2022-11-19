import datetime
import re

def minimum(s):
    l=[0,15,30,45,60]
    m=100
    x=0
    for i in l:
        if m > abs(i-s):
            x=i-s
            m=abs(i-s)
    return x

def date(s):
    try:
        match = re.search(r'\d{2}-\d{2}-\d{4}', str(s))
        if match:
            date = datetime.datetime.strptime(match.group(), '%d-%m-%Y').date()
            if (date-datetime.date.today()).days in range(1,30):
                return date
            else:
                return None
    except ValueError:
        return None
    return None

def times(s):
    try:
        match = re.search(r'\d{2}:\d{2}:\d{2}', str(s))
        if match:
            time = datetime.datetime.strptime(match.group(), '%H:%M:%S').time()
            if time:
                if time.minute % 15 !=0:
                    m=minimum(int(time.minute))
                    time=(datetime.datetime.combine(datetime.datetime.today(), time) + datetime.timedelta(minutes=m)).time()
                return time
    except ValueError:
        return None
    return None

