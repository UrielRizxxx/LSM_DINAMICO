import os

carpeta_data = "data"

archivos_vacios = []

for clase in os.listdir(carpeta_data):
    ruta_clase = os.path.join(carpeta_data, clase)
    for archivo in os.listdir(ruta_clase):
        ruta_archivo = os.path.join(ruta_clase, archivo)
        if os.path.getsize(ruta_archivo) == 0:
            archivos_vacios.append(ruta_archivo)

if archivos_vacios:
    print("Se encontraron archivos vacíos o corruptos:")
    for archivo in archivos_vacios:
        print(f"🗑 Eliminando: {archivo}")
        os.remove(archivo)
    print("\n✅ Archivos vacíos eliminados correctamente.")
else:
    print("✅ No se encontraron archivos vacíos.")
