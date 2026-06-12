from class_his import EventoHistorial
import uuid
class Proyecto:
    def __init__(self, nombre, ruta, ev, git_carpeta, historial=None, id=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.nombre = nombre
        self.ruta = ruta
        self._entorno_virtual = ev
        self._git_carpeta = git_carpeta
        self.historial = historial if historial is not None else []

        

    def registrar_evento(self, accion, descripcion):
        nuevo_evento = EventoHistorial(accion, descripcion)
        self.historial.append(nuevo_evento)

    def a_diccionario(self):
        return {
            "id": str(self.id),
            "nombre": self.nombre,
            "ruta": self.ruta,
            "entorno": self._entorno_virtual,
            "git_carpeta": self._git_carpeta,
            "historial": [evento.a_diccionario() for evento in self.historial]
        }
    

#METODOS ESPECIALES 
    def __str__(self):
        return f"| {self.nombre} | \n| Entorno: {self.entorno_virtual} |\nRuta: {self.ruta}\nCapeta git: {self.git_carpeta}\n"
    
    def __repr__(self):
        return f"Proyecto(nombre='{self.nombre}', ruta='{self.ruta}', ev='{self.entorno_virtual}')"
    
    def __eq__(self, otro):
        if not isinstance(otro, Proyecto):
            return False
        return self.id == otro.id
    
    def __lt__(self, otro):
        if not isinstance(otro, Proyecto):
            return NotImplemented
        return self.nombre.lower() < otro.nombre.lower()
    
#DECORADORES
    @classmethod
    def desde_diccionario(cls, diccionario):
        datos_historial = diccionario.get("historial", [])
        objetos_historial = [EventoHistorial.desde_diccionario(e) for e in datos_historial]
        
        return cls(
            id=diccionario.get("id", None),
            nombre=diccionario["nombre"],
            ruta=diccionario["ruta"],
            ev=diccionario.get("entorno"),
            git_carpeta=diccionario.get("git_carpeta", None),
            historial=objetos_historial
        )
    
    @property
    def entorno_virtual(self):
        if self._entorno_virtual is None:
            return "No Hay un entorno registrado"
        return self._entorno_virtual

    @property
    def git_carpeta(self):
        if self._git_carpeta is None:
            return "No Hay un repositorio registrado"
        return self._git_carpeta

    @entorno_virtual.setter
    def entorno_virtual(self, ev):
        if ev is not None and not isinstance(ev, str):
            raise ValueError("Solo se permite formato str o None en ev.")
        self._entorno_virtual = ev

    @git_carpeta.setter
    def git_carpeta(self, git_carpeta):
        if git_carpeta is not None and not isinstance(git_carpeta, str):
            raise ValueError("Solo se permite formato str en la git carpeta.")
        self._git_carpeta = git_carpeta