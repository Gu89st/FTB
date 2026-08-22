"""
Diagnóstico de solo lectura: muestra todas las secciones (con su tarea)
y cuántas notas tiene cada una, más el detalle de cada nota y a qué
seccion_id apunta. No modifica nada.

Uso:
    python diagnostico.py
"""
import sqlite3
import os

DB_PATH = "ftb_usuarios.db"

if not os.path.exists(DB_PATH):
    print(f"No se encontró {DB_PATH} en este directorio.")
    raise SystemExit(1)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print("=== TAREAS (categorias) ===")
cur.execute("SELECT id, nombre FROM categorias")
for fila in cur.fetchall():
    print(f"  id={fila[0]}  nombre={fila[1]}")

print("\n=== SECCIONES ===")
cur.execute("""
    SELECT secciones.id, secciones.nombre, categorias.nombre
    FROM secciones
    LEFT JOIN categorias ON secciones.categoria_id = categorias.id
""")
secciones = cur.fetchall()
for sec_id, sec_nombre, cat_nombre in secciones:
    cur.execute("SELECT COUNT(*) FROM notas WHERE seccion_id = ?", (sec_id,))
    cantidad_notas = cur.fetchone()[0]
    print(f"  id={sec_id}  nombre='{sec_nombre}'  tarea='{cat_nombre}'  notas={cantidad_notas}")

print("\n=== NOTAS ===")
cur.execute("SELECT id, titulo, seccion_id, categoria_id FROM notas")
for nota_id, titulo, seccion_id, categoria_id_legado in cur.fetchall():
    print(f"  id={nota_id}  titulo='{titulo}'  seccion_id={seccion_id}  categoria_id(legado)={categoria_id_legado}")

conn.close()