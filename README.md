# EcoTech · Gestión de empleados en consola

---

## Funcionalidades

- **Inicio de sesión** con contraseña cifrada mediante hash bcrypt y un máximo de 3 intentos por ejecución.
- **CRUD de empleados:** registrar, listar, buscar, actualizar y eliminar.
- **CRUD de departamentos:** registrar, listar, buscar, actualizar y eliminar.
- **Asignación** de empleados a departamentos, guardada en la base de datos.
- **Reportes:** departamentos con sus empleados, información de un empleado y reporte general.
- **Dos motores de base de datos:** SQLite o MySQL, elegidos desde el archivo `.env` sin cambiar el código.
- **Datos de prueba (semillas)** que se pueden cargar varias veces sin duplicarse.

## Tecnologías

| Herramienta | Uso |
| --- | --- |
| Python 3.10 o superior | Lenguaje del proyecto |
| SQLite | Base de datos en un archivo local (incluida en Python) |
| MySQL / MariaDB | Base de datos en servidor (XAMPP o Wamp) |
| PyMySQL | Conexión a MySQL |
| python-dotenv | Lectura de la configuración desde `.env` |
| bcrypt | Hash seguro de contraseñas |

---

## Instalación

```bash
git clone https://github.com/matyiriarte/proyecto-poo_i.git
cd proyecto-poo_i

python -m venv .venv
.venv\Scripts\activate          # Windows (PowerShell)
# source .venv/bin/activate     # Linux / macOS / Git Bash

python -m pip install -r requirements.txt
copy .env.example .env          # en Linux/macOS: cp .env.example .env
```

### Configurar la base de datos

**SQLite** (por defecto, no requiere nada más). En `.env`:

```
DB_ENGINE=sqlite
DB_NAME=ecotech.db
```

**MySQL** con XAMPP o Wamp:

1. Encender el servicio **MySQL** en el panel de XAMPP/Wamp.
2. En `http://localhost/phpmyadmin`, crear la base de datos `ecotech` (cotejamiento `utf8mb4_general_ci`).
3. En `.env`:

```
DB_ENGINE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ecotech
DB_USER=root
DB_PASSWORD=
```

Las tablas se crean automáticamente al ejecutar el programa.

## Uso

Siempre desde la carpeta raíz del proyecto:

```bash
python src/semillas.py   # opcional: carga 2 departamentos y 3 empleados de prueba
python src/main.py
```

La primera vez no hay cuentas: en la pantalla de acceso elige **2. Crear cuenta** con el ID de un empleado existente y luego **1. Iniciar sesión**. La contraseña no se muestra al escribirla.

```
ACCESO: 1 Iniciar sesión · 2 Crear cuenta · 0 Salir
└── ECOTECH (solo con una cuenta válida)
    ├── 1 Empleados ....... registrar, listar, buscar, actualizar, eliminar, asignar departamento
    ├── 2 Departamentos ... registrar, listar, buscar, actualizar, eliminar
    ├── 3 Reportes ........ departamentos y sus empleados, información de un empleado, reporte general
    └── 0 Salir
```

---

## Arquitectura

El código está separado en capas; cada una tiene una sola responsabilidad.

| Capa | Carpeta | Responsabilidad |
| --- | --- | --- |
| Dominio | `src/dominio/` | Clases del problema y sus reglas de validación. No conoce la base de datos ni la consola. |
| Persistencia | `src/persistencia/` | Conexión, creación de tablas y DAO con todo el SQL. |
| Servicios | `src/servicios/` | Hash de contraseñas y verificación del acceso. |
| Presentación | `src/presentacion/` | Menús de consola: piden datos y muestran resultados. |

