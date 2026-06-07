class Proyecto:
    def __init__(self, nombre, ruta, ev, git_carpeta):
        self.nombre = nombre
        self.ruta = ruta
        self._entorno_virtual = ev
        self._git_carpeta = git_carpeta

    def a_diccionario(self):
        return{
            "nombre": self.nombre,
            "ruta": self.ruta,
            "entorno": self._entorno_virtual,
            "git_carpeta": self._git_carpeta
        }
    
    def __str__(self):
        return f"| {self.nombre} | \n| Entorno: {self._entorno_virtual} |\nRuta: {self.ruta}\nCapeta git: {self._git_carpeta}\n"
    
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
            ev=diccionario.get("entorno"),
            git_carpeta=diccionario.get("git_carpeta", None)
        )
    
    @property
    def entorno_virtual(self):
        if self._entorno_virtual is None:
            return "No configurado"
        return self._entorno_virtual
    
    @property
    def git_carpeta(self):
        if self._git_caperta is None:
            return "No configurado"
        return self._git_carpeta

    @entorno_virtual.setter
    def entorno_virtual(self, ev):
        if not isinstance(ev, str) and ev != None:
            raise ValueError("Solo se permite formato str en ev.")
        self._entorno_virtual = ev

    @git_carpeta.setter
    def git_carpeta(self, git_carpeta):
        if not isinstance(git_carpeta, str) and git_carpeta != None:
            raise ValueError("Solo se permite formato str en la git carpeta.")
        self._git_carpeta = git_carpeta