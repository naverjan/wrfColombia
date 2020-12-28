#Descarga de archivos
#Autor Andres Verjan

import os
import datetime as datetime
from  ftplib import  FTP
import time 
import zipfile
import shutil

#Datos dei conexion
server = 'aplicaciones.canalclima.com'
user = ''
password = ''

#Fecha de hoy
dateTemp = datetime.date.today()

#Conexión via FTP
def connectionFtp(serve, us, pw):
    ftp = FTP()    
    ftp.encoding = 'ISO-8859-1'    
    ftp.connect(serve)
    ftp.login(us, pw)
    return ftp

#Validamos directorio
dir = "archive/%s/" %(dateTemp.strftime("%Y%m%d"))
if not os.path.exists(dir): os.makedirs(dir)

#Obtenemos el nombre del archivo
def getNameFile():        
    date = dateTemp.strftime("%Y-%m-%d") 
    return 'wrfout_d01_'+date+'_00.surface.nc.zip'

#Extracción de zip
def extractZip(filename):
    pathFile = dir+filename
    pathExtract = dir
    fileZip = zipfile.ZipFile(pathFile, "r")
    try:
        nameFileInside = fileZip.namelist()
        pathInside = str(nameFileInside[0])        
        print('Extrayendo archivo %s' %(pathInside))
        fileZip.extractall(pwd=None, path=pathExtract)  
        print('Moviendo archivo')
        shutil.move(dir+pathInside, dir+filename.replace('.zip', ''))
        shutil.rmtree(dir+'home')
        return 'Extracción exitosa'  
    except Exception as exc:
        print(exc)

#Tiempo inicial
start_time = time.time()

file = getNameFile()
print('Archivo a descargar:'+file)

#Conexion ftp
print('Realizando conexión vía ftp')
ftp = connectionFtp(server, user, password)

#Sacamos el tamaño del archivo
size = ftp.size('/PRONOSTICOS/surface/'+file)
sizeFile = round((size / 1024))
print('El archivo encontrado pesa %s MB' %(sizeFile))
num = 0
#Guardamos el archivo
print('Descargando archivo...')
with open(dir+file, 'wb') as archivo:
    ftp.retrbinary('RETR /PRONOSTICOS/surface/'+file, archivo.write)
    
minutes = round((time.time() - start_time)/60, 2)
print('El tiempo de descarga en minutos fue: %s' %(minutes) )

print('Descomprimiendo el archivo...')
responseExtract = extractZip(file)
print(responseExtract)

print('Cerrando conexión ftp')
ftp.quit()
