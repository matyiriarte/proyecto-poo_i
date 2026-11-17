# src/dominio/empleado.py
class Empleado:
    MIN_NOMBRE = 2
    MAX_NOMBRE = 80
    MIN_CORREO = 5
    MAX_CORREO = 150

    def __init__(self, nombre, correo, id=None):
        self.id = id
        self.nombre = nombre
        self.correo = correo

    @staticmethod
    def validar_nombre(nombre):
        if not isinstance(nombre, str):
            raise ValueError("El nombre debe ser texto.")
        nombre = nombre.strip()
        if not (Empleado.MIN_NOMBRE <= len(nombre) <= Empleado.MAX_NOMBRE):
            raise ValueError("El nombre debe tener entre 2 y 80 caracteres.")
        return nombre

    @staticmethod
    def validar_correo(correo):
        if not isinstance(correo, str):
            raise ValueError("El correo debe ser texto.")
        correo = correo.strip()
        if not (Empleado.MIN_CORREO <= len(correo) <= Empleado.MAX_CORREO):
            raise ValueError("El correo debe tener entre 5 y 150 caracteres.")
        if " " in correo:
            raise ValueError("El correo no puede tener espacios.")
        if correo.count("@") != 1:
            raise ValueError("El correo debe tener un solo @.")
        usuario, dominio = correo.split("@")
        if not usuario:
            raise ValueError("El correo requiere un usuario antes del @.")
        partes = dominio.split(".")
        if len(partes) < 2 or "" in partes:
            raise ValueError("El correo requiere un dominio con punto, por ejemplo ecotech.cl.")
        return correo

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = self.validar_nombre(valor)

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        self._correo = self.validar_correo(valor)

    def mostrar_datos(self) -> str:
        return f"{self.nombre} - {self.correo}"
