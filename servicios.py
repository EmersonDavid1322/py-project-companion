import subprocess
import os
from pathlib import Path
from class_launcher import Proyecto
from storge_json import guardar_proyecto, cargar_proyectos

def verificar_proyecto(proyecto):

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
        return None
    
def crear_ev(proyecto):

    try:

        _, existe_ev, _ = verificar_proyecto(proyecto=proyecto)

        if existe_ev:
            print("Ya se a detectado un entorno virtual en su carpeta")
            return
        else:

            ruta = Path(proyecto.ruta)

            ruta_final_env = ruta / ".venv"

            comando_interno = ["python3", "-m", "venv", str(ruta_final_env)]

            resultado = subprocess.run(
            comando_interno,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True
        )
            
            if resultado.returncode == 0:
                print("Entorno virtual creado con éxito.")
                return ".venv"
            else:
                print(f"Error al crear el entorno: {resultado.stderr}")
            return None
    
    except FileNotFoundError:
        print("Error: la ruta del proyecto no existe")
        return None

def agregar_proyecto():
    proyecto_list = cargar_proyectos()
    nombre = input("Introduzca el nombre: ")

    ubicacion = input("Coloque la ubicación del proyecto: ").strip()

    proyecto = Proyecto(nombre=nombre, ruta=ubicacion, ev=None)

    ruta_verificacion_proyecto, ruta_verificacion_ev, nombre_ev = verificar_proyecto(proyecto=proyecto)

    if ruta_verificacion_proyecto:
        if ruta_verificacion_ev:
            print(f"EL proyecto a sido agregado correctamente. \nNombre: {proyecto.nombre} \nRuta: {proyecto.ruta}")
            proyecto.entorno_virtual = nombre_ev
            proyecto_list.append(proyecto)
            guardar_proyecto(proyectos=proyecto_list)
        else:
            print("(El proyecto se a guardo sin un entorno virtual)\nNo se a detecteado un entorno virtual, recomendamos crearlo.\n")

            confirmacio_ev = input("(Por defecto venv)\nDesea agregar uno de forma automatica (SI/NO): ").lower()
            if confirmacio_ev in ("si","s"):
                nombre_ev_new = crear_ev(proyecto=proyecto_list)
                proyecto.entorno_virtual = nombre_ev_new
                proyecto_list.append(proyecto)
                guardar_proyecto(proyectos=proyecto_list)
            else:
                proyecto_list.append(proyecto)
                guardar_proyecto(proyectos=proyecto_list)
    else:
        print("Error: No se a encontrado la ruta")

def mostrar_proyectos():
    proyectos = cargar_proyectos()

    for proyecto in proyectos:
        print(f"Nombre: {proyecto.nombre} \nRuta: {proyecto.ruta}\nEntrono virtua: {proyecto.entorno_virtual}\n")

def crear_ev_personalizado():
    proyectos = cargar_proyectos()

    for i, proyecto in enumerate(proyectos):
        print(f"{i} | {proyecto.nombre}\nRuta: {proyecto.ruta}\n")

    seleccion = int(input("Introduzca el índice del proyecto que desea: "))

    if 0 <= seleccion < len(proyectos):

        proyecto_seleccionado = proyectos[seleccion]
        
        nombre_ev = crear_ev(proyecto=proyecto_seleccionado)
        if nombre_ev == None:
            print("Hubo un error en la ejecución")
            return

        proyecto_seleccionado.entorno_virtual = nombre_ev

        guardar_proyecto(proyectos=proyectos)
        print("¡Proyecto actualizado y guardado con éxito!")
    else:
        print("Selección inválida.")

def activar_proyecto():
    proyectos = cargar_proyectos()

    for i, proyecto in enumerate(proyectos):
        print(f"{i} | {proyecto.nombre} | Entorno: {proyecto.entorno_virtual}\n")

    seleccion = input("Intruduzca el proyecto que desea activar: ")

    for proyecto in proyectos:
        if seleccion == proyecto.nombre:
            proyecto_usar = proyecto
            print(f"Proyecto {proyecto_usar.nombre} encontrado")

    ruta_venv = os.path.join(proyecto_usar.ruta, proyecto_usar.entorno_virtual, "bin", "activate")
    print(ruta_venv)

    if os.path.exists(ruta_venv):
        comando_interno = f"bash --rcfile <(echo 'source ~/.bashrc; source {ruta_venv}')"
    
    else:
        comando_interno = f"cd '{proyecto_usar.ruta}' && exec bash"
        print("Nota: No se detectó entorno virtual (.venv), abriendo terminal normal.")

    try:
        subprocess.run([
            "x-terminal-emulator", 
            "--", 
            "bash", 
            "-c", 
            comando_interno
        ], check=True)

        subprocess.run(["code", proyecto_usar.ruta], check=True)
    
    except subprocess.CalledProcessError as e:
        print(f"❌ El comando falló con el código: {e.returncode}")
        print(f"🔍 El comando que falló fue: {e.cmd}")
        print(f"⚠️ Mensaje real de Linux: {e.stderr}")


def git_commit():
    proyectos = cargar_proyectos()

    for i, proyecto in enumerate(proyectos):
        print(f"{i} | {proyecto.nombre} | Entorno: {proyecto.entorno_virtual}\n")

    seleccion = input("Introduzca el nombre del proyecto que desea: ")

    for i, proyecto in enumerate(proyectos):
        if seleccion == proyecto.nombre:
            proyecto_usar = proyecto
            print(f"proyecto {proyecto_usar.nombre} encontrado\nRuta: {proyecto_usar.ruta} ")

    commit = input("Introduzca el commit: ")

    try:
    # Revisa cómo está configurado el repositorio actual
        resultado = subprocess.run(
            ["git", "remote", "get-url", "origin"], 
            capture_output=True, 
            text=True, 
            check=True,
            cwd=proyecto_usar.ruta
        )
        url_actual = resultado.stdout.strip()

        if url_actual.startswith("http"):
            print("⚠️ ADVERTENCIA: Este script ejecuta Git en segundo plano.")
            print("Para usar esta opción, necesitas configurar claves SSH en tu cuenta")
            print("y cambiar el origen del repositorio a SSH (git@github.com...).")
            print("De lo contrario, el proceso se congelará esperando tu contraseña.")
            
            confirmar = input("\n¿Ya configuraste el 'credential.helper' para recordar tu contraseña? (s/n): ")
            if confirmar.lower() != 's':
                print("Operación cancelada para evitar bloqueos.")
                return

        print("Subiendo cambios de forma invisible...")
        
        subprocess.run(["git", "add", "."], stdout=subprocess.DEVNULL, cwd=proyecto_usar.ruta)
        
        subprocess.run(["git", "commit", "-m", commit], stdout=subprocess.DEVNULL, cwd=proyecto_usar.ruta)
        
        subprocess.run(["git", "push", "origin", "main"], stdout=subprocess.DEVNULL, cwd=proyecto_usar.ruta)
        
        print("¡Cambios subidos con éxito!")

    except subprocess.CalledProcessError:
        print("Error: Este directorio no parece tener un repositorio de Git configurado.")