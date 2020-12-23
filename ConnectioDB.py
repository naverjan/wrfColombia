#Connection to DB

import pyodbc

def createConnection(server, database, user, password):
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};
            SERVER='+server+';
            DATABASE='+database+';
            UID='+user+';
            PWD='+password)
        return conn
    except Exception as ex:
        print("Ha ocurrido un error al conectarse a la DB:"+ex)
