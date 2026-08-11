from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base, SessionLocal, engine

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    color=Column(String, default="#26a69a")

    notas=relationship("Nota", back_populates="categoria")

class Nota(Base):
    __tablename__ = "notas"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    contenido = Column(String, nullable=False)
    fecha=Column(String)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    categoria = relationship("Categoria", back_populates="notas")

class TasksModel:
    def __init__(self):
        # Esta línea asegura que las nuevas tablas se creen en tu archivo .db
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()
        
    def crear_categoria(self, nombre, color):
        """Guarda una nueva categoría en la base de datos"""
        nueva_categoria = Categoria(nombre=nombre, color=color)
        self.db.add(nueva_categoria)
        self.db.commit()
        return nueva_categoria

    def obtener_categorias(self):
        """Devuelve todas las categorías guardadas"""
        return self.db.query(Categoria).all()