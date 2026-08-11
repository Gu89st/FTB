import bcrypt
from sqlalchemy import Column, Integer, String
from core.database import Base, SessionLocal

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)

class LoginModel:
    def __init__(self):
        self.db = SessionLocal()

    def verificar_credenciales(self,username,password):
        """Busca al usuario y verifica su contraseña encriptada"""
        usuario = self.db.query(Usuario).filter(Usuario.username == username).first()
        if usuario is None:
            return False

        coincide=bcrypt.checkpw(
            password.encode('utf-8'),
            usuario.password_hash.encode('utf-8')
        )
        return coincide