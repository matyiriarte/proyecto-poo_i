import logging

from persistencia.conexion import ERRORES_OPERACION
from persistencia.crear_bd import crear_tablas
from presentacion.menu_principal import menu_principal
from presentacion.menu_usuario import menu_inicio

logging.basicConfig(filename="errores.log", level=logging.ERROR)


def main():
    try:
        crear_tablas()
    except ERRORES_OPERACION:
        logging.exception("No se pudo preparar la base de datos.")
        print("No se pudo conectar a la base de datos.")
        print("Revisa el .env y que el servidor (XAMPP o Wamp) esté encendido.")
        return

    usuario_actual = menu_inicio()
    if usuario_actual is None:  # Sin cuenta válida, el menú no se abre
        print("Hasta luego.")
        return
    menu_principal()
    usuario_actual = None


if __name__ == "__main__":
    main()