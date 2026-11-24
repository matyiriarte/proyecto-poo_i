from dominio.usuario import Usuario
from persistencia.conexion import abrir_conexion, obtener_marcador

class UsuarioDAO:
    @staticmethod
    def insertar(usuario):
        marcador = obtener_marcador()
        sql = f"""
            INSERT INTO usuario (empleado_id, nombre_usuario, password_hash)
            VALUES ({marcador}, {marcador}, {marcador})
        """
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (usuario.empleado_id, usuario.nombre_usuario, usuario.password_hash))
            conexion.commit()
            usuario.id = cursor.lastrowid
            return usuario
        finally:
            conexion.close()

    @staticmethod
    def buscar_por_nombre(nombre_usuario):
        sql = f"""
            SELECT id, empleado_id, nombre_usuario, password_hash
            FROM usuario WHERE nombre_usuario = {obtener_marcador()}
        """
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (nombre_usuario,))
            fila = cursor.fetchone()
        finally:
            conexion.close()

        if fila is None:
            return None
        id_usuario, empleado_id, nombre, password_hash = fila
        return Usuario(nombre, password_hash, empleado_id, id=id_usuario)