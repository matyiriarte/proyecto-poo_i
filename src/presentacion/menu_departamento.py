import logging

from dominio.departamento import Departamento
from persistencia.conexion import ERRORES_INTEGRIDAD, ERRORES_OPERACION
from persistencia.departamento_dao import DepartamentoDAO
from presentacion.menu_empleado import solicitar_id

logger = logging.getLogger(__name__)


def solicitar_nombre_departamento():
    while True:
        valor = input("Nombre del departamento: ")
        try:
            return Departamento.validar_nombre(valor)
        except ValueError as error:
            print(f"Nombre inválido: {error}")


def crear_departamento():
    departamento = Departamento(solicitar_nombre_departamento())
    try:
        DepartamentoDAO.insertar(departamento)
    except ERRORES_INTEGRIDAD:
        logger.exception("Restricción de BD al registrar departamento.")
        print("Ya existe un departamento con ese nombre.")
    except ERRORES_OPERACION:
        logger.exception("Fallo al registrar departamento.")
        print("No se pudo completar la operación.")
    else:
        print(f"Departamento registrado. ID: {departamento.id}")


def listar_departamentos():
    departamentos = DepartamentoDAO.listar()
    if not departamentos:
        print("Todavía no hay departamentos registrados.")
    else:
        for departamento in departamentos:
            print(f"{departamento.id}: {departamento.nombre}")


def buscar_departamento():
    departamento = DepartamentoDAO.buscar_por_id(solicitar_id("ID del departamento: "))
    if departamento is None:
        print("No existe un departamento con ese ID.")
    else:
        print(f"{departamento.id}: {departamento.nombre}")


def actualizar_departamento():
    departamento = DepartamentoDAO.buscar_por_id(solicitar_id("ID del departamento: "))
    if departamento is None:
        print("No existe un departamento con ese ID.")
        return
    print(f"Actual: {departamento.nombre}")
    departamento.nombre = solicitar_nombre_departamento()
    try:
        filas = DepartamentoDAO.actualizar(departamento)
    except ERRORES_INTEGRIDAD:
        logger.exception("Restricción de BD al actualizar departamento.")
        print("Ya existe otro departamento con ese nombre.")
        return
    if filas == 1:
        print("Departamento actualizado correctamente.")
    else:
        print("Vuelve a consultar el estado del departamento.")


def eliminar_departamento():
    departamento = DepartamentoDAO.buscar_por_id(solicitar_id("ID del departamento: "))
    if departamento is None:
        print("No existe un departamento con ese ID.")
        return
    confirmacion = input(f"¿Eliminar {departamento.nombre}? (s/n): ").strip().lower()
    if confirmacion != "s":
        print("Eliminación cancelada.")
        return
    try:
        DepartamentoDAO.eliminar(departamento.id)
    except ERRORES_INTEGRIDAD:
        logger.exception("Restricción de BD al eliminar departamento.")
        print("No se puede eliminar: tiene empleados asignados.")
    else:
        print("Departamento eliminado.")


def menu_departamentos():
    while True:
        print("\n--- DEPARTAMENTOS ---")
        print("1. Registrar\n2. Listar\n3. Buscar\n4. Actualizar\n5. Eliminar\n0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            crear_departamento()
        elif opcion == "2":
            listar_departamentos()
        elif opcion == "3":
            buscar_departamento()
        elif opcion == "4":
            actualizar_departamento()
        elif opcion == "5":
            eliminar_departamento()
        elif opcion == "0":
            break
        else:
            print("Elige una opción del 0 al 5.")