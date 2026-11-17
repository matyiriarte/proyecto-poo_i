# src/persistencia/empleado_dao.py
from dominio.empleado import Empleado
from persistencia.conexion import abrir_conexion, obtener_marcador


class EmpleadoDAO:
    @staticmethod
    def insertar(empleado):
        marcador = obtener_marcador()
        sql = f"""
            INSERT INTO empleado (nombre, correo)
            VALUES ({marcador}, {marcador})
        """
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (empleado.nombre, empleado.correo))
            conexion.commit()
            empleado.id = cursor.lastrowid
            return empleado
        finally:
            conexion.close()

    @staticmethod
    def listar():
        sql = "SELECT id, nombre, correo FROM empleado ORDER BY id"
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql)
            filas = cursor.fetchall()
        finally:
            conexion.close()

        empleados = []
        for id_empleado, nombre, correo in filas:
            empleados.append(Empleado(nombre=nombre, correo=correo, id=id_empleado))
        return empleados

    @staticmethod
    def buscar_por_id(id_empleado):
        sql = (
            "SELECT id, nombre, correo "
            f"FROM empleado WHERE id = {obtener_marcador()}"
        )
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (id_empleado,))
            fila = cursor.fetchone()
        finally:
            conexion.close()

        if fila is None:
            return None
        id_empleado, nombre, correo = fila
        return Empleado(nombre=nombre, correo=correo, id=id_empleado)
