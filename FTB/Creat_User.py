# crear_usuario.py
import bcrypt
from core.database import engine, Base, SessionLocal
from modules.login.model import Usuario

# 1. Crea el archivo de la base de datos y todas las tablas
print("Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)

# 2. Genera una contraseña segura encriptada
password_elegida = "123456789" # Aquí puedes poner la que quieras
sal = bcrypt.gensalt()
password_encriptada = bcrypt.hashpw(password_elegida.encode('utf-8'), sal)

# 3. Guarda el usuario en la base de datos
db = SessionLocal()
nuevo_usuario = Usuario(
    username="admin", 
    password_hash=password_encriptada.decode('utf-8')
)

try:
    db.add(nuevo_usuario)
    db.commit()
    print("✅ Usuario 'admin' creado exitosamente con contraseña '1234'.")
except Exception as e:
    print("El usuario ya existe o hubo un error:", e)
finally:
    db.close()