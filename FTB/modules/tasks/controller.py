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

        # Estado temporal mientras se llena el diálogo de "Nueva/Editar Nota"
        self._nota_editando_id = None
        self._fecha_evento_nota_actual = None
        self._hora_inicio_nota_actual = None
        self._hora_fin_nota_actual = None

        # Estado temporal mientras se llena el diálogo de "Nueva/Editar Sección"
        self._categoria_editando_id = None

        # Acción pendiente de confirmación (eliminar sección / nota)
        self._accion_eliminar_pendiente = None

    def obtener_vista(self):
        return self.view

    def actualizar_pantalla(self):
        try:
            if self.view.page:
                self.view.page.update()
        except Exception as ex:
            print(f"Error al actualizar pantalla: {ex}")

    # --- CONTROL DE DIÁLOGOS ---
    def abrir_dialogo_categoria(self, e, categoria=None):
        self._categoria_editando_id = categoria.id if categoria else None
        self.view.txt_titulo_dialogo_categoria.value = "Editar Sección" if categoria else "Nueva Sección"
        self.view.txt_nombre_cat.value = categoria.nombre if categoria else ""
        self.view.drop_color_cat.value = categoria.color if categoria else "#26a69a"
        self.view.page.show_dialog(self.view.dialogo_categoria)
        self.actualizar_pantalla()

    def abrir_dialogo_nota(self, e, nota=None):
        self._nota_editando_id = nota.id if nota else None
        self.view.txt_titulo_dialogo_nota.value = "Editar Nota" if nota else "Nueva Nota"
        self.view.txt_titulo_nota.value = nota.titulo if nota else ""
        self.view.txt_descripcion_nota.value = (nota.descripcion or "") if nota else ""

        self._fecha_evento_nota_actual = nota.fecha_evento if nota else None
        self._hora_inicio_nota_actual = nota.hora_inicio if nota else None
        self._hora_fin_nota_actual = nota.hora_fin if nota else None
        self.view.lbl_fecha_evento_nota.value = (
            self._fecha_evento_nota_actual.strftime("%d/%m/%Y")
            if self._fecha_evento_nota_actual else "Sin fecha"
        )
        self.view.lbl_hora_inicio_nota.value = self._hora_inicio_nota_actual or "--:--"
        self.view.lbl_hora_fin_nota.value = self._hora_fin_nota_actual or "--:--"

        categorias = self.model.obtener_categorias()
        categoria_objetivo = nota.categoria_id if nota else self.categoria_seleccionada_id

        if categoria_objetivo and not nota:
            # Crear nota desde una sección ya activa: no hace falta elegir,
            # se guarda directo ahí.
            categoria_activa = next((c for c in categorias if c.id == categoria_objetivo), None)
            self.view.drop_seccion_nota.visible = False
            self.view.lbl_seccion_fija_nota.visible = True
            self.view.lbl_seccion_fija_nota.value = (
                f"Se agregará a: {categoria_activa.nombre}" if categoria_activa else ""
            )
        else:
            # Sin sección activa (o editando, donde siempre se permite mover
            # la nota de sección): mostramos el selector con la lista.
            self.view.drop_seccion_nota.visible = True
            self.view.lbl_seccion_fija_nota.visible = False
            self.view.drop_seccion_nota.options = [
                ft.DropdownOption(key=str(c.id), text=c.nombre) for c in categorias
            ]
            self.view.drop_seccion_nota.value = str(categoria_objetivo) if categoria_objetivo else None

        self.view.page.show_dialog(self.view.dialogo_nota)
        self.actualizar_pantalla()

    def cerrar_dialogos(self, e=None):
        self.view.page.pop_dialog()
        self.actualizar_pantalla()

    # --- CONFIRMACIÓN DE ELIMINACIÓN (reutilizable) ---
    def _pedir_confirmacion_eliminar(self, mensaje, accion):
        self.view.txt_mensaje_confirmar.value = mensaje
        self._accion_eliminar_pendiente = accion
        self.view.page.show_dialog(self.view.dialogo_confirmar)
        self.actualizar_pantalla()

    def confirmar_eliminacion(self, e):
        if self._accion_eliminar_pendiente:
            self._accion_eliminar_pendiente()
        self._accion_eliminar_pendiente = None
        self.cerrar_dialogos()

    # --- LÓGICA DE NEGOCIO: CATEGORÍAS ---
    def guardar_categoria(self, e):
        nombre = self.view.txt_nombre_cat.value
        color = self.view.drop_color_cat.value
        if not nombre:
            return

        if self._categoria_editando_id:
            self.model.editar_categoria(self._categoria_editando_id, nombre, color)
            self._categoria_editando_id = None
        else:
            self.model.crear_categoria(nombre, color)

        self.cerrar_dialogos()
        self.refrescar_ui_categorias()

    def refrescar_ui_categorias(self, es_inicio=False):
        categorias = self.model.obtener_categorias()
        self.view.lista_categorias.controls.clear()

        for cat in categorias:
            self.view.lista_categorias.controls.append(self.view.crear_item_categoria(cat))

        # Ya no depende de haber seleccionado una sección primero: el propio
        # diálogo de "Nueva Nota" trae su selector. Solo se deshabilita si
        # todavía no existe ninguna sección creada.
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

    def eliminar_categoria(self, categoria):
        self._pedir_confirmacion_eliminar(
            f"¿Eliminar la sección '{categoria.nombre}' y todas sus notas? Esta acción no se puede deshacer.",
            lambda: self._eliminar_categoria_confirmada(categoria.id),
        )

    def _eliminar_categoria_confirmada(self, categoria_id):
        self.model.eliminar_categoria(categoria_id)
        if self.categoria_seleccionada_id == categoria_id:
            self.categoria_seleccionada_id = None
            self.nota_seleccionada_id = None
            self.view.lista_notas_ui.controls.clear()
            self.view.lbl_categoria_seleccionada.value = ""
            self.view.lbl_editor_titulo.value = "Selecciona una nota"
            self.view.txt_editor_contenido.value = ""
            self.view.txt_editor_contenido.disabled = True
        self.refrescar_ui_categorias()
        self.refrescar_calendario_eventos()

    # --- LÓGICA DE NEGOCIO: NOTAS ---
    def guardar_nueva_nota(self, e):
        titulo = self.view.txt_titulo_nota.value
        descripcion = self.view.txt_descripcion_nota.value or ""

        if self.view.drop_seccion_nota.visible:
            seccion_id = self.view.drop_seccion_nota.value
        else:
            seccion_id = str(self.categoria_seleccionada_id) if self.categoria_seleccionada_id else None

        if not titulo or not seccion_id:
            return

        if self._nota_editando_id:
            self.model.editar_nota(
                self._nota_editando_id, titulo, descripcion, int(seccion_id),
                self._fecha_evento_nota_actual,
                self._hora_inicio_nota_actual, self._hora_fin_nota_actual,
            )
            self._nota_editando_id = None
        else:
            self.model.crear_nota(
                titulo, int(seccion_id), descripcion=descripcion,
                fecha_evento=self._fecha_evento_nota_actual,
                hora_inicio=self._hora_inicio_nota_actual, hora_fin=self._hora_fin_nota_actual,
            )

        self.categoria_seleccionada_id = int(seccion_id)
        self._fecha_evento_nota_actual = None
        self._hora_inicio_nota_actual = None
        self._hora_fin_nota_actual = None

        self.cerrar_dialogos()
        self.refrescar_ui_notas()
        self.refrescar_calendario_eventos()

    def refrescar_ui_notas(self):
        notas = self.model.obtener_notas_por_categoria(self.categoria_seleccionada_id)
        self.view.lista_notas_ui.controls.clear()

        for nota in notas:
            self.view.lista_notas_ui.controls.append(self.view.crear_item_nota(nota))

        self.actualizar_pantalla()

    def seleccionar_nota(self, nota):
        self.nota_seleccionada_id = nota.id
        self.view.lbl_editor_titulo.value = nota.titulo
        self.view.txt_editor_contenido.value = nota.contenido
        self.view.txt_editor_contenido.disabled = False
        self.actualizar_pantalla()

    def eliminar_nota(self, nota):
        self._pedir_confirmacion_eliminar(
            f"¿Eliminar la nota '{nota.titulo}'? Esta acción no se puede deshacer.",
            lambda: self._eliminar_nota_confirmada(nota.id),
        )

    def _eliminar_nota_confirmada(self, nota_id):
        self.model.eliminar_nota(nota_id)
        if self.nota_seleccionada_id == nota_id:
            self.nota_seleccionada_id = None
            self.view.lbl_editor_titulo.value = "Selecciona una nota"
            self.view.txt_editor_contenido.value = ""
            self.view.txt_editor_contenido.disabled = True
        self.refrescar_ui_notas()
        self.refrescar_calendario_eventos()

    def actualizar_texto_nota(self, e):
        if self.nota_seleccionada_id:
            nuevo_texto = self.view.txt_editor_contenido.value
            self.model.actualizar_nota(self.nota_seleccionada_id, nuevo_texto)
            self.actualizar_pantalla()

    # --- SELECTORES DE FECHA / HORA DENTRO DEL DIÁLOGO "NOTA" ---
    def abrir_selector_fecha_nota(self, e):
        self.view.page.show_dialog(self.view.date_picker_nota)

    def fecha_evento_seleccionada(self, e):
        seleccionada = self.view.date_picker_nota.value
        if seleccionada:
            fecha = seleccionada.date() if hasattr(seleccionada, "date") else seleccionada
            self._fecha_evento_nota_actual = fecha
            self.view.lbl_fecha_evento_nota.value = fecha.strftime("%d/%m/%Y")
            self.actualizar_pantalla()

    def abrir_selector_hora_inicio(self, e):
        self.view.page.show_dialog(self.view.time_picker_inicio)

    def hora_inicio_seleccionada(self, e):
        valor = self.view.time_picker_inicio.value
        if valor:
            self._hora_inicio_nota_actual = valor.strftime("%H:%M")
            self.view.lbl_hora_inicio_nota.value = self._hora_inicio_nota_actual
            self.actualizar_pantalla()

    def abrir_selector_hora_fin(self, e):
        self.view.page.show_dialog(self.view.time_picker_fin)

    def hora_fin_seleccionada(self, e):
        valor = self.view.time_picker_fin.value
        if valor:
            self._hora_fin_nota_actual = valor.strftime("%H:%M")
            self.view.lbl_hora_fin_nota.value = self._hora_fin_nota_actual
            self.actualizar_pantalla()

    # --- CALENDARIO SEMANAL ---
    def _inicio_semana(self, fecha):
        return fecha - timedelta(days=fecha.weekday())

    def refrescar_calendario_eventos(self):
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