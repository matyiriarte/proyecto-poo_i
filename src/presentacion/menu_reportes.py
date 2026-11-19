from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from presentacion.menu_empleado import solicitar_id


def reporte_departamentos():
    departamentos = DepartamentoDAO.listar()
    if not departamentos:
        print("Todavía no hay departamentos registrados.")
        return
    for dep in departamentos:
        departamento = DepartamentoDAO.buscar_con_empleados(dep.id)
        print(f"\n{departamento.nombre}")
        if not departamento.empleados:
            print("  (sin empleados)")
        for empleado in departamento.empleados:
            print(f"  {empleado.id}: {empleado.nombre} - {empleado.correo}")


def reporte_empleado():
    empleado = EmpleadoDAO.buscar_por_id(solicitar_id())
    if empleado is None:
        print("No existe un empleado con ese ID.")
        return
    if empleado.departamento is None:
        nombre_departamento = "Sin asignar"
    else:
        nombre_departamento = empleado.departamento.nombre
    print(f"ID: {empleado.id}")
    print(f"Nombre: {empleado.nombre}")
    print(f"Correo: {empleado.correo}")
    print(f"Departamento: {nombre_departamento}")


def menu_reportes():
    while True:
        print("\n--- REPORTES ---")
        print("1. Departamentos y sus empleados\n2. Información de un empleado\n0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            reporte_departamentos()
        elif opcion == "2":
            reporte_empleado()
        elif opcion == "0":
            break
        else:
            print("Elige 0, 1 o 2.")