from logica_cli import encontrar_proyecto, agregar_proyecto, mostrar_proyectos, crear_ev_personalizado, git_commit, crear_requirements, eliminar, escanear_proyecto,editar

def main_menu():
    opciones = {
            1: secund_menu,
            2: agregar_proyecto,
            3: editar,
            4: eliminar,
            5: mostrar_proyectos,
        }
    
    while True:
        print("\n1) Seleccionar proyecto")
        print("2) Agregar proyecto")
        print("3) Editar proyecto")
        print("4) Eliminar proyecto")
        print("5) Ver proyectos")
        print("0) Salir")

        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("\nOpción no valida\n")
            continue
        except KeyboardInterrupt:
            print("\nTen un buen dia :)")
            break

        if opcion in opciones:
            opciones[opcion]()
        elif opcion == 0:
            print("Ten un buen día :)")
            break
        else:
            print("Opción no disponible")

def secund_menu():
    proyecto_seleccionado, proyectos = encontrar_proyecto()

    if proyecto_seleccionado is None:
        return

    opciones = {
            1: lambda: crear_ev_personalizado(proyecto_seleccionado, proyectos),
            2: lambda: crear_requirements(proyecto_seleccionado),
            3: lambda: proyecto_seleccionado.activar_proyecto(),
            4: lambda: git_commit(proyecto_seleccionado),
            5: lambda: escanear_proyecto(proyecto_seleccionado)
        }

    while True:
        print(f"Proyecto seleccionado: {proyecto_seleccionado.nombre}\n")
        print("1) Crear entorno virtual")
        print("2) Crear requirements")
        print("3) Activar proyecto")
        print("4) Subir cambios a github")
        print("5) Escanear proyecto")
        print("0) Volver al menu")

        try:
            opcion = int(input("\nSeleccione una opción: "))
        except ValueError:
            print("\nOpción no valida\n")
            continue
        except KeyboardInterrupt:
            break

        if opcion in opciones:
            opciones[opcion]()
        elif opcion == 0:
            break
        else:
            print("Opción no disponible")




if __name__ == "__main__":
    main_menu()