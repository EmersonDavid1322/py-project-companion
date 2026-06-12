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

    def __str__(self):
        return f"| Fecha: {self.timestamp} |\n| Acción: {self.accion} |\n| Descricipción: {self.descripcion} |\n"

    @classmethod
    def desde_diccionario(cls, dicc):
        return cls(
            timestamp=dicc["timestamp"],
            accion=dicc["accion"],
            descripcion=dicc["descripcion"]
        )
