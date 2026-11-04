class empleado:

    def __init__(self, nombre:str, correostr:str):
        self.nombre = nombre
        self.correo = correo

    def msotrar_datos(self) -> str: 
        return f" nombre: {self.nombre} correo: {self.correo}"