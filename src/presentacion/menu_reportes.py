from dominio.reporte import ReporteEmpleados, ReportePorDepartamento
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from presentacion.menu_empleado import solicitar_id


def imprimir_reportes(reportes):
    for reporte in reportes:
        print()
        print(reporte.generar())


def reporte_departamentos():
    departamentos = DepartamentoDAO.listar()
    if not departamentos:
        print("Todavía no hay departamentos registrados.")
        return
    reportes = []
    for dep in departamentos:
        departamento = DepartamentoDAO.buscar_con_empleados(dep.id)
        reportes.append(ReportePorDepartamento(departamento))
    imprimir_reportes(reportes)


def reporte_general():
    reportes = [ReporteEmpleados(EmpleadoDAO.listar())]
    for dep in DepartamentoDAO.listar():
        departamento = DepartamentoDAO.buscar_con_empleados(dep.id)
        reportes.append(ReportePorDepartamento(departamento))
    imprimir_reportes(reportes)


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
        print("1. Departamentos y sus empleados\n2. Información de un empleado")
        print("3. Reporte general (todos los reportes)\n0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            reporte_departamentos()
        elif opcion == "2":
            reporte_empleado()
        elif opcion == "3":
            reporte_general()
        elif opcion == "0":
            break
        else:
            print("Elige 0, 1, 2 o 3.")