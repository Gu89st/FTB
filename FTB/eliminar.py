"""
Script de un solo uso para vaciar las tablas 'notas' y 'categorias'
sin tocar ninguna otra tabla de ftb_usuarios.db (p. ej. usuarios).

Uso:
    python limpiar_notas.py

Ejecutar desde la raíz del proyecto (donde vive ftb_usuarios.db).
"""
import sqlite3
import os

DB_PATH = "ftb_usuarios.db"

if not os.path.exists(DB_PATH):
    print(f"No se encontró {DB_PATH} en este directorio. "
          f"Ejecuta este script desde la raíz del proyecto.")
    raise SystemExit(1)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Mostrar qué hay antes de borrar, para confirmar
cur.execute("SELECT id, nombre, color FROM categorias")
categorias = cur.fetchall()
print("Categorías actuales:")
for c in categorias:
    print(f"  id={c[0]}  nombre={c[1]}  color={c[2]}")

cur.execute("SELECT id, titulo, categoria_id FROM notas")
notas = cur.fetchall()
print("\nNotas actuales:")
for n in notas:
    print(f"  id={n[0]}  titulo={n[1]}  categoria_id={n[2]}")

respuesta = input("\n¿Borrar TODAS las categorías y notas de arriba? (s/n): ")
if respuesta.strip().lower() == "s":
    cur.execute("DELETE FROM notas")
    cur.execute("DELETE FROM categorias")
    conn.commit()
    print("Listo. Tablas 'notas' y 'categorias' vaciadas.")
else:
    print("Cancelado. No se borró nada.")

conn.close()