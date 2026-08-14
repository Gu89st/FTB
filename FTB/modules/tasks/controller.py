# modules/tasks/controller.py
import flet as ft
from .view import TasksView
from .model import TasksModel

class TasksController:
    def __init__(self):
        self.model = TasksModel()
        self.view = TasksView(controlador=self)

    

    def obtener_vista(self):
        return self.view

    def actualizar_pantalla(self):
        """Método ultra-blindado que absorbe cualquier error de desincronización"""
        try:
            if self.view.page:
                self.view.page.update()
        except Exception:
            pass # Si Flet no está listo, ignoramos el error en lugar de colapsar la app

    def obtener_vista(self):
        return self.view

    # --- CONTROL DE DIÁLOGOS ---
    def abrir_dialogo_categoria(self, e):
        self.view.txt_nombre_cat.value = ""
        self.view.page.dialog = self.view.dialogo_categoria
        self.view.dialogo_categoria.open = True
        self.actualizar_pantalla()

    def abrir_dialogo_nota(self, e):
        self.view.txt_titulo_nota.value = ""
        self.view.page.dialog = self.view.dialogo_nota
        self.view.dialogo_nota.open = True
        self.actualizar_pantalla()

    def cerrar_dialogos(self, e=None):
        self.view.dialogo_categoria.open = False
        self.view.dialogo_nota.open = False
        self.actualizar_pantalla()

    # --- LÓGICA DE NEGOCIO ---
    def guardar_categoria(self, e):
        nombre = self.view.txt_nombre_cat.value
        color = self.view.drop_color_cat.value
        if nombre:
            self.model.crear_categoria(nombre, color)
            self.cerrar_dialogos()
            self.refrescar_ui_categorias() # Aquí sí actualizamos porque ya está montado

    def refrescar_ui_categorias(self, es_inicio=False):
        categorias = self.model.obtener_categorias()
        self.view.lista_categorias.controls.clear()
        
        for cat in categorias:
            btn = ft.Container(
                content=ft.Row([
                    ft.Text(cat.nombre, color="white", weight="bold", expand=True),
                    ft.CircleAvatar(content=ft.Text("0", size=10, color="white"), radius=12, bgcolor=ft.colors.with_opacity(0.3, "black"))
                ]),
                bgcolor=cat.color, padding=15, border_radius=10,
                on_click=lambda e, id=cat.id: self.seleccionar_categoria(id)
            )
            self.view.lista_categorias.controls.append(btn)
        
        # Solo forzamos la actualización visual si NO es el arranque inicial
        if not es_inicio:
            self.actualizar_pantalla()

    def seleccionar_categoria(self, categoria_id):
        self.categoria_seleccionada_id = categoria_id
        self.view.btn_crear_nota.disabled = False 
        self.refrescar_ui_notas()

    def guardar_nueva_nota(self, e):
        titulo = self.view.txt_titulo_nota.value
        if titulo and self.categoria_seleccionada_id:
            self.model.crear_nota(titulo, self.categoria_seleccionada_id)
            self.cerrar_dialogos()
            self.refrescar_ui_notas()

    def refrescar_ui_notas(self):
        notas = self.model.obtener_notas_por_categoria(self.categoria_seleccionada_id)
        self.view.lista_notas_ui.controls.clear()

        for nota in notas:
            tarjeta = ft.Card(
                elevation=1,
                content=ft.Container(
                    bgcolor="#e0f2f1", padding=15, border_radius=10,
                    content=ft.Column([
                        ft.Text(nota.titulo, weight="bold", color="black87"),
                        ft.Text(nota.fecha, color="grey", size=12)
                    ]),
                    on_click=lambda e, n=nota: self.seleccionar_nota(n)
                )
            )
            self.view.lista_notas_ui.controls.append(tarjeta)
            
        self.actualizar_pantalla()

    def seleccionar_nota(self, nota):
        self.nota_seleccionada_id = nota.id
        self.view.lbl_editor_titulo.value = nota.titulo
        self.view.txt_editor_contenido.value = nota.contenido
        self.view.txt_editor_contenido.disabled = False 
        self.actualizar_pantalla()

    def actualizar_texto_nota(self, e):
        if self.nota_seleccionada_id:
            nuevo_texto = self.view.txt_editor_contenido.value
            self.model.actualizar_nota(self.nota_seleccionada_id, nuevo_texto)
            self.actualizar_pantalla()