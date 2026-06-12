import os
from pathlib import Path
from storge_json import cargar_proyectos, guardar_accion

def verificar_proyecto_basico(proyecto):

    try:
        verificacion_carpeta_proyecto = Path(proyecto.ruta)

        if verificacion_carpeta_proyecto.exists():
            existe_capeta_proyecto = True
        else:
            existe_capeta_proyecto = False

        nombres_comunes = ["venv", ".venv", "env", ".env"]

        if proyecto._entorno_virtual != None:
            nombres_comunes.append(proyecto._entorno_virtual)

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

        if not tiene_git:
            ruta_git = None
        
        ruta_requirements = os.path.join(proyecto.ruta, "requirements.txt")
        tiene_requirements = os.path.exists(ruta_requirements)
        
        archivos_en_directorio = os.listdir(proyecto.ruta)
        
        contador_scripts_python = sum(1 for archivo in archivos_en_directorio if archivo.endswith(".py"))
        contador_scripts_bash = sum(1 for archivo in archivos_en_directorio if archivo.endswith(".sh"))

        return ruta_git, tiene_requirements, contador_scripts_python, contador_scripts_bash
    except FileNotFoundError:
        print("Error: la ruta del proyecto no existe")
        return False, False, 0, 0
    
def comprobar_info(proyecto):
    proyectos = cargar_proyectos()
    
    ruta_verificacion_proyecto, ruta_verificacion_ev, nombre_ev = verificar_proyecto_basico(proyecto=proyecto)
    
    ruta_git, tiene_requirements, contador_scrips, contador_sh = verificador_proyecto_intermedio(proyecto=proyecto)

    if ruta_verificacion_proyecto:
        if nombre_ev != proyecto._entorno_virtual:
            print(f"Nombre ev: {nombre_ev} Nombre proyecto ev: {proyecto._entorno_virtual}")
            try:
                    indice = proyectos.index(proyecto)
                    
                    proyecto_actualizado = proyectos[indice]
                    proyecto_actualizado._entorno_virtual = nombre_ev

                    guardar_accion(proyecto=proyecto_actualizado, indice=indice,
                                    titulo="Entorno virtual", accion=f"Se modifico el estado del entorno virtual {proyecto_actualizado}")
                    print("Se actualizó el nombre del entorno virtual.")
            except ValueError as e:
                print(f"Error: {e}")

        if ruta_git and proyecto._git_carpeta != ruta_git:
            indice = proyectos.index(proyecto)

            proyectos[indice]._git_carpeta = ruta_git
            guardar_accion(proyecto=proyecto, indice=indice,
                                    titulo="Carpeta git", accion=f"Se modifico el estado de la carpeta git {proyecto}")
            print("Se a actualizado la información de la carpeta git")

    else:
        print("Error: No se ha encontrado el directorio.")



