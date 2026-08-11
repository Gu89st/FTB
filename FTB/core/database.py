from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

engine =create_engine('sqlite:///ftb_usuarios.db', connect_args={"check_same_thread": False})

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
def obtener_sesion():
    """Devuelve una nueva sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()