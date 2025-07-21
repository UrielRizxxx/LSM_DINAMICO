class EstabilidadMano:
    def __init__(self, umbral=5):
        self.historial = []
        self.umbral = umbral
        self.ultima = None

    def verificar(self, prediccion):
        self.historial.append(prediccion)
        if len(self.historial) > self.umbral:
            self.historial.pop(0)

        if self.historial.count(prediccion) == self.umbral and prediccion != self.ultima:
            self.ultima = prediccion
            return True
        return False
