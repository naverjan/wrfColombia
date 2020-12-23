#Descarga de archivos
#Autor Andres Verjan

import os
import datetime as datetime
from  ftplib import  FTP
import ssl

#Datos dei conexion
server = 'aplicaciones.canalclima.com'
user = 'ftpUser'
password = 'S3rficorp'

def connectionFtp(serve, us, pw):
    ftp = FTP()
    ftp.connect(serve)
    ftp.login(us, pw)
    return ftp

#Validamos directorio
dir = "archive/"
if not os.path.exists(dir): os.makedirs(dir)

#fecha de hoy
dateTemp = datetime.date.today()
date = dateTemp.strftime("%Y-%m-%d") 

file = 'wrfout_d01_'+date+'_00.surface.nc.zip'

#Conexion ftp
ftp = connectionFtp(server, user, password)

#Guardamos el archivo
with open(dir+file, 'wb') as archivo:
    ftp.retrbinary('RETR /PRONOSTICOS/surface/'+file, archivo.write)

ftp.quit()






