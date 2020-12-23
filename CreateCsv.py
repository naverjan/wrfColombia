import csv
import netCDF4 as nc


path = "archive/paquete_completo.surface.nc"

num = 0
print("Abriendo archivo")
content = nc.Dataset(path)

print("Tomando coordenas")
XLONG, XLAT = content.variables["XLONG"], content.variables["XLAT"]

print("Creando archivo")
with open("prueba.csv", "wt") as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(('Posicion', 'Longitud', 'Latitud'))
    print("Recorriendo posiciones")
    for c2 in range(len(XLONG[0])):
        for c3 in range(len(XLONG[0][c2])):
            num = num + 1
            row = (num, str(XLONG[0][c2][c3]), str(XLAT[0][c2][c3]))
            writer.writerow(row)


print("Finalizado proceso de creacion de archivo")
