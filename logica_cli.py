import subprocess
import os
from pathlib import Path
from class_launcher import Proyecto
from storge_json import guardar_proyecto, cargar_proyectos
from seguimiento import verificar_proyecto_basico, verificador_proyecto_intermedio

def encontrar_proyecto():
    proyectos = cargar_proyectos()
    proyecto_usar = None
    

    for i, proyecto in enumerate(proyectos):
        print(f"{i} | {proyecto.nombre} | Entorno: {proyecto.entorno_virtual}\nRuta: {proyecto.ruta}\n")

    try:
        seleccion = int(input("Intruduzca el indice del proyecto: "))

        if seleccion >= 0:

            proyecto_usar = proyectos[seleccion]
            print(proyecto_usar.nombre)
        else:
            print("El indice debe ser mayor o igual a 0")

    except (ValueError, IndexError) as e:
        print(f"Error: {e}")

    return proyecto_usar, proyectos

def crear_ev(proyecto):

    try:

        _, existe_ev, _= verificar_proyecto_basico(proyecto=proyecto)

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

    ruta_verificacion_proyecto, ruta_verificacion_ev, nombre_ev= verificar_proyecto_basico(proyecto=proyecto)

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

def editar():
    proyecto_seleccionado, proyectos = encontrar_proyecto()

    print("Si no desea cambiar un campo dejalo vasio\n")

    if proyecto_seleccionado:
        nombre = input("Introduzca el nombre: \n")

        ubicacion = input("Coloque la ubicación del proyecto: \n").strip()

        env = input("Introduza el nombre del entorno virtual: \n")

        if nombre != "":
            proyecto_seleccionado.nombre = nombre

        if ubicacion != "":
            proyecto_seleccionado.ruta = ubicacion

        if env != "":
            proyecto_seleccionado.entorno_virtual = env

        guardar_proyecto(proyectos=proyectos)

    else:
        print("Proyecto no encontrado")
        return

    print(f"Nombre: {proyecto_seleccionado.nombre}\nRuta: {proyecto_seleccionado.ruta}\nenv: {proyecto_seleccionado.entorno_virtual}")


def eliminar():
    proyecto_seleccionado, proyectos = encontrar_proyecto()

    if proyecto_seleccionado is None:
        return

    proyectos.remove(proyecto_seleccionado)

    guardar_proyecto(proyectos=proyectos)

def mostrar_proyectos():
    proyectos = cargar_proyectos()

    for proyecto in proyectos:
        print(f"Nombre: {proyecto.nombre} \nRuta: {proyecto.ruta}\nEntrono virtua: {proyecto.entorno_virtual}\n")

def crear_ev_personalizado():
    proyecto_seleccionado, proyectos = encontrar_proyecto()
    
    nombre_ev = crear_ev(proyecto=proyecto_seleccionado)
    if nombre_ev == None:
        print("Hubo un error en la ejecución")
        return

    proyecto_seleccionado.entorno_virtual = nombre_ev

    guardar_proyecto(proyectos=proyectos)
    print("¡Proyecto actualizado y guardado con éxito!")

def activar_proyecto():
    proyecto_seleccionado, _ = encontrar_proyecto()

    if proyecto_seleccionado is None:
        return

    
    if proyecto_seleccionado.entorno_virtual != None:
        ruta_venv = os.path.join(proyecto_seleccionado.ruta, proyecto_seleccionado.entorno_virtual, "bin", "activate")
        print(ruta_venv)
        comando_interno = f"bash --rcfile <(echo 'source ~/.bashrc; source {ruta_venv}')"
    
    else:
        comando_interno = f"cd '{proyecto_seleccionado.ruta}' && exec bash"
        print("Nota: No se detectó entorno virtual (.venv), abriendo terminal normal.")

    try:
        subprocess.run([
            "x-terminal-emulator", 
            "--", 
            "bash", 
            "-c", 
            comando_interno
        ], check=True)

        subprocess.run(["code", proyecto_seleccionado.ruta], check=True)
    
    except subprocess.CalledProcessError as e:
        print(f"❌ El comando falló con el código: {e.returncode}")
        print(f"🔍 El comando que falló fue: {e.cmd}")
        print(f"⚠️ Mensaje real de Linux: {e.stderr}")


def escanear_proyecto():
    proyecto, proyectos = encontrar_proyecto()

    if proyecto is None:
        return

    ruta_verificacion_proyecto, ruta_verificacion_ev, _, = verificar_proyecto_basico(proyecto=proyecto)
    
    tiene_git, tiene_requirements, contador_scrips, contador_sh = verificador_proyecto_intermedio(proyecto=proyecto)

    print(f"=== REPORTE DE SALUD: {proyecto.nombre.upper()} ===")
    print(f"📍 Ruta: {proyecto.ruta}")
    print(f"📦 Entorno Virtual: {proyecto.entorno_virtual if ruta_verificacion_ev else '❌ No configurado'}")
    print(f"🐙 Repositorio Git: {'✅ Inicializado' if tiene_git else '❌ Sin Git'}")
    print(f"📋 Archivo de Dependencias: {'✅ Detectado (requirements.txt)' if tiene_requirements else '⚠️ Falta requirements.txt'}")
    print(f"💻 Total de Scripts: {contador_scrips} archivos .py | {contador_sh} archivos .sh")
    print("=========================================\n")

def git_commit():
    proyecto_seleccionado, _ = encontrar_proyecto()

    if proyecto_seleccionado is None:
        return

    print(f"Ruta: {proyecto_seleccionado.ruta}\n")
    print("Debe de colocar el commit entre comillas dobles\n")
    commit = input("Introduzca el commit: ")

    try:

        resultado = subprocess.run(
            ["git", "remote", "get-url", "origin"], 
            capture_output=True, 
            text=True, 
            check=True,
            cwd=proyecto_seleccionado.ruta
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
        
        subprocess.run(["git", "add", "."], stdout=subprocess.DEVNULL, cwd=proyecto_seleccionado.ruta)
        
        subprocess.run(["git", "commit", "-m", commit], stdout=subprocess.DEVNULL, cwd=proyecto_seleccionado.ruta)
        
        subprocess.run(["git", "push", "origin", "main"], stdout=subprocess.DEVNULL, cwd=proyecto_seleccionado.ruta)
        
        print("¡Cambios subidos con éxito!\n")

    except subprocess.CalledProcessError:
        print("Error: Este directorio no parece tener un repositorio de Git configurado.")