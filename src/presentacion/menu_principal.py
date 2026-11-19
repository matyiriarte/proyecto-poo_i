from presentacion.menu_departamento import menu_departamentos
from presentacion.menu_empleado import menu_empleados
from presentacion.menu_reportes import menu_reportes


def menu_principal():
    while True:
        print("\n=== ECOTECH ===")
        print("1. Empleados\n2. Departamentos\n3. Reportes\n0. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            menu_empleados()
        elif opcion == "2":
            menu_departamentos()
        elif opcion == "3":
            menu_reportes()
        elif opcion == "0":
            print("Hasta luego.")
            break
        else:
            print("Elige 0, 1, 2 o 3.")