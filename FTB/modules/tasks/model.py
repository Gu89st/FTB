from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from core.database import Base, SessionLocal, engine
import datetime

class Categoria(Base):
    """En la UI se muestra como 'Tarea' (ej: Universidad, Trabajo)."""
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    color = Column(String, default="#26a69a")
    secciones = relationship("Seccion", back_populates="categoria")

class Seccion(Base):
    """En la UI se muestra como 'Sección' (ej: Tecnologías Emergentes),
    agrupa notas dentro de una Tarea."""
    __tablename__ = "secciones"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    color = Column(String, default="#26a69a")
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    categoria = relationship("Categoria", back_populates="secciones")
    notas = relationship("Nota", back_populates="seccion")

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
    prioridad = Column(String, default="media")   # alta | media | baja | anotacion
    color_anotacion = Column(String, nullable=True)  # solo si prioridad == "anotacion"
    ruta_adjunto = Column(String, nullable=True)
    nombre_adjunto = Column(String, nullable=True)
    seccion_id = Column(Integer, ForeignKey("secciones.id"))
    seccion = relationship("Seccion", back_populates="notas")

COLORES_PRIORIDAD = {
    "alta": "#e53935",
    "media": "#fdd835",
    "baja": "#3949ab",
}

class TasksModel:
    def __init__(self):
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()

    # --- TAREAS (Categoria) ---
    def crear_categoria(self, nombre, color):
        nueva = Categoria(nombre=nombre, color=color)
        self.db.add(nueva)
        self.db.commit()
        return nueva

    def obtener_categorias(self):
        return self.db.query(Categoria).all()

    def editar_categoria(self, categoria_id, nombre, color):
        cat = self.db.query(Categoria).filter(Categoria.id == categoria_id).first()
        if cat:
            cat.nombre = nombre
            cat.color = color
            self.db.commit()

    def eliminar_categoria(self, categoria_id):
        """Elimina la tarea, sus secciones, y las notas de esas secciones."""
        secciones = self.db.query(Seccion).filter(Seccion.categoria_id == categoria_id).all()
        for s in secciones:
            self.db.query(Nota).filter(Nota.seccion_id == s.id).delete()
        self.db.query(Seccion).filter(Seccion.categoria_id == categoria_id).delete()
        cat = self.db.query(Categoria).filter(Categoria.id == categoria_id).first()
        if cat:
            self.db.delete(cat)
        self.db.commit()

    # --- SECCIONES ---
    def crear_seccion(self, nombre, color, categoria_id):
        nueva = Seccion(nombre=nombre, color=color, categoria_id=categoria_id)
        self.db.add(nueva)
        self.db.commit()
        return nueva

    def obtener_secciones_por_categoria(self, categoria_id):
        return self.db.query(Seccion).filter(Seccion.categoria_id == categoria_id).all()

    def obtener_todas_secciones(self):
        return self.db.query(Seccion).all()

    def editar_seccion(self, seccion_id, nombre, color):
        sec = self.db.query(Seccion).filter(Seccion.id == seccion_id).first()
        if sec:
            sec.nombre = nombre
            sec.color = color
            self.db.commit()

    def eliminar_seccion(self, seccion_id):
        self.db.query(Nota).filter(Nota.seccion_id == seccion_id).delete()
        sec = self.db.query(Seccion).filter(Seccion.id == seccion_id).first()
        if sec:
            self.db.delete(sec)
        self.db.commit()

    # --- NOTAS ---
    def crear_nota(self, titulo, seccion_id, descripcion="", fecha_evento=None,
                    hora_inicio=None, hora_fin=None, prioridad="media",
                    color_anotacion=None, ruta_adjunto=None, nombre_adjunto=None):
        fecha_actual = datetime.datetime.now().strftime("%b%d")
        nueva = Nota(
            titulo=titulo,
            contenido="",
            descripcion=descripcion,
            fecha=fecha_actual,
            fecha_evento=fecha_evento,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            prioridad=prioridad,
            color_anotacion=color_anotacion,
            ruta_adjunto=ruta_adjunto,
            nombre_adjunto=nombre_adjunto,
            seccion_id=seccion_id,
        )
        self.db.add(nueva)
        self.db.commit()
        return nueva

    def obtener_notas_por_seccion(self, seccion_id):
        return self.db.query(Nota).filter(Nota.seccion_id == seccion_id).all()

    def obtener_notas_por_rango_fecha(self, fecha_inicio, fecha_fin):
        return (
            self.db.query(Nota)
            .filter(Nota.fecha_evento.isnot(None))
            .filter(Nota.fecha_evento >= fecha_inicio)
            .filter(Nota.fecha_evento <= fecha_fin)
            .all()
        )

    def editar_nota(self, nota_id, titulo, descripcion, seccion_id, fecha_evento,
                     hora_inicio, hora_fin, prioridad, color_anotacion,
                     ruta_adjunto, nombre_adjunto):
        nota = self.db.query(Nota).filter(Nota.id == nota_id).first()
        if nota:
            nota.titulo = titulo
            nota.descripcion = descripcion
            nota.seccion_id = seccion_id
            nota.fecha_evento = fecha_evento
            nota.hora_inicio = hora_inicio
            nota.hora_fin = hora_fin
            nota.prioridad = prioridad
            nota.color_anotacion = color_anotacion
            if ruta_adjunto is not None:
                nota.ruta_adjunto = ruta_adjunto
                nota.nombre_adjunto = nombre_adjunto
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