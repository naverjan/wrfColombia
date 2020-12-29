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
user = 'ftpUser'
password = 'S3rficorp'

#Fecha de hoy
dateTemp = datetime.date.today()

''' Realiza la conexión vía FTP al servidor '''
def connectionFtp(serve, us, pw):
    ftp = FTP()    
    ftp.encoding = 'ISO-8859-1'#Este codificación solo es necesario en Windows
    ftp.connect(serve)
    ftp.login(us, pw)
    return ftp

#Validamos directorio
dir = "archive/%s/" %(dateTemp.strftime("%Y%m%d"))
if not os.path.exists(dir): os.makedirs(dir)

''' Retorna el nombre del archivo '''
def getNameFile():        
    date = dateTemp.strftime("%Y-%m-%d") 
    # return 'wrfout_d01_'+date+'_00.surface.nc.zip'
    return 'wrfout_d01_2020-12-27_00.surface.nc.zip'

''' Extrae un archivo por nombre de archivo
    Author: Andres Verjan
    Date: 28/12/2020 '''
def extractZipForFile(filename):
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
        print('Ocurrio un error al extraer el archivo:',exc)

''' Extrae un archivo por por ruta
    Author: Andres Verjan
    Date: 28/12/2020 '''
def extractZipForPath(path):
    contentDir = os.listdir(path)
    pathExtract = dir
    try:
        for file in contentDir:
            if os.path.isfile(os.path.join(dir, file)) and file.endswith('.zip'):
                print(dir+file)
                fileZip = zipfile.ZipFile(dir+file, "r")
                nameFileInside = fileZip.namelist()
                pathInside = str(nameFileInside[0])        
                print('Extrayendo archivo %s' %(pathInside))
                fileZip.extractall(pwd=None, path=pathExtract)  
                print('Moviendo archivo a carptea raiz')
                shutil.move(dir+pathInside, dir+file.replace('.zip', ''))
                shutil.rmtree(dir+'home')
        return 'Extracción exitosa'  
    except Exception as exc:
        print('Ocurrio un error al extraer el archivo: ',exc)

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

response = extractZipForPath(dir)
print(response)

print('Cerrando conexión ftp')
ftp.quit()