```
proyecto-poo_i/
├── docs/
│   └── UML_base_v1.md            # diagrama de clases y decisiones de diseño
├── src/
│   ├── dominio/
│   │   ├── empleado.py           # Empleado: validación de nombre y correo
│   │   ├── departamento.py       # Departamento: colección de empleados
│   │   ├── reporte.py            # ReporteEmpleados y ReportePorDepartamento
│   │   └── usuario.py            # Usuario: cuenta vinculada a un empleado
│   ├── persistencia/
│   │   ├── conexion.py           # abre SQLite o MySQL según .env
│   │   ├── crear_bd.py           # tablas departamento, empleado y usuario
│   │   ├── empleado_dao.py
│   │   ├── departamento_dao.py
│   │   └── usuario_dao.py
│   ├── servicios/
│   │   └── autenticacion.py      # crear_hash, registrar_usuario, autenticar
│   ├── presentacion/
│   │   ├── menu_usuario.py       # pantalla de acceso
│   │   ├── menu_principal.py
│   │   ├── menu_empleado.py
│   │   ├── menu_departamento.py
│   │   └── menu_reportes.py
│   ├── semillas.py
│   └── main.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### Modelo de datos

| Tabla | Columnas principales | Restricciones |
| --- | --- | --- |
| `departamento` | `id`, `nombre` | PK, `nombre` UNIQUE |
| `empleado` | `id`, `nombre`, `correo`, `departamento_id` | PK, `correo` UNIQUE, FK a `departamento` (puede ser nula) |
| `usuario` | `id`, `empleado_id`, `nombre_usuario`, `password_hash` | PK, FK a `empleado` UNIQUE, `nombre_usuario` UNIQUE |

---

## Conceptos de POO aplicados

- **Encapsulamiento:** nombre, correo y departamento son atributos privados que se modifican mediante `@property`; cada setter valida antes de guardar, así que un objeto nunca queda con datos inválidos.
- **Asociación:** un `Departamento` tiene 0 o muchos `Empleado` y un empleado pertenece a 0 o 1 departamento. `agregar_empleado()` mantiene ambos lados de la relación y la colección se expone como tupla de solo lectura.
- **Herencia y polimorfismo:** `ReportePorDepartamento` hereda de `ReporteEmpleados`, reutiliza su constructor con `super()` y redefine `generar()`. El menú llama a `generar()` sobre una lista con ambos tipos de reporte.
- **Asociación, no herencia, entre Usuario y Empleado:** una cuenta pertenece a un empleado; no *es* un empleado.
- **Import circular evitado:** `departamento.py` importa `Empleado` dentro de `agregar_empleado()` y no al inicio del archivo.

## Seguridad

- Las contraseñas se guardan **solo como hash bcrypt** con sal aleatoria; se verifican con `checkpw` y nunca se recuperan.
- La contraseña se pide con `getpass`, sin mostrarla en pantalla.
- **Consultas parametrizadas** en todos los DAO, para evitar inyección SQL.
- El mismo mensaje para usuario inexistente y clave incorrecta, para no revelar qué cuentas existen.
- **Máximo 3 intentos** de inicio de sesión por ejecución.
- Un fallo de la base de datos nunca se interpreta como acceso exitoso.
- `.env`, la base local y `errores.log` están excluidos del repositorio.

## Manejo de errores

| Situación | Respuesta del programa |
| --- | --- |
| Dato inválido (`ValueError`) | Se vuelve a pedir solo el campo incorrecto |
| Correo, departamento o usuario repetido (`IntegrityError`) | Mensaje explicando el duplicado |
| Eliminar un departamento con empleados o un empleado con cuenta (`IntegrityError` por FK) | Se rechaza y se explica el motivo |
| Base de datos no disponible (`OperationalError`) | Mensaje claro, sin cerrar el programa con un error técnico |

El detalle técnico de cada error queda registrado en `errores.log`.

## Semillas

`python src/semillas.py` inserta 2 departamentos (Soporte y Ventas) y 3 empleados ficticios. Antes de insertar consulta la base de datos y solo agrega lo que falta, por lo que puede ejecutarse varias veces sin duplicar registros:

```
Departamentos: 2 creados, 0 ya existían.     ← primera ejecución
Departamentos: 0 creados, 2 ya existían.     ← segunda ejecución
```

Las restricciones `UNIQUE` de la base de datos respaldan la misma regla.

---

## Pruebas realizadas

Probado con SQLite y con MySQL.

| Caso | Esperado | Observado |
| --- | --- | --- |
| Usuario inexistente | Rechazo | "Usuario o contraseña incorrectos." |
| Clave incorrecta | Rechazo | "Usuario o contraseña incorrectos." |
| Tres intentos fallidos | Termina sin abrir el menú | "Demasiados intentos fallidos." |
| Login correcto | Entra y muestra el empleado | "Sesión iniciada: pisco · Marta Díaz (marta.diaz@ecotech.cl)" |
| Fallo de BD al autenticar | No entra | "No se pudo verificar el acceso." |
| Correo repetido | Rechazo | "Ya existe un empleado con ese correo." |
| Eliminar empleado con cuenta | Rechazo por FK | "No se puede eliminar: el empleado tiene una cuenta de usuario." |
| Eliminar departamento con empleados | Rechazo por FK | "No se puede eliminar: tiene empleados asignados." |
| Relación después de reiniciar | Se recupera desde la BD | El reporte muestra cada departamento con sus empleados |
| BD no disponible al arrancar | Mensaje, sin caerse | "No se pudo conectar a la base de datos." |
| Semillas dos veces | Sin duplicados | "0 creados" en la segunda ejecución |

## Documentación

El diagrama de clases UML y las decisiones de diseño están en [`docs/UML_base_v1.md`](docs/UML_base_v1.md).
