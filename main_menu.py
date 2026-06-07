from logica_cli import agregar_proyecto, mostrar_proyectos, activar_proyecto, crear_ev_personalizado, git_commit, eliminar, escanear_proyecto,editar

def main_menu():
    while True:
        print("1) Agregar proyecto")
        print("2) Editar proyecto")
        print("3) Eliminar proyecto")
        print("4) Ver proyectos")
        print("5) Crear entorno virtual")
        print("6) Activar proyecto")
        print("7) Subir cambios a github")
        print("8) Escanear proyecto")
        print("0) Salir")

        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("Opción no valida")
            continue
        except KeyboardInterrupt:
            print("\nTen un buen dia :)")
            break

        opciones = {
            1: agregar_proyecto,
            2: editar,
            3: eliminar,
            4: mostrar_proyectos,
            5: crear_ev_personalizado,
            6: activar_proyecto,
            7: git_commit,
            8: escanear_proyecto
        }

        if opcion in opciones:
            opciones[opcion]()
        elif opcion == 0:
            print("Ten un buen día :)")
            break
        else:
            print("Opción no disponible")



if __name__ == "__main__":
    main_menu()