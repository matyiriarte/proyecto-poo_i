# src/main.py
from dominio.empleado import Empleado
from persistencia.crear_bd import crear_tablas
from persistencia.empleado_dao import EmpleadoDAO

crear_tablas()

# 1. Validación: el dominio rechaza datos incorrectos
try:
    Empleado(" ", "ana@ecotech.cl")
except ValueError as error:
    print(f"No se pudo crear el empleado: {error}")

try:
    Empleado("Ana Torres", "ana@")
except ValueError as error:
    print(f"No se pudo crear el empleado: {error}")

# 2. Empleado válido: id antes y después del INSERT
empleado = Empleado("  Ana Torres  ", "ana@ecotech.cl")
print(f"Datos válidos: '{empleado.nombre}'")   # strip() quita los espacios
print("Antes:", empleado.id)                    # None
EmpleadoDAO.insertar(empleado)
print("Después:", empleado.id)                  # id generado por la BD

# 3. Listar: cada fila se reconstruye como objeto Empleado
empleados = EmpleadoDAO.listar()
if not empleados:
    print("Todavía no hay empleados registrados.")
else:
    for e in empleados:
        print(f"{e.id}: {e.nombre} - {e.correo}")

# 4. Buscar por ID: existe y no existe
for id_buscado in (empleado.id, 9999):
    encontrado = EmpleadoDAO.buscar_por_id(id_buscado)
    if encontrado is None:
        print(f"No existe un empleado con ID {id_buscado}.")
    else:
        print(f"Encontrado: {encontrado.mostrar_datos()}")
