"""
Migración de un solo uso: crea la tabla 'secciones' y agrega a 'notas'
las columnas nuevas (seccion_id, prioridad, color_anotacion, ruta_adjunto,
nombre_adjunto).

Como las notas ANTES colgaban directo de una categoría (ej. "BIG DATA",
"Tecnologías Emergentes" dentro de "Universidad"), y ahora deben colgar
de una Sección, esta migración convierte cada nota existente en una
NUEVA sección con ese mismo nombre, y esa nota queda como la primera
nota dentro de esa sección (conserva su contenido, fecha, hora, etc.).

Uso:
    python migrar_secciones.py

Ejecutar desde la raíz del proyecto (donde vive ftb_usuarios.db), con la
app cerrada. Es seguro correrlo más de una vez: si ya migraste antes,
detecta que 'seccion_id' ya existe y no vuelve a duplicar datos.
"""
import sqlite3
import os

DB_PATH = "ftb_usuarios.db"

if not os.path.exists(DB_PATH):
    print(f"No se encontró {DB_PATH} en este directorio.")
    raise SystemExit(1)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 1. Crear tabla 'secciones' si no existe
cur.execute("""
CREATE TABLE IF NOT EXISTS secciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    color TEXT DEFAULT '#26a69a',
    categoria_id INTEGER REFERENCES categorias(id)
)
""")
conn.commit()
print("Tabla 'secciones' lista.")

# 2. Agregar columnas nuevas a 'notas'
cur.execute("PRAGMA table_info(notas)")
columnas_actuales = {fila[1] for fila in cur.fetchall()}
seccion_id_era_nueva = "seccion_id" not in columnas_actuales

columnas_nuevas = {
    "seccion_id": "INTEGER REFERENCES secciones(id)",
    "prioridad": "TEXT DEFAULT 'media'",
    "color_anotacion": "TEXT",
    "ruta_adjunto": "TEXT",
    "nombre_adjunto": "TEXT",
}
for nombre, tipo in columnas_nuevas.items():
    if nombre not in columnas_actuales:
        cur.execute(f"ALTER TABLE notas ADD COLUMN {nombre} {tipo}")
        print(f"Columna '{nombre}' agregada a notas.")
    else:
        print(f"Columna '{nombre}' ya existía, se omite.")
conn.commit()

# 3. Migrar datos: cada nota existente (que colgaba de una categoría) se
#    convierte en una nueva sección, y la nota queda como su primer
#    contenido.
if seccion_id_era_nueva:
    cur.execute("SELECT id, titulo, categoria_id FROM notas WHERE categoria_id IS NOT NULL")
    notas_viejas = cur.fetchall()
    print(f"\nMigrando {len(notas_viejas)} nota(s) existente(s) a nuevas secciones...")
    for nota_id, titulo, categoria_id in notas_viejas:
        cur.execute(
            "INSERT INTO secciones (nombre, color, categoria_id) VALUES (?, ?, ?)",
            (titulo, "#26a69a", categoria_id),
        )
        nueva_seccion_id = cur.lastrowid
        cur.execute("UPDATE notas SET seccion_id = ? WHERE id = ?", (nueva_seccion_id, nota_id))
        print(f"  '{titulo}' -> nueva sección (id={nueva_seccion_id})")
    conn.commit()
    print("Migración de datos completada.")
else:
    print("\nLa columna 'seccion_id' ya existía: se omite la migración de datos (ya se hizo antes).")

conn.close()
print("\nListo.")