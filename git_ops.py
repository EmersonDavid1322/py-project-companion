import subprocess
import platform
from storage_json import guardar_accion

def verificar_remoto(proyecto_usar):
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
                return False
    except subprocess.CalledProcessError as e:
        print("Error al verificar el remoto:\n", e.stderr)
        return False

    return True

def ejecutar_commit(proyecto_usar, rama_usar, commit_usar):
    sistema = platform.system()

    if not verificar_remoto(proyecto_usar):
        return

    try:
        print("Subiendo cambios...")
        
        subprocess.run(["git", "add", "."], stdout=subprocess.DEVNULL, cwd=proyecto_usar.ruta)
        
        subprocess.run(["git", "commit", "-m", commit_usar], stdout=subprocess.DEVNULL, cwd=proyecto_usar.ruta)
        
        subprocess.run(["git", "push", "origin", rama_usar], stdout=subprocess.DEVNULL, cwd=proyecto_usar.ruta, shell=(sistema == "Windows"), check=True)

        guardar_accion(proyecto=proyecto_usar, titulo="Git commit", 
                        accion=f"Se hiso un git commit\nRama: {rama_usar}\nCommit: '{commit_usar}'")
        print("¡Cambios subidos con éxito!\n")

    except subprocess.CalledProcessError:
        print("Error: Este directorio no parece tener un repositorio de Git configurado.")

def ejecutar_git_pull(proyecto_usar, rama_usar):
    sistema = platform.system()

    if not verificar_remoto(proyecto_usar):
        return

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
        print("Error al hacer pull:\n", e.stderr)

    except KeyboardInterrupt:
        print("Cancelado\n")

def tiempo_ultimo_commit(proyecto_seleccionado):
    sistema = platform.system()

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
        print("Error al hacer el comando:\n", e.stderr)
        return None

