import os
import sqlite3
import pymysql
from dotenv import load_dotenv

load_dotenv()

ERRORES_INTEGRIDAD = (sqlite3.IntegrityError, pymysql.err.IntegrityError)
ERRORES_OPERACION = (sqlite3.OperationalError, pymysql.err.OperationalError)


def obtener_motor():
    return os.getenv("DB_ENGINE", "sqlite").lower()


def obtener_marcador():
    return "?" if obtener_motor() == "sqlite" else "%s"


def abrir_conexion():
    motor = obtener_motor()

    if motor == "sqlite":
        conexion = sqlite3.connect(os.getenv("DB_NAME", "ecotech.db"))
        conexion.execute("PRAGMA foreign_keys = ON")  # SQLite no revisa las FK si no se activa
        return conexion
    if motor == "mysql":
        return pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
        )
    raise ValueError(f"Motor no soportado: {motor}")
