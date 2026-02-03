from dotenv import load_dotenv, find_dotenv
import os
import mysql.connector
from typing import List, Dict, Any, cast
from mysql.connector.cursor import MySQLCursorDict

# Carga .env desde la raíz
load_dotenv(find_dotenv())

def get_connection():
    """
    Crea y retorna una conexión a la base de datos MySQL.
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "glowy_db"),
        port=int(os.getenv("DB_PORT", "3306")),
        charset="utf8mb4"
    )


def fetch_all_productos() -> List[Dict[str, Any]]:
    """
    Ejecuta SELECT * FROM productos y devuelve una lista de dicts.
    """
    conn = None
    try:
        conn = get_connection()
        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)  # type: ignore[assignment]
        try:
            cur.execute(
                "SELECT id, nombre, categoria, precio, stock, descripcion FROM productos;"
            )
            rows = cast(List[Dict[str, Any]], cur.fetchall())
            return rows
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()


def fetch_producto_by_id(producto_id: int) -> Dict[str, Any] | None:
    """
    Obtiene un producto por su ID.
    Retorna un dict con los datos del producto o None si no existe.
    """
    conn = None
    try:
        conn = get_connection()
        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)  # type: ignore[assignment]
        try:
            cur.execute(
                "SELECT id, nombre, categoria, precio, stock, descripcion FROM productos WHERE id = %s",
                (producto_id,)
            )
            result = cur.fetchone()
            return dict(result) if result else None
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()


def insert_producto(
    nombre: str, 
    categoria: str, 
    precio: float,
    stock: int,
    descripcion: str | None = None
) -> int:
    """
    Inserta un nuevo producto en la base de datos.
    Retorna el ID del producto insertado.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO productos (nombre, categoria, precio, stock, descripcion)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (nombre, categoria, precio, stock, descripcion)
            )
            conn.commit()
            return cur.lastrowid or 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()


def update_producto(
    producto_id: int,
    nombre: str,
    categoria: str,
    precio: float,
    stock: int,
    descripcion: str | None = None
) -> bool:
    """
    Actualiza los datos de un producto existente.
    Retorna True si se actualizó correctamente, False si no se encontró.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                UPDATE productos 
                SET nombre = %s, categoria = %s, precio = %s, stock = %s, descripcion = %s
                WHERE id = %s
                """,
                (nombre, categoria, precio, stock, descripcion, producto_id)
            )
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()


def delete_producto(producto_id: int) -> bool:
    """
    Elimina un producto de la base de datos por su ID.
    Retorna True si se eliminó correctamente, False si no se encontró.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "DELETE FROM productos WHERE id = %s",
                (producto_id,)
            )
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()
