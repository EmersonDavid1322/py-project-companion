import subprocess
import platform
import logging
from storage_json import guardar_accion

def verificar_remoto(proyecto_usar):
    logger = logging.getLogger(__name__)
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
            return {"estado": "http", "mensaje": "El repositorio es HTTP"}

    except subprocess.CalledProcessError as e:
        logger.error(f"Error al ejecutar el comando {e.stderr}")
        return {"estado": "error_subprocess", "mensaje": f"Error al ejecutar el comando {e.stderr}" }

    return {"estado": "ok", "mensaje": "El repositorio es SSH y se puede usar en segundo plano"}

def ejecutar_commit(proyecto_usar, rama_usar, commit_usar):
    sistema = platform.system()
    logger = logging.getLogger(__name__)

    try:
        print("Subiendo cambios...")
        
        subprocess.run(["git", "add", "."], stdout=subprocess.DEVNULL, cwd=proyecto_usar.ruta)
        
        subprocess.run(["git", "commit", "-m", commit_usar], stdout=subprocess.DEVNULL, cwd=proyecto_usar.ruta)
        
        subprocess.run(["git", "push", "origin", rama_usar], stdout=subprocess.DEVNULL, cwd=proyecto_usar.ruta, shell=(sistema == "Windows"), check=True)

        guardar_accion(proyecto=proyecto_usar, titulo="Git commit", 
                        accion=f"Se hiso un git commit\nRama: {rama_usar}\nCommit: '{commit_usar}'")
        logger.info(f"Se hizo un commit al proyecto: {proyecto_usar.nombre} rama: {rama_usar}\nCommit: '{commit_usar}'")
        print("¡Cambios subidos con éxito!\n")

    except subprocess.CalledProcessError as e:
        logger.error(f"Error al ejecutar el comando {e.stderr}")
        print("Error: Este directorio no parece tener un repositorio de Git configurado.")

def ejecutar_git_pull(proyecto_usar, rama_usar):
    logger = logging.getLogger(__name__)
    sistema = platform.system()

    try:
        print("Cargando cambios...")
        
        resultado = subprocess.run(
            ["git", "pull", "origin", rama_usar], 
            capture_output=True, 
            text=True, 
            cwd=proyecto_usar.ruta, 
            shell=(sistema == "Windows"), 
            check=True
        )
        
        print("¡Cambios cargados con éxito!\n")

        guardar_accion(proyecto=proyecto_usar, titulo="Git Pull",
                        accion=f"Se hiso un git pull al proyecto: {proyecto_usar.nombre}")

    except subprocess.CalledProcessError as e:
        logger.error(f"Error al ejecutar el comando {e.stderr}")
        print("Error al hacer pull:\n", e.stderr)

    except KeyboardInterrupt:
        print("Cancelado\n")

def tiempo_ultimo_commit(proyecto_seleccionado):
    sistema = platform.system()
    logger = logging.getLogger(__name__)

    try:
        resultado = subprocess.run(
            ["git", "log", "-1", "--format=%cr"],
            capture_output=True, 
            text=True, 
            cwd=proyecto_seleccionado.ruta, 
            shell=(sistema == "Windows"), 
            check=True
        )
        
        return resultado.stdout.strip()

    except subprocess.CalledProcessError as e:
        logger.error(f"Error al ejecutar el comando {e.stderr}")
        print("Error al hacer el comando:\n", e.stderr)
        return None

