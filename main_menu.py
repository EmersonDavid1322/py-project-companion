import logica_cli as cli

def main_menu():
    opciones = {
            1: secund_menu,
            2: cli.agregar_proyecto,
            3: cli.editar,
            4: cli.eliminar,
            5: cli.mostrar_proyectos,
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
    proyecto_seleccionado, proyectos = cli.encontrar_proyecto()

    if proyecto_seleccionado is None:
        return

    opciones = {
            1: lambda: cli.crear_ev_personalizado(proyecto_seleccionado, proyectos),
            2: lambda: cli.crear_requirements(proyecto_seleccionado),
            3: lambda: cli.activar_proyecto(proyecto_seleccionado),
            4: lambda: cli.git_pull(proyecto_seleccionado),
            5: lambda: cli.git_commit(proyecto_seleccionado),
            7: lambda: cli.mostrar_historia(proyecto_seleccionado)
        }

    while True:
        print(f"Proyecto seleccionado: {proyecto_seleccionado.nombre}\n")
        print("1) Crear entorno virtual")
        print("2) Crear requirements")
        print("3) Activar proyecto")
        print("4) Git pull")
        print("5) Subir cambios a github")
        print("6) Escanear proyecto")
        print("7) Mostrar historial de acciones")
        print("0) Volver al menu")

        try:
            opcion = int(input("\nSeleccione una opción: "))
        except ValueError:
            print("\nOpción no valida\n")
            continue
        except KeyboardInterrupt:
            break

        if opcion == 6:
                proyecto_seleccionado = cli.escanear_proyecto(proyecto_seleccionado)
        else:
            if opcion in opciones:
                opciones[opcion]()
            elif opcion == 0:
                break
            else:
                print("Opción no disponible")




if __name__ == "__main__":
    main_menu()