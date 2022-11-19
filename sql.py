import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="username",
    password="password",
    database="Appointment" )

cursor = conn.cursor(buffered=True)

def query(s):
    try:
        cursor.execute(s)
        conn.commit()
        return True
    except:
        return False


def fetch(s):
    try:
        cursor.execute(s)
        conn.commit()
        return cursor.fetchall()
    except :
        return []

