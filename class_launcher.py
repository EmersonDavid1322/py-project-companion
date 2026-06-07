class Proyecto:
    def __init__(self, nombre, ruta,ev):
        self.nombre = nombre
        self.ruta = ruta
        self._entorno_virtual = ev

    def a_diccionario(self):
        return{
            "nombre": self.nombre,
            "ruta": self.ruta,
            "entorno": self._entorno_virtual
        }
    
    def __str__(self):
        return f"| {self.nombre} | \n| Entorno: {self._entorno_virtual} |\nRuta: {self.ruta}\n"
    
    def __repr__(self):
        return f"Proyecto(nombre='{self.nombre}', ruta='{self.ruta}', ev='{self._entorno_virtual}')"
    
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
    
    @property
    def entorno_virtual(self):
        if self._entorno_virtual == None:
            return "No configurado"
        return self._entorno_virtual

    @entorno_virtual.setter
    def entorno_virtual(self, ev):
        if not isinstance(ev, str) and ev != None:
            raise ValueError("Solo se permite formato str en ev.")
        self._entorno_virtual = ev