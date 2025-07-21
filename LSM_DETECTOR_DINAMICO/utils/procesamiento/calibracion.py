import math

def mano_a_distancia(landmarks):
    # Calcula la distancia aproximada de la mano a la cámara usando landmarks específicos
    # Por ejemplo, usando la distancia entre muñeca (0) y el dedo medio (9)
    x1, y1 = landmarks[0][0], landmarks[0][1]
    x2, y2 = landmarks[9][0], landmarks[9][1]
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    # Esta distancia es relativa, puedes calibrarla con pruebas reales
    return distancia

def mano_centrada(landmarks, threshold=0.1):
    # Determina si la mano está suficientemente centrada en el frame
    # Usamos la coordenada x del landmark muñeca (0) y la comparamos con el centro (0.5)
    x_centro = landmarks[0][0]
    return abs(x_centro - 0.5) < threshold
