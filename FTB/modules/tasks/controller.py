# modules/tasks/controller.py
from .view import TasksView
from .model import TasksModel

class TasksController:
    def __init__(self):
        self.model = TasksModel()
        self.view = TasksView(controlador=self)

    def obtener_vista(self):
        return self.view

    # --- LÓGICA DE CATEGORÍAS ---
    def abrir_dialogo_categoria(self, e):
        """Abre el popup usando la sintaxis moderna de Flet"""
        # Limpiamos los campos antes de abrir
        self.view.txt_nombre_cat.value = ""
        self.view.drop_color_cat.value = "#26a69a"
        self.view.page.open(self.view.dialogo_categoria)

    def cerrar_dialogo_categoria(self, e):
        """Cierra el popup sin hacer nada"""
        self.view.page.close(self.view.dialogo_categoria)

    def guardar_categoria(self, e):
        """Toma los datos del popup y los guarda en la BD"""
        nombre = self.view.txt_nombre_cat.value
        color = self.view.drop_color_cat.value

        # Solo guardamos si el usuario escribió un nombre
        if nombre:
            # 1. Guardar en la base de datos
            self.model.crear_categoria(nombre, color)
            
            # 2. Cerrar el popup
            self.view.page.close(self.view.dialogo_categoria)
            
            # (En el próximo paso actualizaremos la lista visual de categorías aquí)
            print(f"✅ ¡Categoría '{nombre}' guardada con color {color}!")