import flet as ft
from datetime import date, timedelta
from .view import TasksView
from .model import TasksModel

class TasksController:
    def __init__(self):
        self.model = TasksModel()
        self.view = TasksView(controlador=self)
        self.categoria_seleccionada_id = None
        self.nota_seleccionada_id = None
        self.semana_actual = self._inicio_semana(date.today())
        self._fecha_evento_nota_actual = None  # fecha elegida en el diálogo de nota, aún no guardada

    def obtener_vista(self):
        return self.view

    def actualizar_pantalla(self):
        try:
            if self.view.page:
                self.view.page.update()
        except Exception as ex:
            print(f"Error al actualizar pantalla: {ex}")

    # --- CONTROL DE DIÁLOGOS ---
    def abrir_dialogo_categoria(self, e):
        self.view.txt_nombre_cat.value = ""
        self.view.page.show_dialog(self.view.dialogo_categoria)
        self.actualizar_pantalla()

    def abrir_dialogo_nota(self, e):
        self.view.txt_titulo_nota.value = ""
        self.view.txt_descripcion_nota.value = ""
        self._fecha_evento_nota_actual = None
        self.view.lbl_fecha_evento_nota.value = "Sin fecha"

        # Llena el selector de sección con las secciones actuales,
        # preseleccionando la que estaba activa (si había una).
        categorias = self.model.obtener_categorias()
        self.view.drop_seccion_nota.options = [
            ft.DropdownOption(key=str(c.id), text=c.nombre) for c in categorias
        ]
        self.view.drop_seccion_nota.value = (
            str(self.categoria_seleccionada_id) if self.categoria_seleccionada_id else None
        )

        self.view.page.show_dialog(self.view.dialogo_nota)
        self.actualizar_pantalla()

    def cerrar_dialogos(self, e=None):
        self.view.page.pop_dialog()
        self.actualizar_pantalla()

    # --- LÓGICA DE NEGOCIO: CATEGORÍAS ---
    def guardar_categoria(self, e):
        nombre = self.view.txt_nombre_cat.value
        color = self.view.drop_color_cat.value
        if nombre:
            self.model.crear_categoria(nombre, color)
            self.cerrar_dialogos()
            self.refrescar_ui_categorias()

    def refrescar_ui_categorias(self, es_inicio=False):
        categorias = self.model.obtener_categorias()
        self.view.lista_categorias.controls.clear()

        for cat in categorias:
            btn = ft.Container(
                content=ft.Row([
                    ft.Text(cat.nombre, color="white", weight="bold", expand=True),
                    ft.CircleAvatar(
                        content=ft.Text("0", size=10, color="white"),
                        radius=12,
                        bgcolor=ft.Colors.with_opacity(0.3, "black")
                    )
                ]),
                bgcolor=cat.color, padding=15, border_radius=10,
                on_click=lambda e, c=cat: self.seleccionar_categoria(c)
            )
            self.view.lista_categorias.controls.append(btn)

        # Ya no depende de haber seleccionado una sección primero: el propio
        # diálogo de "Nueva Nota" trae su selector de sección. Solo se
        # deshabilita si todavía no existe ninguna sección creada.
        self.view.btn_crear_nota.disabled = (len(categorias) == 0)

        if es_inicio:
            self.refrescar_calendario_eventos()
        else:
            self.actualizar_pantalla()

    def seleccionar_categoria(self, categoria):
        self.categoria_seleccionada_id = categoria.id
        self.view.btn_crear_nota.disabled = False
        self.view.lbl_categoria_seleccionada.value = f"· {categoria.nombre}"
        self.refrescar_ui_notas()

    # --- LÓGICA DE NEGOCIO: NOTAS ---
    def guardar_nueva_nota(self, e):
        titulo = self.view.txt_titulo_nota.value
        descripcion = self.view.txt_descripcion_nota.value or ""
        seccion_id = self.view.drop_seccion_nota.value

        if not titulo or not seccion_id:
            return  # falta título o sección: no hay nada que guardar

        self.model.crear_nota(
            titulo,
            int(seccion_id),
            descripcion=descripcion,
            fecha_evento=self._fecha_evento_nota_actual,
        )

        # Si la nota se guardó en una sección distinta a la activa,
        # cambiamos la sección activa a esa para poder ver la nota.
        self.categoria_seleccionada_id = int(seccion_id)
        self._fecha_evento_nota_actual = None

        self.cerrar_dialogos()
        self.refrescar_ui_notas()
        self.refrescar_calendario_eventos()

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

    # --- SELECTOR DE FECHA DENTRO DEL DIÁLOGO "NUEVA NOTA" ---
    def abrir_selector_fecha_nota(self, e):
        self.view.page.show_dialog(self.view.date_picker_nota)

    def fecha_evento_seleccionada(self, e):
        seleccionada = self.view.date_picker_nota.value
        if seleccionada:
            fecha = seleccionada.date() if hasattr(seleccionada, "date") else seleccionada
            self._fecha_evento_nota_actual = fecha
            self.view.lbl_fecha_evento_nota.value = fecha.strftime("%d/%m/%Y")
            self.actualizar_pantalla()

    # --- CALENDARIO SEMANAL ---
    def _inicio_semana(self, fecha):
        """Devuelve el lunes de la semana que contiene 'fecha'."""
        return fecha - timedelta(days=fecha.weekday())

    def refrescar_calendario_eventos(self):
        """Repinta encabezados de la semana y los bloques de notas agendadas."""
        fin_semana = self.semana_actual + timedelta(days=6)
        notas_con_fecha = self.model.obtener_notas_por_rango_fecha(self.semana_actual, fin_semana)
        self.view.actualizar_semana(self.semana_actual)
        self.view.pintar_eventos_semana(self.semana_actual, notas_con_fecha)
        self.actualizar_pantalla()

    def semana_anterior(self, e):
        self.semana_actual -= timedelta(days=7)
        self.refrescar_calendario_eventos()

    def semana_siguiente(self, e):
        self.semana_actual += timedelta(days=7)
        self.refrescar_calendario_eventos()

    def abrir_selector_fecha(self, e):
        self.view.page.show_dialog(self.view.date_picker)

    def fecha_seleccionada(self, e):
        seleccionada = self.view.date_picker.value
        if seleccionada:
            fecha = seleccionada.date() if hasattr(seleccionada, "date") else seleccionada
            self.semana_actual = self._inicio_semana(fecha)
            self.refrescar_calendario_eventos()