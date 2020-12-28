#Connection to DB
import pyodbc

server = 'DESKTOP-1BUR167\SQLEXPRESS'
db = 'DBTEST'
user = 'naverjan'
pw = 'qwe123'

def createConnection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=%s;DATABASE=%s;UID=%s+;PWD=%s' 
            %(server, db, user, pw))
        return conn
    except Exception as ex:
        print("Ha ocurrido un error al conectarse a la DB:"+ex)
