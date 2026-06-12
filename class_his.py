from datetime import datetime

class EventoHistorial:
    def __init__(self, accion, descripcion, timestamp=None):
        self.timestamp = timestamp if timestamp else datetime.now().isoformat()
        self.accion = accion
        self.descripcion = descripcion

    def a_diccionario(self):
        return {
            "timestamp": self.timestamp,
            "accion": self.accion,
            "descripcion": self.descripcion
        }

    @classmethod
    def desde_diccionario(cls, dicc):
        return cls(
            timestamp=dicc["timestamp"],
            accion=dicc["accion"],
            descripcion=dicc["descripcion"]
        )
