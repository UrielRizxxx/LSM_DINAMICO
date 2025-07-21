import os

def menu():
    print("\n📦 LSM_DETECTOR_DINAMICO")
    print("Calibrar cámara con OpenCV")
    print("  Recolectar secuencias de señas")
    print("  Entrenar modelo LSTM")
    print("  Ejecutar detector en tiempo real")
    print("  Salir")
    return input("Selecciona una opción (1-5): ")

while True:
    opcion = menu()

    if opcion == '1':
        os.system("python scripts/calibrar_camara.py")
    elif opcion == '2':
        print("\n⚠️ Asegúrate de configurar el nombre de la seña antes de iniciar.")
        os.system("python scripts/recolectar_secuencias.py")
    elif opcion == '3':
        os.system("python scripts/entrenar_lstm.py")
    elif opcion == '4':
        os.system("python scripts/detectar_lsm_dinamico.py")
    elif opcion == '5':
        print("Saliendo del sistema... 👋")
        break
    else:
        print("❌ Opción inválida. Intenta de nuevo.")
