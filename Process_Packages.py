#Procesamiento de paquete NetCDF
#Andres Verjan 07/12/2020 9:14 am

import os
import netCDF4 as nc
import numpy as np
import datetime as datetime
from datetime import timedelta
import ConnectionDB as connection


#dia actual
today = datetime.date.today()


#Paquete de las 00 horas
pathFile = "archive/%s/" %(today.strftime("%Y%m%d")) + "wrfout_d01_"+str(today)+"_00.surface.nc"

# pathFile = "archive/paquete_completo.surface.nc"

print("Abriendo archivo NetCDF")
content = nc.Dataset(pathFile)

print("Recolectando variables")
#Sacamos variables de latitud y longitud 379x379
XLONG, XLAT = content.variables["XLONG"], content.variables["XLAT"]

#Sacamos variables por la 121 horas y por las 379x379 coordenadas
Times = content.variables["Times"]  #Horas formar b 'b
RAINC  =  content.variables["RAINC"] #Lluvia
Q2 = content.variables["Q2"] #Humedad especifica
T2 = content.variables["T2"] #Temperatura
U10 = content.variables["U10"] #Viento zonal
V10 = content.variables["V10"] #Viento meridional
SWDOWN = content.variables["SWDOWN"] #Radiacion incidente
PSFC = content.variables["PSFC"] #Presion de la superficie
SST = content.variables["SST"] #Temperatura de la superficie del mar
CLDFRA = content.variables["CLDFRA"] #Fraccion de nubes


#Creamos carpeta donde se guardara la informacion de cada punto
dir = "sites/"
if not os.path.exists(dir): os.makedirs(dir)#Si no existe la crea


def convertKelvinToCelsius(kelvin):
    return round(kelvin - 273.15, 2)

#Devuelve datetime coorespodiente a las 00 h utc Colombia
def getDatetimeInit():
    return datetime.datetime(today.year, today.month, today.day, 19, 00, 00000)

def getDatetimeForHour(hour):
    date = getDatetimeInit()
    return date + timedelta(hours=hour)

#De acuerdo a la hora Colombia obtenemos hora UTC
def getHourUTC(hour):
    date = getDatetimeForHour(hour)
    dateUTC = date + timedelta(hours=5)
    return dateUTC.hour

#Obtenemos conexión
print('Realizando conexión a la base de datos')
conn = connection.createConnectionSQLServer()

coordinates = []
def createCoordinate(params):
    try:
        with conn.cursor() as cursor:
            query = "INSERT INTO cc_location (code, longitude, latitude) VALUES (?,?,?,?)"
            cursor.executemany(query, params)
        print('Coordenadas insertadas correctamentes')
    except Exception as exc:
        print('Ocurrio un error al realizar la inserción '+ exc)


position = 0

print("Recolectando  informacion de las variables...")
#Recorremos la informacion de las capas
#for c2 in range(len(lon[0])):
for c2 in range(1):
   #Informacion de la tercera capa
   #for c3 in range(len(XLONG[0][c2])):
   for c3 in range(1):
       position += 1       
       #Coordenada
       longitude    = str(XLONG[0][c2][c3]) 
       latitude     = str(XLAT[0][c2][c3])
       row = [str(position), None, str(longitude), str(latitude)]
       coordinates.append(row)       


       ##Recorremos las 121 horas
    #    for hour in range(len(Times)):
    #        dateH = getDatetimeInit() if hour == 0 else getDatetimeForHour(hour)
    #        hourUTC = getHourUTC(hour)

    #        #Sacamos los variables por hora
    #        RAINH = RAINC[hour][0][c2][c3]
    #        Q2H = Q2[hour][0][c2][c3]
    #        T2H = convertKelvinToCelsius(T2[hour][0][c2][c3])
    #        U10H = U10[hour][0][c2][c3]
    #        V10H = V10[hour][0][c2][c3]
    #        SWDOWNH = SWDOWN[hour][0][c2][c3]
    #        PSFCH = PSFC[hour][0][c2][c3]
    #        SSTH = SST[hour][0][c2][c3]
    #        CLDFRAH = CLDFRA[hour][0][c2][c3] 
    # 

print(coordinates)
createCoordinate(coordinates)   


print('Cerrando conexion a DB')
conn.close()