import cv2
import numpy as np
import os
import mediapipe as mp
from datetime import datetime

# Variables
seña = input("Nombre de la seña: ").strip().lower()
ruta_guardado = os.path.join("data", seña)
os.makedirs(ruta_guardado, exist_ok=True)

# Inicializa MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Inicializa captura de cámara
cap = cv2.VideoCapture(0)

secuencia = []
grabando = False
contador = 0

print("Presiona 's' para iniciar la grabación de una secuencia de 30 frames.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Procesar imagen
    imagen = cv2.flip(frame, 1)
    img_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    resultados = hands.process(img_rgb)

    if resultados.multi_hand_landmarks:
        for mano in resultados.multi_hand_landmarks:
            mp_drawing.draw_landmarks(imagen, mano, mp_hands.HAND_CONNECTIONS)

        # Extraer landmarks
        landmarks = []
        for punto in resultados.multi_hand_landmarks[0].landmark:
            landmarks.extend([punto.x, punto.y, punto.z])

        if grabando:
            secuencia.append(landmarks)
            contador += 1
            cv2.putText(imagen, f"Grabando ({contador}/30)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            if contador == 30:
                nombre_archivo = os.path.join(ruta_guardado, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.npy")
                np.save(nombre_archivo, np.array(secuencia))
                print(f"[✔] Secuencia guardada: {nombre_archivo}")

                # Reset
                grabando = False
                secuencia = []
                contador = 0
        else:
            cv2.putText(imagen, f"Presiona 's' para grabar", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Recolector de Señales LSM", imagen)
    tecla = cv2.waitKey(1)

    if tecla & 0xFF == ord('s') and not grabando:
        print("[▶] Iniciando grabación...")
        grabando = True
        secuencia = []
        contador = 0
    elif tecla & 0xFF == ord('q'):
        print("[🚪] Cerrando...")
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
