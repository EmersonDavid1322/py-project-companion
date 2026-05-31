from servicios import agregar_proyecto, mostrar_proyectos, activar_proyecto, crear_ev_personalizado, git_commit

def main_menu():
    while True:
        print("1) Agregar proyecto")
        print("2) ver proyectos")
        print("3) crear entorno virtual")
        print("4) activar proyecto")
        print("5) subir cambios a github")
        print("0) Salir")

        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("Opción no valida")
            continue

        if opcion == 1:
            agregar_proyecto()

        elif opcion == 2:
            mostrar_proyectos()

        elif opcion == 3:
            crear_ev_personalizado()

        elif opcion == 4:
            activar_proyecto()

        elif opcion == 5:
            git_commit()

        elif opcion == 0:
            print("Ten un buen dia :)")
            break
        else:
            print("Opcion no disponible")



if __name__ == "__main__":
    main_menu()