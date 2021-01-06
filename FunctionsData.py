import numpy as np
import ConnectionDB as Connection

''' Constantes '''
IDMODEL = 6


def insertCoordinates(params):
    try:
        conn = Connection.createConnectionSQLServer()
        with conn.cursor() as cursor:
            query = "INSERT INTO cc_locationCol (id, code, longitude, latitude) VALUES (?,?,?,?)"
            cursor.executemany(query, params)
        print('Coordenadas insertadas correctamentes')        
    except Exception as exc:
        print('Ocurrio un error al realizar la inserción '+ str(exc))
    finally:
        conn.close()


def insertRunProcess(id, idStatus):
    try:
        conn = Connection.createConnectionSQLServer()
        with conn.cursor() as cursor:
            query = "INSERT INTO cc_run (id, idModel, idStatus) VALUES (?,?,?)"
            cursor.execute(query, (id, IDMODEL, idStatus))
        print("Se inserto el registro de corrida del proceso")
    except Exception as exc:
        print("Ocurrio un error al insertar la corrida del proceso: " + str(exc))
    finally:
        conn.close()


def insertDataProcess(data):
    try:
        conn = Connection.createConnectionSQLServer()
        with conn.cursor() as cursor:
            query = "INSERT INTO cc_JMWrfColombia (idTime, idModel, idRun, idLocation, year, month, day, hour, rain, specificHumidity, temperature, zonalWind, southernWind, incidentRadiation, pressureSurface, seaSurfaceTemp, cloudFraction) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            cursor.executemany(query, data)
        print("Se inserto correctamente la información de las variables")
    except Exception as exc:
        print("Ocurrio un error al insertar la información de las variables: " + str(exc))
    finally:
        conn.close()
