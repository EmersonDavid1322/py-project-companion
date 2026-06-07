from logica_cli import encontrar_proyecto, agregar_proyecto, mostrar_proyectos, activar_proyecto, crear_ev_personalizado, git_commit, eliminar, escanear_proyecto,editar

def main_menu():
    while True:
        print("1) Seleccionar proyecto")
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

        opciones = {
            1: secund_menu,
            2: agregar_proyecto,
            3: editar,
            4: eliminar,
            5: mostrar_proyectos,
        }

        if opcion in opciones:
            opciones[opcion]()
        elif opcion == 0:
            print("Ten un buen día :)")
            break
        else:
            print("Opción no disponible")

def secund_menu():
    proyecto_seleccionado, proyectos = encontrar_proyecto()

    while True:
        print(f"Proyecto seleccionado: {proyecto_seleccionado.nombre}\n")
        print("1) Crear entorno virtual")
        print("2) Activar proyecto")
        print("3) Subir cambios a github")
        print("4) Escanear proyecto")
        print("0) Volver al menu")

        try:
            opcion = int(input("\nSeleccione una opción: "))
        except ValueError:
            print("\nOpción no valida\n")
            continue
        except KeyboardInterrupt:
            break

        opciones = {
            1: crear_ev_personalizado,
            2: activar_proyecto,
            3: git_commit,
            4: escanear_proyecto
        }

        if opcion in opciones:
            opciones[opcion](proyecto_seleccionado, proyectos)
        elif opcion == 0:
            break
        else:
            print("Opción no disponible")




if __name__ == "__main__":
    main_menu()