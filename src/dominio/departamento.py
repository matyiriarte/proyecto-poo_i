# src/dominio/departamento.py
class Departamento:
    MIN_NOMBRE = 2
    MAX_NOMBRE = 80

    def __init__(self, nombre, id=None):
        self.id = id
        self.nombre = nombre
        self._empleados = []
    
    @staticmethod
    def validar_nombre(nombre):
        if not isinstance(nombre, str):
            raise ValueError("El nombre debe ser texto.")
        nombre = nombre.strip()
        if not (Departamento.MIN_NOMBRE <= len(nombre) <= Departamento.MAX_NOMBRE):
            raise ValueError("El nombre debe tener entre 2 y 80 caracteres.")
        return nombre

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = self.validar_nombre(valor)

    @property
    def empleados(self):
        return tuple(self._empleados)

    def agregar_empleado(self, empleado):
        empleado.departamento = self
        if empleado not in self._empleados:
            self._empleados.append(empleado)