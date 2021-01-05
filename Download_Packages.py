#Descarga de archivos
#Autor Andres Verjan

import os
import datetime as datetime
from  ftplib import  FTP
import time 
import subprocess# Utilizaciónde 7Zip

#Datos dei conexion
server = 'aplicaciones.canalclima.com'
user = 'ftpUser'
password = 'S3rficorp'

#Fecha de hoy
dateTemp = datetime.date.today()

''' Realiza la conexión vía FTP al servidor '''
def connectionFtp(serve, us, pw):
    ftp = FTP()    
    ftp.encoding = 'ISO-8859-1'#Esta codificación solo es necesario en Windows
    ftp.connect(serve, port=0, timeout=5)
    ftp.login(us, pw)    
    return ftp

#Validamos directorio
dir = "archive/%s/" %(dateTemp.strftime("%Y%m%d"))
if not os.path.exists(dir): os.makedirs(dir)

''' Retorna el nombre del archivo '''
def getNameFile():        
    date = dateTemp.strftime("%Y-%m-%d") 
    return 'wrfout_d01_'+date+'_00.surface.nc.zip'
    # return 'wrfout_d01_2020-12-27_00.surface.nc.zip'


''' Extrae un archivo por por ruta
    Author: Andres Verjan
    Date: 28/12/2020 '''
def extractZipForPath(path):
    contentDir = os.listdir(path)
    pathExtract = dir
    try:
        for file in contentDir:
            if os.path.isfile(os.path.join(dir, file)) and file.endswith('.zip'):
                dirFile = dir + file                
                ''' Se utiliza 7zip debido que al momento de utilizar zipfile no reconoce el archivo como un .zip '''
                ziploc = "C:/Program Files/7-Zip/7z.exe" # Ubicación de .exe del programa
                cmd = [ziploc, 'e', dirFile, '-o' + pathExtract, '-r']
                subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)                                            
        return 'Extracción exitosa del archivo %s' %(file)
    except Exception as exc:
        print('Ocurrio un error al extraer el zip: ',exc)

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

downloaded = open(dir+file, 'wb')
max_attemps = 5 #5 intentos de descargar el archivo
while size != downloaded.tell():
    try:
        print("%s - Realizando descarga del archivo " % dateTemp.strftime("%d-%m-%Y %H.%M"))
        if downloaded.tell() != 0:
            ftp.retrbinary('RETR /PRONOSTICOS/surface/'+file, downloaded.write, downloaded.tell())
        else:
            ftp.retrbinary('RETR /PRONOSTICOS/surface/'+file, downloaded.write)                
    except Exception as exc:
        if max_attemps != 0:
            print("%s Ocurrio un error, realizando intento: %s\n \tTamaño del archivo es: %i > %i\n" %
                   (dateTemp.strftime("%d-%m-%Y %H.%M"), exc, size, downloaded.tell()))
            ftp = connectionFtp(server, user, password)
            max_attemps -= 1
        else:
            break
    
minutes = round((time.time() - start_time)/60, 2)
print('El tiempo de descarga en minutos fue: %s' %(minutes) )

print('Cerrando conexión ftp')
ftp.quit()

print('Descomprimiendo el archivo...')
time.sleep(120)

response = extractZipForPath(dir)
print(response)