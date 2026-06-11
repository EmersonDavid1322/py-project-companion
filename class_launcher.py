import platform
import os
import subprocess
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
#METODOS ESPECIALES 

    # METODOS ESPECIALES 
    def __str__(self):
        return f"| {self.nombre} | \n| Entorno: {self.entorno_virtual} |\nRuta: {self.ruta}\nCapeta git: {self.git_carpeta}\n"
    
    def __repr__(self):
        return f"Proyecto(nombre='{self.nombre}', ruta='{self.ruta}', ev='{self.entorno_virtual}')"
    
    def __eq__(self, otro):
        if not isinstance(otro, Proyecto):
            return False
        return self.nombre == otro.nombre 
    
    def __lt__(self, otro):
        if not isinstance(otro, Proyecto):
            return NotImplemented
        return self.nombre.lower() < otro.nombre.lower()
    
#DECORADORES
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