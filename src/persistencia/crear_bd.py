# src/persistencia/crear_bd.py
from persistencia.conexion import abrir_conexion, obtener_motor


def crear_tablas():
    conexion = abrir_conexion()
    cursor = conexion.cursor()

    if obtener_motor() == "sqlite":
        sql_departamento = """
            CREATE TABLE IF NOT EXISTS departamento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE
            )
        """
        sql_empleado = """
            CREATE TABLE IF NOT EXISTS empleado (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT NOT NULL UNIQUE,
                departamento_id INTEGER,
                FOREIGN KEY (departamento_id) REFERENCES departamento(id)
            )
        """
    else:
        sql_departamento = """
            CREATE TABLE IF NOT EXISTS departamento (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nombre VARCHAR(80) NOT NULL UNIQUE
            )
        """
        sql_empleado = """
            CREATE TABLE IF NOT EXISTS empleado (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nombre VARCHAR(100) NOT NULL,
                correo VARCHAR(150) NOT NULL UNIQUE,
                departamento_id INT NULL,
                FOREIGN KEY (departamento_id) REFERENCES departamento(id)
            )
        """

    cursor.execute(sql_departamento)  # primero departamento: empleado lo referencia
    cursor.execute(sql_empleado)
    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    crear_tablas()
    print("Base de datos preparada correctamente.")
