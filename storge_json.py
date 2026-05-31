import json 
import sys
import os
from class_launcher import Proyecto

if getattr(sys, 'frozen', False):
    ruta_base = os.path.dirname(sys.executable)
else:
    ruta_base = os.path.dirname(os.path.abspath(__file__))

CARPETA_DATA = os.path.join(ruta_base, "data")
os.makedirs(CARPETA_DATA, exist_ok=True)

RUTA_PROYECTOS = os.path.join(CARPETA_DATA, "proyectos.json")

def guardar_proyecto(proyectos):

    proyectos_dict = [proyecto.a_diccionario() for proyecto in proyectos]

    # 2. Sobrescribimos el archivo con la lista completa y actualizada
    with open(RUTA_PROYECTOS, "w", encoding="utf-8") as f:
        json.dump(proyectos_dict, f, indent=4, ensure_ascii=False)


def cargar_proyectos():
    proyecto_lista = []
    try:
        with open(RUTA_PROYECTOS, "r", encoding="utf-8") as f:

            proyectos = json.load(f)

            for p_dict in proyectos:
                proyecto_objeto = Proyecto.desde_diccionario(p_dict)
                proyecto_lista.append(proyecto_objeto)
    
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error cargando datos: {e}")
        proyecto_lista = []

    return proyecto_lista