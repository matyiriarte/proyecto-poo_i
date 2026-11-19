# src/persistencia/empleado_dao.py
from dominio.departamento import Departamento
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
        # LEFT JOIN: trae el empleado aunque no tenga departamento
        sql = f"""
            SELECT e.id, e.nombre, e.correo, d.id, d.nombre
            FROM empleado e
            LEFT JOIN departamento d ON e.departamento_id = d.id
            WHERE e.id = {obtener_marcador()}
        """
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (id_empleado,))
            fila = cursor.fetchone()
        finally:
            conexion.close()

        if fila is None:
            return None
        id_emp, nombre, correo, id_dep, nombre_dep = fila
        empleado = Empleado(nombre=nombre, correo=correo, id=id_emp)
        if id_dep is not None:
            empleado.departamento = Departamento(nombre_dep, id=id_dep)
        return empleado

    @staticmethod
    def actualizar(empleado):
        marcador = obtener_marcador()
        sql = f"""
            UPDATE empleado SET nombre = {marcador}, correo = {marcador}
            WHERE id = {marcador}
        """
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (empleado.nombre, empleado.correo, empleado.id))
            conexion.commit()
            return cursor.rowcount  # cuántas filas cambiaron
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_empleado):
        sql = f"DELETE FROM empleado WHERE id = {obtener_marcador()}"
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (id_empleado,))
            conexion.commit()
            return cursor.rowcount
        finally:
            conexion.close()

    @staticmethod
    def actualizar_departamento(empleado):
        marcador = obtener_marcador()
        sql = f"UPDATE empleado SET departamento_id = {marcador} WHERE id = {marcador}"
        id_dep = empleado.departamento.id if empleado.departamento else None
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (id_dep, empleado.id))
            conexion.commit()
            return cursor.rowcount
        finally:
            conexion.close()
