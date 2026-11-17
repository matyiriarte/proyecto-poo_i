# Proyecto POO I · EcoTech

Gestión de empleados de EcoTech con Python, aplicando POO y persistencia mediante un DAO (SQLite o MySQL).
Avance hasta la **Clase 3: Empleado válido y lectura de datos**.

## Estructura
```
src/
├── dominio/
│   ├── empleado.py       # Empleado con validación de nombre y correo (@property)
│   └── departamento.py   # Departamento con colección de empleados
├── persistencia/
│   ├── conexion.py       # Abre SQLite o MySQL según DB_ENGINE
│   ├── crear_bd.py       # Crea la tabla empleado
│   └── empleado_dao.py   # insertar(), listar(), buscar_por_id()
└── main.py               # Demostración
```

## Cómo ejecutar
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python src/main.py
```

## Reglas de validación
- **Nombre:** texto, sin espacios extremos, entre 2 y 80 caracteres.
- **Correo:** entre 5 y 150 caracteres, sin espacios, un solo `@`, usuario no vacío y dominio con punto.

## Recorrido de un empleado
1. `Empleado(...)` valida y normaliza los datos; si una regla falla lanza `ValueError`.
2. `EmpleadoDAO.insertar()` guarda el registro; la BD genera el id y el DAO lo asigna con `cursor.lastrowid`.
3. `EmpleadoDAO.listar()` usa `fetchall()` y convierte cada fila en un objeto `Empleado` (devuelve `[]` si no hay registros).
4. `EmpleadoDAO.buscar_por_id()` usa `fetchone()` y devuelve un `Empleado` o `None` si el ID no existe.
