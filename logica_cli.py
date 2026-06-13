import subprocess
import os
from pathlib import Path
import platform
from collections import deque
from class_launcher import Proyecto
from storge_json import guardar_a_json, cargar_proyectos, guardar_accion
from seguimiento import verificar_proyecto_basico, verificador_proyecto_intermedio, comprobar_info

def encontrar_proyecto():
    proyectos = cargar_proyectos()
    proyecto_usar = None

    for i, proyecto in enumerate(proyectos):
        print(f"| {i} {proyecto}")

    try:
        print("Cancela con 'CTRL + C'")
        seleccion = int(input("Intruduzca el indice del proyecto: "))

        if seleccion >= 0:

            proyecto_usar = proyectos[seleccion]
            indice = proyectos.index(proyecto_usar)
            ruta = Path(proyecto_usar.ruta)

            if not ruta.is_dir():
                print("\nEl directorio no existe.\n")
                return None, proyectos
            
        else:
            print("El indice debe ser mayor o igual a 0")

    except (ValueError, IndexError) as e:
        print(f"Error: {e}\n")
    
    except KeyboardInterrupt:
        print("Cancelado\n")

    return proyecto_usar, proyectos

def crear_ev(proyecto):
    sistema = platform.system()

    try:

        _, existe_ev, _= verificar_proyecto_basico(proyecto=proyecto)

        if existe_ev:
            print("Ya se a detectado un entorno virtual en su carpeta")
            return
        else:

            ruta = Path(proyecto.ruta)

            comando_python = "py" if sistema == "Windows" else "python3"

            ruta_final_env = ruta / ".venv"

            comando_interno = [comando_python, "-m", "venv", str(ruta_final_env)]

            resultado = subprocess.run(
            comando_interno,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True
            )
            
            if resultado.returncode == 0:
                print("Entorno virtual creado con éxito.\n")
                return ".venv"
            else:
                print(f"Error al crear el entorno: {resultado.stderr}\n")
            return None
    
    except FileNotFoundError:
        print("Error: la ruta del proyecto no existe")
        return None

def agregar_proyecto():
    proyecto_list = cargar_proyectos()
    nombre = input("Introduzca el nombre: ")

    ubicacion = input("Coloque la ubicación del proyecto: ").strip()

    proyecto = Proyecto(nombre=nombre, ruta=ubicacion, ev=None, git_carpeta=None)

    ruta_verificacion_proyecto, ruta_verificacion_ev, nombre_ev= verificar_proyecto_basico(proyecto=proyecto)

    if ruta_verificacion_proyecto:
        proyecto_list.append(proyecto)

        proyecto.registrar_evento(accion="Creación",descripcion=f"Se añadio el proyecto {proyecto}")
        guardar_a_json(proyectos=proyecto_list)
        print("Recomendamos escaner el proyecto para guardar la información\n")
    else:
        print("Error: No se a encontrado la ruta")

def editar():
    proyecto_seleccionado, proyectos = encontrar_proyecto()

    if proyecto_seleccionado is None:
        return

    print("Si no desea cambiar un campo, dejalo vacio")
    nombre = input("Introduzca el nombre: \n")

    ubicacion = input("Coloque la ubicación del proyecto: \n").strip()

    env = input("Introduza el nombre del entorno virtual: \n")

    if nombre != "":
        proyecto_seleccionado.nombre = nombre

    if ubicacion != "":
        proyecto_seleccionado.ruta = ubicacion

    if env != "":
        proyecto_seleccionado._entorno_virtual = env

    guardar_accion(proyecto=proyecto_seleccionado,titulo="Edición",accion=f"Se edito el proyecto{proyecto_seleccionado}")

    print(f"Nombre: {proyecto_seleccionado.nombre}\nRuta: {proyecto_seleccionado.ruta}\nenv: {proyecto_seleccionado.entorno_virtual}")


def eliminar():
    proyecto_seleccionado, proyectos = encontrar_proyecto()

    if proyecto_seleccionado is None:
        return

    proyectos.remove(proyecto_seleccionado)

    guardar_a_json(proyectos=proyectos)

def mostrar_proyectos():
    proyectos = cargar_proyectos()

    proyectos.sort()
    for proyecto in proyectos:
        print(proyecto)

