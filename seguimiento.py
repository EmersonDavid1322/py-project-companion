import os
from pathlib import Path
from storge_json import guardar_proyecto, cargar_proyectos

def verificar_proyecto_basico(proyecto):

    try:
    
        verificacion_carpeta_proyecto = Path(proyecto.ruta)

        if verificacion_carpeta_proyecto.exists():
            existe_capeta_proyecto = True
        else:
            existe_capeta_proyecto = False

        nombres_comunes = ["venv", ".venv", "env", ".env"]

        contenido = os.listdir(proyecto.ruta)

        for elemento in contenido:
            ruta = os.path.join(proyecto.ruta, elemento)
            if elemento in nombres_comunes and os.path.isdir(ruta):
                existe_capeta_ev = True
                return existe_capeta_proyecto, existe_capeta_ev, elemento
        
        existe_capeta_ev = False
        elemento = None
        return existe_capeta_proyecto, existe_capeta_ev, elemento
    
    except FileNotFoundError:
        print("Error: la ruta del proyecto no existe")
        return False, False, None
    
def verificador_proyecto_intermedio(proyecto):
    try:

        ruta_git = os.path.join(proyecto.ruta, ".git")
        tiene_git = os.path.exists(ruta_git)
        
        ruta_requirements = os.path.join(proyecto.ruta, "requirements.txt")
        tiene_requirements = os.path.exists(ruta_requirements)
        
        archivos_en_directorio = os.listdir(proyecto.ruta)
        contador_scripts_python = 0
        contador_scripts_bash = 0
        
        for archivo in archivos_en_directorio:
            if archivo.endswith(".py"):
                contador_scripts_python += 1
            elif archivo.endswith(".sh"):
                contador_scripts_bash += 1

        return tiene_git, tiene_requirements, contador_scripts_python, contador_scripts_bash
    except FileNotFoundError:
        print("Error: la ruta del proyecto no existe")
        return False, False, 0, 0
    
def comprobar_info(proyecto):
    proyectos = cargar_proyectos()
    
    ruta_verificacion_proyecto, ruta_verificacion_ev, nombre_ev = verificar_proyecto_basico(proyecto=proyecto)
    
    tiene_git, tiene_requirements, contador_scrips, contador_sh = verificador_proyecto_intermedio(proyecto=proyecto)

    if ruta_verificacion_proyecto:
        if nombre_ev != proyecto.entorno_virtual:
            try:
                    indice = proyectos.index(proyecto)
                    
                    proyectos[indice].entorno_virtual = nombre_ev
                    
                    guardar_proyecto(proyectos=proyectos)
                    print("Se actualizó el nombre del entorno virtual.")
            except ValueError:
                print("Error: El proyecto no existe en la lista guardada.")
    else:
        print("Error: No se ha encontrado el directorio.")



