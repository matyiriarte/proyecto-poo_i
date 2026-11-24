import logging

from dominio.empleado import Empleado
from persistencia.conexion import ERRORES_INTEGRIDAD, ERRORES_OPERACION
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO

logger = logging.getLogger(__name__)


def guardar_empleado(empleado):
    try:
        EmpleadoDAO.insertar(empleado)
    except ERRORES_INTEGRIDAD:
        logger.exception("Restricción de BD al registrar.")
        print("Ya existe un empleado con ese correo.")
    except ERRORES_OPERACION:
        logger.exception("Fallo al registrar en la BD.")
        print("No se pudo completar la operación.")
    else:
        print(f"Empleado registrado. ID: {empleado.id}")


def solicitar_id(mensaje="ID del empleado: "):
    while True:
        texto = input(mensaje).strip()
        try:
            id_buscado = int(texto)
            if id_buscado <= 0:
                raise ValueError("El ID debe ser positivo.")
        except ValueError:
            print("Ingresa un entero mayor que 0.")
        else:
            return id_buscado


def solicitar_nombre():
    while True:
        valor = input("Nombre: ")
        try:
            return Empleado.validar_nombre(valor)
        except ValueError as error:
            print(f"Nombre inválido: {error}")


def solicitar_correo():
    while True:
        valor = input("Correo: ")
        try:
            return Empleado.validar_correo(valor)
        except ValueError as error:
            print(f"Correo inválido: {error}")


def crear_empleado():
    nombre = solicitar_nombre()
    correo = solicitar_correo()
    empleado = Empleado(nombre=nombre, correo=correo)
    guardar_empleado(empleado)


def listar_empleados():
    empleados = EmpleadoDAO.listar()
    if not empleados:
        print("Todavía no hay empleados registrados.")
    else:
        for empleado in empleados:
            print(f"{empleado.id}: {empleado.nombre} - {empleado.correo}")


def buscar_empleado():
    empleado = EmpleadoDAO.buscar_por_id(solicitar_id())
    if empleado is None:
        print("No existe un empleado con ese ID.")
    else:
        print(f"{empleado.id}: {empleado.nombre} - {empleado.correo}")


def actualizar_empleado():
    empleado = EmpleadoDAO.buscar_por_id(solicitar_id())
    if empleado is None:
        print("No existe un empleado con ese ID.")
        return
    print(f"Actual: {empleado.nombre} - {empleado.correo}")
    empleado.nombre = solicitar_nombre()
    empleado.correo = solicitar_correo()
    try:
        filas = EmpleadoDAO.actualizar(empleado)
    except ERRORES_INTEGRIDAD:
        logger.exception("Restricción de BD al actualizar.")
        print("Ya existe otro empleado con ese correo.")
        return
    if filas == 1:
        print("Empleado actualizado correctamente.")
    else:
        print("Vuelve a consultar el estado del empleado.")


def eliminar_empleado():
    empleado = EmpleadoDAO.buscar_por_id(solicitar_id())
    if empleado is None:
        print("No existe un empleado con ese ID.")
        return
    print(f"Vas a eliminar a: {empleado.nombre} - {empleado.correo}")
    confirmacion = input("¿Confirmas? (s/n): ").strip().lower()
    if confirmacion != "s":
        print("Eliminación cancelada.")
        return
    try:
        filas = EmpleadoDAO.eliminar(empleado.id)
    except ERRORES_INTEGRIDAD:
        logger.exception("Restricción de BD al eliminar empleado.")
        print("No se puede eliminar: el empleado tiene una cuenta de usuario.")
        return
    if filas == 1:
        print("Empleado eliminado.")
    else:
        print("No se pudo eliminar. Vuelve a consultar.")


def seleccionar_departamento():
    departamentos = DepartamentoDAO.listar()
    if not departamentos:
        print("Primero registra un departamento.")
        return None
    for departamento in departamentos:
        print(f"{departamento.id}: {departamento.nombre}")
    departamento = DepartamentoDAO.buscar_por_id(solicitar_id("ID del departamento: "))
    if departamento is None:
        print("No existe ese departamento.")
    return departamento


def asignar_departamento():
    empleado = EmpleadoDAO.buscar_por_id(solicitar_id())
    if empleado is None:
        print("No existe ese empleado.")
        return
    departamento = seleccionar_departamento()
    if departamento is None:
        return
    departamento.agregar_empleado(empleado)
    filas = EmpleadoDAO.actualizar_departamento(empleado)
    if filas == 1:
        print(f"{empleado.nombre} asignado a {departamento.nombre}.")
    else:
        print("Consulta nuevamente para comprobar el resultado.")


def menu_empleados():
    while True:
        print("\n--- EMPLEADOS ---")
        print("1. Registrar\n2. Listar\n3. Buscar\n4. Actualizar")
        print("5. Eliminar\n6. Asignar departamento\n0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            crear_empleado()
        elif opcion == "2":
            listar_empleados()
        elif opcion == "3":
            buscar_empleado()
        elif opcion == "4":
            actualizar_empleado()
        elif opcion == "5":
            eliminar_empleado()
        elif opcion == "6":
            asignar_departamento()
        elif opcion == "0":
            break
        else:
            print("Elige una opción del 0 al 6.")