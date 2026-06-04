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
    
    def __str__(self):
        return f"| {self.nombre} | \n| Entorno: {self.entorno_virtual} |\nRuta: {self.ruta}\n"
    
    def __repr__(self):
        return f"Proyecto(nombre='{self.nombre}', ruta='{self.ruta}', ev='{self.entorno_virtual}')"
    
    def __eq__(self, otro):
        if not isinstance(otro, Proyecto):
            return False
        return self.nombre == otro.nombre 
    
    @classmethod
    def desde_diccionario(cls, diccionario):
        return cls(
            nombre=diccionario["nombre"],
            ruta=diccionario["ruta"],
            ev=diccionario["entorno"]
        )

