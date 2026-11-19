import logging

from persistencia.crear_bd import crear_tablas
from presentacion.menu_principal import menu_principal

logging.basicConfig(filename="errores.log", level=logging.ERROR)

if __name__ == "__main__":
    crear_tablas()
    menu_principal()