# src/persistencia/departamento_dao.py
from dominio.departamento import Departamento
from dominio.empleado import Empleado
from persistencia.conexion import abrir_conexion, obtener_marcador


class DepartamentoDAO:
    @staticmethod
    def insertar(departamento):
        sql = f"INSERT INTO departamento (nombre) VALUES ({obtener_marcador()})"
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (departamento.nombre,))
            conexion.commit()
            departamento.id = cursor.lastrowid
            return departamento
        finally:
            conexion.close()

    @staticmethod
    def listar():
        sql = "SELECT id, nombre FROM departamento ORDER BY id"
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql)
            filas = cursor.fetchall()
        finally:
            conexion.close()

        departamentos = []
        for id_dep, nombre in filas:
            departamentos.append(Departamento(nombre, id=id_dep))
        return departamentos

    @staticmethod
    def buscar_por_id(id_departamento):
        sql = f"SELECT id, nombre FROM departamento WHERE id = {obtener_marcador()}"
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (id_departamento,))
            fila = cursor.fetchone()
        finally:
            conexion.close()

        if fila is None:
            return None
        id_dep, nombre = fila
        return Departamento(nombre, id=id_dep)

    @staticmethod
    def actualizar(departamento):
        marcador = obtener_marcador()
        sql = f"UPDATE departamento SET nombre = {marcador} WHERE id = {marcador}"
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (departamento.nombre, departamento.id))
            conexion.commit()
            return cursor.rowcount
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_departamento):
        sql = f"DELETE FROM departamento WHERE id = {obtener_marcador()}"
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (id_departamento,))
            conexion.commit()
            return cursor.rowcount
        finally:
            conexion.close()

    @staticmethod
    def buscar_con_empleados(id_departamento):
        # LEFT JOIN: trae el departamento aunque no tenga empleados
        sql = f"""
            SELECT d.id, d.nombre, e.id, e.nombre, e.correo
            FROM departamento d
            LEFT JOIN empleado e ON e.departamento_id = d.id
            WHERE d.id = {obtener_marcador()}
            ORDER BY e.id
        """
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (id_departamento,))
            filas = cursor.fetchall()
        finally:
            conexion.close()

        if not filas:
            return None
        departamento = Departamento(filas[0][1], id=filas[0][0])
        for _, _, id_emp, nombre, correo in filas:
            if id_emp is not None:
                empleado = Empleado(nombre, correo, id=id_emp)
                departamento.agregar_empleado(empleado)
        return departamento