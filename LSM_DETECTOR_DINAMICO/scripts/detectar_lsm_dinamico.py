import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import pyttsx3
import time
from collections import deque
import threading
import queue
from utils.procesamiento.estabilidad import EstabilidadMano

# ======== Cargar modelo y etiquetas ==========
model = tf.keras.models.load_model("models/modelo_lsm_lstm.keras")
label_dict = np.load("models/labels_lstm.npy", allow_pickle=True).item()

# ======== Inicializar MediaPipe ==========
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# ======== Configuración del sintetizador de voz ==========
voz_queue = queue.Queue()
engine = pyttsx3.init()

def hilo_voz():
    while True:
        mensaje = voz_queue.get()
        if mensaje is None:
            break
        engine.say(mensaje)
        engine.runAndWait()

thread_voz = threading.Thread(target=hilo_voz, daemon=True)
thread_voz.start()

# ======== Variables de control ==========
cap = cv2.VideoCapture(0)
secuencia_longitud = 30
frames = deque(maxlen=secuencia_longitud)
estabilidad = EstabilidadMano(umbral=5)
ultima_sena = ""
tiempo_ultima = 0

# ======== Bucle principal ==========
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Extraer landmarks (x, y, z) por punto
        landmarks = []
        for lm in hand_landmarks.landmark:
            landmarks.extend([lm.x, lm.y, lm.z])
        frames.append(landmarks)

        # Si hay suficientes frames, hacer predicción
        if len(frames) == secuencia_longitud:
            entrada = np.array(frames).reshape(1, secuencia_longitud, -1)
            pred = model.predict(entrada, verbose=0)[0]
            clase = np.argmax(pred)
            confi = pred[clase]

            if confi > 0.65:
                nombre = label_dict[clase]

                if estabilidad.verificar(nombre):
                    cv2.putText(frame, f"{nombre} ({confi:.2f})", (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    # Solo hablar si cambia la seña o han pasado 2 segundos
                    if nombre != ultima_sena or time.time() - tiempo_ultima > 2:
                        voz_queue.put(nombre)
                        ultima_sena = nombre
                        tiempo_ultima = time.time()
            else:
                cv2.putText(frame, "No confiable", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        cv2.putText(frame, "No se detecta mano", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Detección LSM Dinámica", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ======== Liberar recursos ==========
cap.release()
voz_queue.put(None)
thread_voz.join()
cv2.destroyAllWindows()
