#Procesamiento de paquete NetCDF
#Andres Verjan 07/12/2020 9:14 am

import os
import netCDF4 as nc
import numpy as np
from datetime import date
from datetime import datetime
from datetime import timedelta
import ConnectionDB

#dia actual
today = date.today()

#Paquete de las 00 horas
#pathFile = "WRF/wrfout_d01_"+str(today)+"_00.surface.nc.zip"

pathFile = "archive/paquete_completo.surface.nc"

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
    return datetime(today.year, today.month, today.day, 19, 00, 00000)

def getDatetimeForHour(hour):
    date = getDatetimeInit()
    return date + timedelta(hours=hour)

#De acuerdo a la hora Colombia obtenemos hora UTC
def getHourUTC(hour):
    date = getDatetimeForHour(hour)
    dateUTC = date + timedelta(hours=5)
    return dateUTC.hour

print("Recolectando  informacion de las variables...")
#Recorremos la informacion de las capas
#for c2 in range(len(lon[0])):
for c2 in range(1):
   #Informacion de la tercera capa
   #for c3 in range(len(XLONG[0][c2])):
   for c3 in range(1):
       #Coordenada
       coordinate = str(XLONG[0][c2][c3]) + str(XLAT[0][c2][c3])
       print('Creando archivo para la coordenada {}'.format(coordinate))
       #Creamos el archivo
       file = open(dir +"prueba.txt", "w")
       file.write("YY,MM,DD,HH,HF,RAINC,Q2,T2,U10,V10,SWDOWN,PSFC,SST,CLDFRA"+ os.linesep)

       ##Recorremos las 121 horas
       for hour in range(len(Times)):
           dateH = getDatetimeInit() if hour == 0 else getDatetimeForHour(hour)
           hourUTC = getHourUTC(hour)

           #Sacamos los variables por hora
           RAINH = RAINC[hour][0][c2][c3]
           Q2H = Q2[hour][0][c2][c3]
           T2H = convertKelvinToCelsius(T2[hour][0][c2][c3])
           U10H = U10[hour][0][c2][c3]
           V10H = V10[hour][0][c2][c3]
           SWDOWNH = SWDOWN[hour][0][c2][c3]
           PSFCH = PSFC[hour][0][c2][c3]
           SSTH = SST[hour][0][c2][c3]
           CLDFRAH = CLDFRA[hour][0][c2][c3]

           #Escribimos los valores por hora
           file.write(str(dateH.year)+","+str(dateH.month)+","+str(dateH.day)+","+str(dateH.hour)+","+str(hourUTC)+","+str(RAINH)+","+str(Q2H)+","+str(T2H)+","+str(U10H)+","+str(V10H)+","+str(SWDOWNH)+","+str(PSFCH)+","+str(SSTH)+","+str(CLDFRAH)+ os.linesep)

       #Cerramos el archivo
       file.close()


