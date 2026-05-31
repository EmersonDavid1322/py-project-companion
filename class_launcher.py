class Proyecto:
    def __init__(self, nombre, ruta,ev):
        self.nombre = nombre
        self.ruta = ruta
        self.entorno_virtual = ev

    def a_diccionario(self):
        return{
            "nombre": self.nombre,
            "ruta": self.ruta,
            "entorno": self.entorno_virtual
        }
    
    @classmethod
    def desde_diccionario(cls, diccionario):
        return cls(
            nombre=diccionario["nombre"],
            ruta=diccionario["ruta"],
            ev=diccionario["entorno"]
        )
