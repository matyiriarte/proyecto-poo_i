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
        sql_usuario = """
            CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                empleado_id INTEGER NOT NULL UNIQUE,
                nombre_usuario TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                FOREIGN KEY (empleado_id) REFERENCES empleado(id)
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
        sql_usuario = """
            CREATE TABLE IF NOT EXISTS usuario (
                id INT PRIMARY KEY AUTO_INCREMENT,
                empleado_id INT NOT NULL UNIQUE,
                nombre_usuario VARCHAR(40) NOT NULL UNIQUE,
                password_hash VARCHAR(100) NOT NULL,
                FOREIGN KEY (empleado_id) REFERENCES empleado(id)
            )
        """

    cursor.execute(sql_departamento)
    cursor.execute(sql_empleado)
    cursor.execute(sql_usuario)
    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    crear_tablas()
    print("Base de datos preparada correctamente.")