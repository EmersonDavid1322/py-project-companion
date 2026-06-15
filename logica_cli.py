import subprocess
import os
from pathlib import Path
import platform
from collections import deque
from class_launcher import Proyecto
from storage_json import guardar_a_json, cargar_proyectos, guardar_accion
from git_ops import ejecutar_commit, tiempo_ultimo_commit, ejecutar_git_pull
from sistema_ops import crear_ev
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
                commit_informacion = {"proyecto": proyecto_seleccionado, "rama": rama, "commit": commit}
                lista_commits.append(commit_informacion)
                print(f"commit añadido al proyecto: {commit_informacion}")
            else:
                print("Error: Proyecto ya añadido\n")
        
        except ValueError:
            print("Proyecto no encontrado en la lista")

        except KeyboardInterrupt:
            break
    
    if not lista_commits:
        print("No se ejecuto ningun commit")
    else:
        print("Proyectos seleccionados:\n")
        for proyecto in lista_commits:
            print(f"Información: {proyecto["proyecto"]}\nRama: {proyecto["rama"]}\nCommit: {proyecto["commit"]}\n")

        confirmacion = input("¿Desea continuar? (SI/NO): ").lower()
        if confirmacion in ("s","si"):
            while lista_commits:
                proyecto = lista_commits.popleft()
                print(f"Se incio el commit {proyecto}")
                
                ejecutar_commit(proyecto_usar=proyecto["proyecto"], rama_usar=proyecto["rama"], commit_usar=proyecto["commit"])
        else:
            print("Se cancelo la ejecución")

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

def git_pull(proyecto_seleccionado):
    if proyecto_seleccionado is None:
        return

    print(f"Ruta: {proyecto_seleccionado.ruta}\n")
    rama = input("\n('Dejalo vacio = main')\nColoque el nombre de la rama\n")
    if rama == "":
        rama = "main"

    print(f"\nInformación: {proyecto_seleccionado}\nRama: {rama}")
    confirmacion = input("¿Desea continuar? (SI/NO): ").lower()

    if confirmacion in ("s","si"):
        ejecutar_git_pull(proyecto_usar=proyecto_seleccionado, rama_usar=rama)
    else:
        print("Se cancelo la ejecución")

def git_commit(proyecto_seleccionado):
    if proyecto_seleccionado is None:
        return

    try:
        print(f"Ruta: {proyecto_seleccionado.ruta}\n")
        commit = input("Introduzca el commit:\n")
        rama = input("\n('Dejalo vacio = main')\nColoque el nombre de la rama\n")
        if rama == "":
            rama = "main"

        print(f"\nInformación: {proyecto_seleccionado}\nRama: {rama}\nCommit: {commit}")
        confirmacion = input("¿Desea continuar? (SI/NO): ")

        if confirmacion in ("s","si"):
            ejecutar_commit(proyecto_usar=proyecto_seleccionado, rama_usar=rama, commit_usar=commit)
        else:
            print("Se cancelo el commit")
    except KeyboardInterrupt:
        print("Cancelado\n")


def escanear_proyecto(proyecto):

    if proyecto is None:
        return

    tiempo_commit = None

    tiene_git, tiene_requirements, contador_scrips, contador_sh = verificador_proyecto_intermedio(proyecto=proyecto)

    proyecto_actualizado = comprobar_info(proyecto=proyecto)

    print(f"=== REPORTE DE SALUD: {proyecto.nombre.upper()} ===")
    print(f"📍 Ruta: {proyecto.ruta}")
    print(f"📦 Entorno Virtual: {proyecto.entorno_virtual}")
    print(f"🐙 Repositorio Git: {proyecto.git_carpeta}")
    print(f"📋 Archivo de Dependencias: {'✅ Detectado (requirements.txt)' if tiene_requirements else '⚠️ Falta requirements.txt'}")
    print(f"💻 Total de Scripts: {contador_scrips} archivos .py | {contador_sh} archivos .sh")
    if tiene_git:
        tiempo_commit = tiempo_ultimo_commit(proyecto_actualizado)
    print(f"Ultimo commit registrado: {tiempo_commit if tiempo_commit is not None else "No hay logs registrados"}")
    print("=========================================\n")

    return proyecto_actualizado

def mostrar_historia(proyecto):

    for accion in proyecto.historial:
        print(accion)