def secuencia_commits():
    lista_commits = deque([])

    while True:
        try:
            proyecto_seleccionado, _ = encontrar_proyecto()
            if proyecto_seleccionado is None:
                break
            commit = input("Introduzca el commit:\n")

            rama = input("\n('Dejalo vacio = main')\nColoque el nombre de la rama\n")
            if rama == "":
                rama = "main"

            
            if not any(d["proyecto"] == proyecto_seleccionado for d in lista_commits):
                commit_informacion = {"proyecto": proyecto_seleccionado.nombre, "rama": rama, "commit": commit}
                lista_commits.append(commit_informacion)
                print(f"commit añadido al proyecto: {commit_informacion}")
            else:
                print("Proyecto ya añadido")
        
        except ValueError:
            print("Proyecto no encontrado en la lista")

        except KeyboardInterrupt:
            print("Selecciones hechas ejecutanto commits")
            break
    
    if not lista_commits:
        print("No se ejecuto ningun commit")
        return
    
    while lista_commits:
        proyecto = lista_commits.popleft()
        print(f"Se incio el commit {proyecto}")
        
        ejecutar_commit(proyecto_usar=proyecto["proyecto"], rama_usar=proyecto["rama"], commit_usar=proyecto["commit"])



def crear_ev_personalizado(proyecto_seleccionado, proyectos):

    if proyecto_seleccionado is None:
        return
    
    indice = proyectos.index(proyecto_seleccionado)
    
    nombre_ev = crear_ev(proyecto=proyecto_seleccionado)
    if nombre_ev == None:
        print("Hubo un error en la ejecución")
        return

    proyecto_seleccionado._entorno_virtual = nombre_ev

    guardar_accion(proyecto=proyecto_seleccionado,
                    titulo="Entorno virtual",
                    accion=f"Se creo y vinculó un entorno al proyecto {proyecto_seleccionado.nombre} EV: {proyecto_seleccionado.entorno_virtual}")
    print("¡Proyecto actualizado y guardado con éxito!")

def crear_requirements(proyecto):
    if proyecto is None:
        return
    
    if proyecto._entorno_virtual is None:
        print("Advertencia: No se puede crear un archivo requirements sin un entorno virtual registrado.")
        return
    
    sistema = platform.system()
    print("Generando...")

    try:
        if sistema == "Linux":
            ruta_venv = os.path.join(proyecto.ruta, proyecto._entorno_virtual, "bin", "activate")
            ruta_requirements = os.path.join(proyecto.ruta, "requirements.txt")

            subprocess.run([
                "bash", 
                "-c", 
                f'source "{ruta_venv}" && pip freeze > "{ruta_requirements}"'
            ], check=True)
            print("✅ Requirements creado exitosamente en Linux.")

        else:
            ruta_venv = os.path.join(proyecto.ruta, proyecto._entorno_virtual, "Scripts", "Activate.ps1")
            comando_powershell = f'. "{ruta_venv}"; pip freeze > "{os.path.join(proyecto.ruta, "requirements.txt")}"'
            subprocess.run([
                "powershell", 
                "-NoProfile", 
                "-ExecutionPolicy", "Bypass", 
                "-Command", comando_powershell
            ], check=True)
            print("✅ Requirements generado en segundo plano con PowerShell.")

        guardar_accion(proyecto=proyecto,
                    titulo="requirements", 
                    accion=f"Se creo y actualizo un archivo requirements al proyecto: {proyecto.nombre}")

    except subprocess.CalledProcessError as e:
        print(f"❌ El comando falló con el código: {e.returncode}")
        print(f"🔍 El comando que falló fue: {e.cmd}")

def activar_proyecto(proyecto):
    sistema = platform.system()

    if sistema == "Windows":
        activar_windows(proyecto)

    elif sistema == "Linux":
        activar_linux(proyecto)

    else:
        print(f"Sistema operativo {sistema} no soportado temporalmente")

def activar_windows(proyecto):

    if proyecto._entorno_virtual is not None:
        ruta_venv = os.path.join(proyecto.ruta, proyecto._entorno_virtual, "Scripts", "Activate.ps1")
        comando_interno = f'powershell -NoExit -ExecutionPolicy Bypass -File "{ruta_venv}"'
        print(ruta_venv)

    else:
        comando_interno = f'powershell -NoExit -Command "Set-Location \'{proyecto.ruta}\'"'
        print("Nota: No se detectó entorno virtual (.venv), abriendo terminal normal.")

    try:
        subprocess.run(f"start {comando_interno}", shell=True, check=True)
        subprocess.run(["code", proyecto.ruta], shell="Windows", check=True)

    except subprocess.CalledProcessError as e:
        print(f"❌ El comando falló con el código: {e.returncode}")
        print(f"🔍 El comando que falló fue: {e.cmd}")

