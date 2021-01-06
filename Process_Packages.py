#Procesamiento de paquete NetCDF
#Andres Verjan 07/12/2020 9:14 am

import os
import netCDF4 as nc
import numpy as np
import datetime as datetime
from datetime import timedelta
import FunctionsData as functions
import time

#dia actual
today = datetime.date.today()
idTime = today.strftime('%Y%m%d%H')

#Buscamos archivo y sacamos informacion del nombre
pathFile = "archive/%s/" %(today.strftime("%Y%m%d"))
contentDir = os.listdir(pathFile)
if len(contentDir) < 1:
    raise SystemExit

file = contentDir[0]
dateFile = file[11:24]#Sacamos la fecha del archivo
dateFormatFile = datetime.datetime.strptime(dateFile, '%Y-%m-%d_%H')#Converti
idRun = dateFormatFile.strftime('%Y%m%d%H')


print("Abriendo archivo NetCDF")
content = nc.Dataset(pathFile+file)

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
# dir = "sites/"
# if not os.path.exists(dir): os.makedirs(dir)#Si no existe la crea

def convertKelvinToCelsius(kelvin):
    return round(kelvin - 273.15, 2)

#Devuelve datetime coorespodiente a las 00 h utc Colombia
def getDatetimeInit(hourRun):
    if int(hourRun) == 0:
        lastDay = today - timedelta(days=1)
        return datetime.datetime(lastDay.year, lastDay.month, lastDay.day, 19, 00, 00000)
    else:
        return datetime.datetime(today.year, today.month, today.day, 7, 12, 00000)

def getDatetimeForHour(hour, hourRun):
    date = getDatetimeInit(hourRun)
    return date + timedelta(hours=hour)

#De acuerdo a la hora Colombia obtenemos hora UTC
def getHourUTC(hour):
    date = getDatetimeForHour(hour, dateFormatFile.hour)
    dateUTC = date + timedelta(hours=5)
    return dateUTC.hour

##Variables y arreglos a utilizar
position = 0
coordinates = []
dataProcess = []

#Medición de tiempo de ejecución
start_time = time.time()


# print('Creando registro de corrida de proceso')
functions.insertRunProcess(id = idRun, idStatus = 1)

print("Recolectando  informacion de las variables...")
#Recorremos la informacion de las capas
# for c2 in range(len(XLONG[0])):
for c2 in range(1):
   #Informacion de la tercera capa
#    for c3 in range(len(XLONG[0][c2])):
   for c3 in range(1):
       position += 1  
       print('Punto: ' + str(position))     
       ##Agregar informacioón para insrción de coordenadas
    #    longitude    = str(XLONG[0][c2][c3]) 
    #    latitude     = str(XLAT[0][c2][c3])
    #    row = [position, None, longitude, latitude]
    #    coordinates.append(row)       


       ##Recorremos las 121 horas
       for hour in range(len(Times)):
           dateH = getDatetimeInit(dateFormatFile.hour) if hour == 0 else getDatetimeForHour(hour, dateFormatFile.hour)
           hourUTC = getHourUTC(hour)        

           #Sacamos los variables por hora
           RAINH = str(RAINC[hour][0][c2][c3])
           Q2H = str(Q2[hour][0][c2][c3])
           T2H = str(convertKelvinToCelsius(T2[hour][0][c2][c3]))
           U10H = str(U10[hour][0][c2][c3])
           V10H = str(V10[hour][0][c2][c3])
           SWDOWNH = str(SWDOWN[hour][0][c2][c3])
           PSFCH = str(PSFC[hour][0][c2][c3])
           SSTH = str(SST[hour][0][c2][c3])
           CLDFRAH = str(CLDFRA[hour][0][c2][c3] )


           ##Arreglo por información
           rowData = [idRun, functions.IDMODEL, idTime, position, dateH.year, dateH.month, dateH.day, dateH.hour, RAINH, Q2H, T2H, U10H, V10H, SWDOWNH, PSFCH, SSTH, CLDFRAH]           
           dataProcess.append(rowData)
    

##Inserción de coordenadas
# print('Insertando coordenadas')
# functions.insertCoordinates(coordinates)

##Inserción de registros
print('Insertando información de variables')
functions.insertDataProcess(dataProcess)

#medicion de tiempo en minutos
minutesExe = round((time.time() - start_time)/60, 2)
print('El tiempo de ejecución en minutos es %s' %(minutesExe))
