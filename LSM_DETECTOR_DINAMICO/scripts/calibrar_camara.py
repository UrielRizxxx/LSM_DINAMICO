import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

def mano_a_distancia(landmarks):
    # Ejemplo simple: distancia entre pulgar (4) y meñique (20)
    x1, y1 = landmarks[4].x, landmarks[4].y
    x2, y2 = landmarks[20].x, landmarks[20].y
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        distancia = mano_a_distancia(hand_landmarks.landmark)
        cv2.putText(frame, f"Distancia: {distancia:.3f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Calibrar Cámara", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
