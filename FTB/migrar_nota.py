"""
Migración de un solo uso: agrega las columnas 'descripcion' y
'fecha_evento' a la tabla 'notas' ya existente, sin perder datos.

Uso:
    python migrar_notas.py

Ejecutar desde la raíz del proyecto (donde vive ftb_usuarios.db).
"""
import sqlite3
import os

DB_PATH = "ftb_usuarios.db"

if not os.path.exists(DB_PATH):
    print(f"No se encontró {DB_PATH} en este directorio.")
    raise SystemExit(1)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("PRAGMA table_info(notas)")
columnas_actuales = {fila[1] for fila in cur.fetchall()}

if "descripcion" not in columnas_actuales:
    cur.execute("ALTER TABLE notas ADD COLUMN descripcion TEXT DEFAULT ''")
    print("Columna 'descripcion' agregada.")
else:
    print("Columna 'descripcion' ya existía, se omite.")

if "fecha_evento" not in columnas_actuales:
    cur.execute("ALTER TABLE notas ADD COLUMN fecha_evento DATE")
    print("Columna 'fecha_evento' agregada.")
else:
    print("Columna 'fecha_evento' ya existía, se omite.")

conn.commit()
conn.close()
print("Migración completada.")