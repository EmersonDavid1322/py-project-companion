import subprocess
import os
import platform
from pathlib import Path
from seguimiento import verificar_proyecto_basico
from storage_json import guardar_accion

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