def activar_linux(proyecto):

    if proyecto._entorno_virtual is not None:
        ruta_venv = os.path.join(proyecto.ruta, proyecto._entorno_virtual, "bin", "activate")
        comando_interno = f"bash --rcfile <(echo 'source ~/.bashrc; source {ruta_venv}')"
        print(ruta_venv)

    else:
        comando_interno = f"cd '{proyecto.ruta}' && exec bash"
        print("Nota: No se detectó entorno virtual (.venv), abriendo terminal normal.")

    try:
        subprocess.run([
            "x-terminal-emulator", 
            "--", 
            "bash", 
            "-c", 
            comando_interno
        ], check=True)

        subprocess.run(["code", proyecto.ruta], check=True) 

    except subprocess.CalledProcessError as e:
        print(f"❌ El comando falló con el código: {e.returncode}")
        print(f"🔍 El comando que falló fue: {e.cmd}")

def git_pull(proyecto_seleccionado):
    sistema = platform.system()

    if proyecto_seleccionado is None:
        return

    try:
        print(f"Ruta: {proyecto_seleccionado.ruta}\n")
        rama = input("\n('Dejalo vacio = main')\nColoque el nombre de la rama\n")
        if rama == "":
            rama = "main"

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

        print("Cargando cambios...")
        
        resultado = subprocess.run(
            ["git", "pull", "origin", rama], 
            capture_output=True, 
            text=True, 
            cwd=proyecto_seleccionado.ruta, 
            shell=(sistema == "Windows"), 
            check=True
        )
        
        print("¡Cambios cargados con éxito!\n")

        guardar_accion(proyecto=proyecto_seleccionado, titulo="Git Pull",
                        accion=f"Se hiso un git pull al proyecto: {proyecto_seleccionado.nombre}")

    except subprocess.CalledProcessError as e:
        print("Error al hacer pull:\n", e.stderr)

    except KeyboardInterrupt:
        print("Cancelado\n")

def git_commit(proyecto_seleccionado):
    if proyecto_seleccionado is None:
        return

    print(f"Ruta: {proyecto_seleccionado.ruta}\n")
    commit = input("Introduzca el commit:\n")
    rama = input("\n('Dejalo vacio = main')\nColoque el nombre de la rama\n")
    if rama == "":
        rama = "main"
        

    ejecutar_commit(proyecto_usar=proyecto_seleccionado, rama_usar=rama, commit_usar=commit)

def ejecutar_commit(proyecto_usar, rama_usar, commit_usar):
    sistema = platform.system()
    try:

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

        print("Subiendo cambios...")
        
        subprocess.run(["git", "add", "."], stdout=subprocess.DEVNULL, cwd=proyecto_usar.ruta)
        
        subprocess.run(["git", "commit", "-m", commit_usar], stdout=subprocess.DEVNULL, cwd=proyecto_usar.ruta)
        
        subprocess.run(["git", "push", "origin", rama_usar], stdout=subprocess.DEVNULL, cwd=proyecto_usar.ruta, shell=(sistema == "Windows"), check=True)

        guardar_accion(proyecto=proyecto_usar, titulo="Git commit", 
                        accion=f"Se hiso un git commit\nRama: {rama_usar}\nCommit: '{commit_usar}'")
        print("¡Cambios subidos con éxito!\n")

    except subprocess.CalledProcessError:
        print("Error: Este directorio no parece tener un repositorio de Git configurado.")

    except KeyboardInterrupt:
        print("Cancelado\n")

def escanear_proyecto(proyecto):

    if proyecto is None:
        return

    tiene_git, tiene_requirements, contador_scrips, contador_sh = verificador_proyecto_intermedio(proyecto=proyecto)

    proyecto_actualizado = comprobar_info(proyecto=proyecto)

    print(f"=== REPORTE DE SALUD: {proyecto.nombre.upper()} ===")
    print(f"📍 Ruta: {proyecto.ruta}")
    print(f"📦 Entorno Virtual: {proyecto.entorno_virtual}")
    print(f"🐙 Repositorio Git: {proyecto.git_carpeta}")
    print(f"📋 Archivo de Dependencias: {'✅ Detectado (requirements.txt)' if tiene_requirements else '⚠️ Falta requirements.txt'}")
    print(f"💻 Total de Scripts: {contador_scrips} archivos .py | {contador_sh} archivos .sh")
    print("=========================================\n")

    return proyecto_actualizado

def mostrar_historia(proyecto):

    for accion in proyecto.historial:
        print(accion)