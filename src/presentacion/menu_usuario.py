import logging
from getpass import getpass

from dominio.usuario import Usuario
from persistencia.conexion import ERRORES_INTEGRIDAD, ERRORES_OPERACION
from persistencia.empleado_dao import EmpleadoDAO
from presentacion.menu_empleado import solicitar_id
from servicios.autenticacion import autenticar, registrar_usuario

logger = logging.getLogger(__name__)


def solicitar_login():
    nombre = input("Usuario: ")
    clave = getpass("Contraseña: ")
    try:
        usuario = autenticar(nombre, clave)
    except (TypeError, ValueError):
        print("Usuario o contraseña incorrectos.")
        return None
    except ERRORES_OPERACION:
        logger.exception("Fallo de BD al autenticar.")
        print("No se pudo verificar el acceso. Intenta más tarde.")
        return None
    if usuario is None:
        print("Usuario o contraseña incorrectos.")
        return None

    try:
        empleado = EmpleadoDAO.buscar_por_id(usuario.empleado_id)
    except ERRORES_OPERACION:
        logger.exception("Fallo de BD al recuperar el empleado de la cuenta.")
        empleado = None
    if empleado is None:
        print("No se pudo recuperar el empleado de la cuenta.")
        return None
    print(f"Sesión iniciada: {usuario.nombre_usuario} · {empleado.nombre} ({empleado.correo})")
    return usuario


def solicitar_nombre_usuario():
    while True:
        valor = input("Nombre de usuario: ")
        try:
            return Usuario.normalizar_usuario(valor)
        except (TypeError, ValueError) as error:
            print(f"Usuario inválido: {error}")


def solicitar_clave_nueva():
    while True:
        clave = getpass("Contraseña nueva: ")
        try:
            Usuario.validar_clave(clave)
        except (TypeError, ValueError) as error:
            print(f"Contraseña inválida: {error}")
            continue
        if getpass("Repite la contraseña: ") != clave:
            print("Las contraseñas no coinciden.")
            continue
        return clave


def crear_cuenta():
    empleado_id = solicitar_id("ID del empleado dueño de la cuenta: ")
    if EmpleadoDAO.buscar_por_id(empleado_id) is None:
        print("No existe un empleado con ese ID.")
        return
    nombre = solicitar_nombre_usuario()
    clave = solicitar_clave_nueva()
    try:
        usuario = registrar_usuario(nombre, clave, empleado_id)
    except ValueError as error:
        print(f"No se pudo crear la cuenta: {error}")
    except ERRORES_INTEGRIDAD:
        logger.exception("Restricción de BD al crear cuenta.")
        print("Ese nombre de usuario ya existe o el empleado ya tiene cuenta.")
    except ERRORES_OPERACION:
        logger.exception("Fallo de BD al crear cuenta.")
        print("No se pudo completar la operación.")
    else:
        print(f"Cuenta creada. ID: {usuario.id}")


MAX_INTENTOS = 3


def menu_inicio():
    intentos = 0
    while True:
        print("\n=== ECOTECH · ACCESO ===")
        print("1. Iniciar sesión\n2. Crear cuenta\n0. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            usuario = solicitar_login()
            if usuario is not None:
                return usuario
            intentos += 1
            if intentos >= MAX_INTENTOS:
                print("Demasiados intentos fallidos. Vuelve a ejecutar el programa.")
                return None
            print(f"Intentos restantes: {MAX_INTENTOS - intentos}")
        elif opcion == "2":
            crear_cuenta()
        elif opcion == "0":
            return None
        else:
            print("Elige 0, 1 o 2.")