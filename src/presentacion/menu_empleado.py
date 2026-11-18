from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO

def guardar_empleado(empleado):
    try:
        EmpleadoDAO.insertar(empleado)
    except IntegrityError:
        logger.exception("Restricción de BD al registrar.")
        print("Revisa las restricciones de los datos.")
    except OperationalError:
        logger.exception("Fallo al registrar en la BD.")
        print("No se pudo completar la operación.")
    else:
        print(f"Empleado registrado. ID: {empleado.id}")

def solicitar_id():
    while True:
        texto = input("ID del empleado: ").strip()
        try:
            id_empleado = int(texto)
            if id_empleado <= 0:
                raise ValueError("El ID debe ser positivo.")
        except ValueError:
            print("Ingresa un entero mayor que 0.") 
        else:       
            return id_empleado

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
    EmpleadoDAO.insertar(empleado)
    print(f"Empleado registrado. ID: {empleado.id}")


def listar_empleados():
    empleados = EmpleadoDAO.listar()
    if not empleados:
        print("Todavía no hay empleados registrados.")
    for empleado in empleados:
        print(f"{empleado.id}: {empleado.nombre} - {empleado.correo}")


def menu_empleados():
    while True:
        print("\n1. Registrar\n2. Listar\n0. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            crear_empleado()
        elif opcion == "2":
            listar_empleados()
        elif opcion == "0":
            break
        else:
            print("Elige 0, 1 o 2.")
