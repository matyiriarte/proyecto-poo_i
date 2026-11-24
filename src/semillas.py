
from dominio.departamento import Departamento
from dominio.empleado import Empleado
from persistencia.crear_bd import crear_tablas
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO

DEPARTAMENTOS = ["Soporte", "Ventas"]

EMPLEADOS = [
    ("Ana Torres", "ana.torres@ecotech.cl", "Soporte"),
    ("Luis Soto", "luis.soto@ecotech.cl", "Soporte"),
    ("Marta Díaz", "marta.diaz@ecotech.cl", "Ventas"),
]


def sembrar_departamentos():
    existentes = {d.nombre: d for d in DepartamentoDAO.listar()}
    creados = 0
    for nombre in DEPARTAMENTOS:
        if nombre not in existentes:
            existentes[nombre] = DepartamentoDAO.insertar(Departamento(nombre))
            creados += 1
    print(f"Departamentos: {creados} creados, {len(DEPARTAMENTOS) - creados} ya existían.")
    return existentes


def sembrar_empleados(departamentos):
    existentes = {e.correo: e for e in EmpleadoDAO.listar()}
    creados = 0
    for nombre, correo, nombre_dep in EMPLEADOS:
        empleado = existentes.get(correo)
        if empleado is None:
            empleado = EmpleadoDAO.insertar(Empleado(nombre, correo))
            creados += 1
        actual = EmpleadoDAO.buscar_por_id(empleado.id)
        departamento = departamentos[nombre_dep]
        if actual.departamento is None or actual.departamento.id != departamento.id:
            departamento.agregar_empleado(actual)
            EmpleadoDAO.actualizar_departamento(actual)
    print(f"Empleados: {creados} creados, {len(EMPLEADOS) - creados} ya existían.")


if __name__ == "__main__":
    crear_tablas()
    departamentos = sembrar_departamentos()
    sembrar_empleados(departamentos)
    print("Semillas listas.")