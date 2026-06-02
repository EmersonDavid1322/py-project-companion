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

        if opcion == 1:
            agregar_proyecto()

        elif opcion == 2:
            editar()

        elif opcion == 3:
            eliminar()

        elif opcion == 4:
            mostrar_proyectos()

        elif opcion == 5:
            crear_ev_personalizado()

        elif opcion == 6:
            activar_proyecto()

        elif opcion == 7:
            git_commit()

        elif opcion == 8:
            escanear_proyecto()

        elif opcion == 0:
            print("Ten un buen dia :)")
            break
        else:
            print("Opcion no disponible")



if __name__ == "__main__":
    main_menu()