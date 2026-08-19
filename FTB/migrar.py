"""
Migración de un solo uso: agrega a la tabla 'notas' las columnas
'descripcion', 'fecha_evento', 'hora_inicio' y 'hora_fin', sin perder datos.

Uso:
    python migrar_notas.py

Ejecutar desde la raíz del proyecto (donde vive ftb_usuarios.db), con la
app cerrada.
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

columnas_nuevas = {
    "descripcion": "TEXT DEFAULT ''",
    "fecha_evento": "DATE",
    "hora_inicio": "TEXT",
    "hora_fin": "TEXT",
}

for nombre, tipo in columnas_nuevas.items():
    if nombre not in columnas_actuales:
        cur.execute(f"ALTER TABLE notas ADD COLUMN {nombre} {tipo}")
        print(f"Columna '{nombre}' agregada.")
    else:
        print(f"Columna '{nombre}' ya existía, se omite.")

conn.commit()
conn.close()
print("Migración completada.")