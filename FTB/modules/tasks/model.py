from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from core.database import Base, SessionLocal, engine
import datetime

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    color = Column(String, default="#26a69a")
    notas = relationship("Nota", back_populates="categoria")

class Nota(Base):
    __tablename__ = "notas"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    contenido = Column(String, nullable=False, default="")
    descripcion = Column(String, nullable=True, default="")
    fecha = Column(String)                       # fecha de creación (texto)
    fecha_evento = Column(Date, nullable=True)    # fecha del evento agendado (opcional)
    hora_inicio = Column(String, nullable=True)   # "HH:MM"
    hora_fin = Column(String, nullable=True)      # "HH:MM"
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    categoria = relationship("Categoria", back_populates="notas")

class TasksModel:
    def __init__(self):
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()

    # --- CATEGORÍAS ---
    def crear_categoria(self, nombre, color):
        nueva_categoria = Categoria(nombre=nombre, color=color)
        self.db.add(nueva_categoria)
        self.db.commit()
        return nueva_categoria

    def obtener_categorias(self):
        return self.db.query(Categoria).all()

    def editar_categoria(self, categoria_id, nombre, color):
        cat = self.db.query(Categoria).filter(Categoria.id == categoria_id).first()
        if cat:
            cat.nombre = nombre
            cat.color = color
            self.db.commit()

    def eliminar_categoria(self, categoria_id):
        """Elimina la sección y todas sus notas (no hay borrado en cascada
        configurado en el ORM, así que las notas se borran explícitamente)."""
        self.db.query(Nota).filter(Nota.categoria_id == categoria_id).delete()
        cat = self.db.query(Categoria).filter(Categoria.id == categoria_id).first()
        if cat:
            self.db.delete(cat)
        self.db.commit()

    # --- NOTAS ---
    def crear_nota(self, titulo, categoria_id, descripcion="", fecha_evento=None,
                    hora_inicio=None, hora_fin=None):
        fecha_actual = datetime.datetime.now().strftime("%b%d")
        nueva_nota = Nota(
            titulo=titulo,
            contenido="",
            descripcion=descripcion,
            fecha=fecha_actual,
            fecha_evento=fecha_evento,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            categoria_id=categoria_id,
        )
        self.db.add(nueva_nota)
        self.db.commit()
        return nueva_nota

    def obtener_notas_por_categoria(self, categoria_id):
        return self.db.query(Nota).filter(Nota.categoria_id == categoria_id).all()

    def obtener_notas_por_rango_fecha(self, fecha_inicio, fecha_fin):
        return (
            self.db.query(Nota)
            .filter(Nota.fecha_evento.isnot(None))
            .filter(Nota.fecha_evento >= fecha_inicio)
            .filter(Nota.fecha_evento <= fecha_fin)
            .all()
        )

    def editar_nota(self, nota_id, titulo, descripcion, categoria_id,
                     fecha_evento, hora_inicio, hora_fin):
        nota = self.db.query(Nota).filter(Nota.id == nota_id).first()
        if nota:
            nota.titulo = titulo
            nota.descripcion = descripcion
            nota.categoria_id = categoria_id
            nota.fecha_evento = fecha_evento
            nota.hora_inicio = hora_inicio
            nota.hora_fin = hora_fin
            self.db.commit()

    def eliminar_nota(self, nota_id):
        nota = self.db.query(Nota).filter(Nota.id == nota_id).first()
        if nota:
            self.db.delete(nota)
            self.db.commit()

    def actualizar_nota(self, nota_id, nuevo_contenido):
        nota = self.db.query(Nota).filter(Nota.id == nota_id).first()
        if nota:
            nota.contenido = nuevo_contenido
            self.db.commit()