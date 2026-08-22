import flet as ft
from datetime import date, timedelta
from .view import TasksView
from .model import TasksModel

class TasksController:
    def __init__(self):
        self.model = TasksModel()
        self.view = TasksView(controlador=self)

        # Selección activa en cada nivel de la jerarquía
        self.categoria_seleccionada_id = None   # Tarea activa
        self.seccion_seleccionada_id = None     # Sección activa
        self.nota_seleccionada_id = None        # Nota abierta en el editor

        self.semana_actual = self._inicio_semana(date.today())

        # Estado temporal mientras se llena el diálogo de "Nueva/Editar Sección"
        self._categoria_editando_id = None

        # Estado temporal mientras se llena el diálogo de "Nueva/Editar Tarea"
        self._seccion_editando_id = None

        # Estado temporal mientras se llena el diálogo de "Nueva/Editar Nota"
        self._nota_editando_id = None
        self._fecha_evento_nota_actual = None
        self._hora_inicio_nota_actual = None
        self._hora_fin_nota_actual = None
        self._color_anotacion_nota_actual = None
        self._ruta_adjunto_nota_actual = None
        self._nombre_adjunto_nota_actual = None
        self._tipo_adjunto_pendiente = None  # "imagen" | "documento" | None

        # Acción pendiente de confirmación (eliminar tarea / sección / nota)
        self._accion_eliminar_pendiente = None

        # Los FilePicker de Flet necesitan estar registrados en el overlay
        # de la página para poder abrirse; se agregan la primera vez que
        # hay página disponible (ver _asegurar_overlay).
        self._overlay_listo = False

    def obtener_vista(self):
        return self.view

    def actualizar_pantalla(self):
        try:
            if self.view.page:
                self.view.page.update()
        except Exception as ex:
            print(f"Error al actualizar pantalla: {ex}")

    def _asegurar_overlay(self):
        if not self._overlay_listo and self.view.page:
            self.view.page.services.append(self.view.selector_archivo)
            self._overlay_listo = True

    # --- CONTROL DE DIÁLOGOS: TAREA (Categoria) ---
    def abrir_dialogo_categoria(self, e, categoria=None):
        self._categoria_editando_id = categoria.id if categoria else None
        self.view.txt_titulo_dialogo_categoria.value = "Editar Tarea" if categoria else "Nueva Tarea"
        self.view.txt_nombre_cat.value = categoria.nombre if categoria else ""
        self.view.drop_color_cat.value = categoria.color if categoria else "#26a69a"
        self.view.page.show_dialog(self.view.dialogo_categoria)
        self.actualizar_pantalla()

    # --- CONTROL DE DIÁLOGOS: SECCIÓN ---
    def abrir_dialogo_seccion(self, e, seccion=None):
        self._seccion_editando_id = seccion.id if seccion else None
        self.view.txt_titulo_dialogo_seccion.value = "Editar Sección" if seccion else "Nueva Sección"
        self.view.txt_nombre_seccion.value = seccion.nombre if seccion else ""
        self.view.drop_color_seccion.value = seccion.color if seccion else "#26a69a"
        self.view.page.show_dialog(self.view.dialogo_seccion)
        self.actualizar_pantalla()

    # --- CONTROL DE DIÁLOGOS: NOTA ---
    def abrir_dialogo_nota(self, e, nota=None, prioridad_inicial=None,
                            enfocar_fecha=False, enfocar_hora=False, es_anotacion=False):
        self._asegurar_overlay()

        self._nota_editando_id = nota.id if nota else None
        self.view.txt_titulo_dialogo_nota.value = "Editar Nota" if nota else "Nueva Nota"
        self.view.txt_titulo_nota.value = nota.titulo if nota else ""
        self.view.txt_descripcion_nota.value = (nota.descripcion or "") if nota else ""

        self._fecha_evento_nota_actual = nota.fecha_evento if nota else None
        self._hora_inicio_nota_actual = nota.hora_inicio if nota else None
        self._hora_fin_nota_actual = nota.hora_fin if nota else None
        self._ruta_adjunto_nota_actual = nota.ruta_adjunto if nota else None
        self._nombre_adjunto_nota_actual = nota.nombre_adjunto if nota else None

        self.view.lbl_fecha_evento_nota.value = (
            self._fecha_evento_nota_actual.strftime("%d/%m/%Y") if self._fecha_evento_nota_actual else "Sin fecha"
        )
        self.view.lbl_hora_inicio_nota.value = self._hora_inicio_nota_actual or "--:--"
        self.view.lbl_hora_fin_nota.value = self._hora_fin_nota_actual or "--:--"
        self.view.lbl_adjunto_nota.value = (
            f"📎 {self._nombre_adjunto_nota_actual}" if self._nombre_adjunto_nota_actual else "Sin adjunto"
        )

        # Prioridad inicial: la de la nota (si se edita), o la pedida por el
        # atajo del toolbar, o "anotacion" si vino del atajo de anotaciones,
        # o "media" por defecto.
        if nota:
            prioridad = nota.prioridad
            self._color_anotacion_nota_actual = nota.color_anotacion
        elif es_anotacion:
            prioridad = "anotacion"
            self._color_anotacion_nota_actual = None
        else:
            prioridad = prioridad_inicial or "media"
            self._color_anotacion_nota_actual = None
        self.view.drop_prioridad_nota.value = prioridad
        self.view.fila_color_anotacion.visible = (prioridad == "anotacion")

        # Selector de sección: solo se muestra si no había una sección
        # ya activa (o si se está editando, para poder mover la nota).
        secciones = self.model.obtener_todas_secciones()
        seccion_objetivo = nota.seccion_id if nota else self.seccion_seleccionada_id

        if seccion_objetivo and not nota:
            seccion_activa = next((s for s in secciones if s.id == seccion_objetivo), None)
            self.view.drop_seccion_nota.visible = False
            self.view.lbl_seccion_fija_nota.visible = True
            self.view.lbl_seccion_fija_nota.value = (
                f"Se agregará a: {seccion_activa.nombre}" if seccion_activa else ""
            )
        else:
            self.view.drop_seccion_nota.visible = True
            self.view.lbl_seccion_fija_nota.visible = False
            self.view.drop_seccion_nota.options = [
                ft.DropdownOption(key=str(s.id), text=f"{s.nombre} · {s.categoria.nombre}") for s in secciones
            ]
            self.view.drop_seccion_nota.value = str(seccion_objetivo) if seccion_objetivo else None

        self.view.page.show_dialog(self.view.dialogo_nota)
        self.actualizar_pantalla()

        if enfocar_fecha:
            self.abrir_selector_fecha_nota(e)
        elif enfocar_hora:
            self.abrir_selector_hora_inicio(e)

    async def abrir_dialogo_nota_con_adjunto(self, e, tipo):
        self.abrir_dialogo_nota(e)
        if tipo == "imagen":
            await self.abrir_selector_imagen(e)
        else:
            await self.abrir_selector_documento(e)

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

    # --- LÓGICA DE NEGOCIO: TAREAS (Categoria) ---
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

        if es_inicio:
            self.refrescar_calendario_eventos()
        else:
            self.actualizar_pantalla()

    def seleccionar_categoria(self, categoria):
        self.categoria_seleccionada_id = categoria.id
        self.seccion_seleccionada_id = None
        self.nota_seleccionada_id = None

        self.view.lbl_tarea_activa.value = f"· {categoria.nombre}"
        self.view.btn_crear_seccion.disabled = False
        self.view.lbl_seccion_activa.value = ""
        self.view.lista_notas_ui.controls.clear()
        self.view.btn_crear_nota.disabled = True
        self.view.lbl_editor_titulo.value = "Selecciona una nota"
        self.view.lbl_editor_meta.value = ""
        self.view.txt_editor_contenido.value = ""
        self.view.txt_editor_contenido.disabled = True

        self.refrescar_ui_secciones()

    def eliminar_categoria(self, categoria):
        self._pedir_confirmacion_eliminar(
            f"¿Eliminar la tarea '{categoria.nombre}', sus secciones y todas sus notas? Esta acción no se puede deshacer.",
            lambda: self._eliminar_categoria_confirmada(categoria.id),
        )

    def _eliminar_categoria_confirmada(self, categoria_id):
        self.model.eliminar_categoria(categoria_id)
        if self.categoria_seleccionada_id == categoria_id:
            self.categoria_seleccionada_id = None
            self.seccion_seleccionada_id = None
            self.nota_seleccionada_id = None
            self.view.lista_secciones.controls.clear()
            self.view.lista_notas_ui.controls.clear()
            self.view.lbl_tarea_activa.value = ""
            self.view.lbl_seccion_activa.value = ""
            self.view.btn_crear_seccion.disabled = True
            self.view.btn_crear_nota.disabled = True
            self.view.lbl_editor_titulo.value = "Selecciona una nota"
            self.view.lbl_editor_meta.value = ""
            self.view.txt_editor_contenido.value = ""
            self.view.txt_editor_contenido.disabled = True
        self.refrescar_ui_categorias()
        self.refrescar_calendario_eventos()

    # --- LÓGICA DE NEGOCIO: SECCIONES ---
    def guardar_seccion(self, e):
        nombre = self.view.txt_nombre_seccion.value
        color = self.view.drop_color_seccion.value
        if not nombre or not self.categoria_seleccionada_id:
            return

        if self._seccion_editando_id:
            self.model.editar_seccion(self._seccion_editando_id, nombre, color)
            self._seccion_editando_id = None
        else:
            self.model.crear_seccion(nombre, color, self.categoria_seleccionada_id)

        self.cerrar_dialogos()
        self.refrescar_ui_secciones()

    def refrescar_ui_secciones(self):
        self.view.lista_secciones.controls.clear()
        if self.categoria_seleccionada_id:
            secciones = self.model.obtener_secciones_por_categoria(self.categoria_seleccionada_id)
            for sec in secciones:
                self.view.lista_secciones.controls.append(self.view.crear_item_seccion(sec))
        self.actualizar_pantalla()

    def seleccionar_seccion(self, seccion):
        self.seccion_seleccionada_id = seccion.id
        self.nota_seleccionada_id = None

        self.view.lbl_seccion_activa.value = f"· {seccion.nombre}"
        self.view.btn_crear_nota.disabled = False
        self.view.lbl_editor_titulo.value = "Selecciona una nota"
        self.view.lbl_editor_meta.value = ""
        self.view.txt_editor_contenido.value = ""
        self.view.txt_editor_contenido.disabled = True

        self.refrescar_ui_notas()

    def eliminar_seccion(self, seccion):
        self._pedir_confirmacion_eliminar(
            f"¿Eliminar la sección '{seccion.nombre}' y todas sus notas? Esta acción no se puede deshacer.",
            lambda: self._eliminar_seccion_confirmada(seccion.id),
        )

    def _eliminar_seccion_confirmada(self, seccion_id):
        self.model.eliminar_seccion(seccion_id)
        if self.seccion_seleccionada_id == seccion_id:
            self.seccion_seleccionada_id = None
            self.nota_seleccionada_id = None
            self.view.lista_notas_ui.controls.clear()
            self.view.lbl_seccion_activa.value = ""
            self.view.btn_crear_nota.disabled = True
            self.view.lbl_editor_titulo.value = "Selecciona una nota"
            self.view.lbl_editor_meta.value = ""
            self.view.txt_editor_contenido.value = ""
            self.view.txt_editor_contenido.disabled = True
        self.refrescar_ui_secciones()
        self.refrescar_calendario_eventos()

    # --- LÓGICA DE NEGOCIO: NOTAS ---
    def prioridad_cambiada(self, e):
        self.view.fila_color_anotacion.visible = (self.view.drop_prioridad_nota.value == "anotacion")
        self.actualizar_pantalla()

    def color_anotacion_elegido(self, color):
        self._color_anotacion_nota_actual = color
        self.actualizar_pantalla()

    def guardar_nueva_nota(self, e):
        titulo = self.view.txt_titulo_nota.value
        descripcion = self.view.txt_descripcion_nota.value or ""
        prioridad = self.view.drop_prioridad_nota.value or "media"

        if self.view.drop_seccion_nota.visible:
            seccion_id = self.view.drop_seccion_nota.value
        else:
            seccion_id = str(self.seccion_seleccionada_id) if self.seccion_seleccionada_id else None

        if not titulo or not seccion_id:
            return

        color_anotacion = self._color_anotacion_nota_actual if prioridad == "anotacion" else None

        if self._nota_editando_id:
            self.model.editar_nota(
                self._nota_editando_id, titulo, descripcion, int(seccion_id),
                self._fecha_evento_nota_actual, self._hora_inicio_nota_actual, self._hora_fin_nota_actual,
                prioridad, color_anotacion,
                self._ruta_adjunto_nota_actual, self._nombre_adjunto_nota_actual,
            )
            self._nota_editando_id = None
        else:
            self.model.crear_nota(
                titulo, int(seccion_id), descripcion=descripcion,
                fecha_evento=self._fecha_evento_nota_actual,
                hora_inicio=self._hora_inicio_nota_actual, hora_fin=self._hora_fin_nota_actual,
                prioridad=prioridad, color_anotacion=color_anotacion,
                ruta_adjunto=self._ruta_adjunto_nota_actual, nombre_adjunto=self._nombre_adjunto_nota_actual,
            )

        self.seccion_seleccionada_id = int(seccion_id)
        self._fecha_evento_nota_actual = None
        self._hora_inicio_nota_actual = None
        self._hora_fin_nota_actual = None
        self._color_anotacion_nota_actual = None
        self._ruta_adjunto_nota_actual = None
        self._nombre_adjunto_nota_actual = None

        self.cerrar_dialogos()
        self.refrescar_ui_notas()
        self.refrescar_calendario_eventos()

    def refrescar_ui_notas(self):
        self.view.lista_notas_ui.controls.clear()
        if self.seccion_seleccionada_id:
            notas = self.model.obtener_notas_por_seccion(self.seccion_seleccionada_id)
            for nota in notas:
                self.view.lista_notas_ui.controls.append(self.view.crear_item_nota(nota))
        self.actualizar_pantalla()

    def seleccionar_nota(self, nota):
        self.nota_seleccionada_id = nota.id
        etiqueta = {"alta": "Alta", "media": "Media", "baja": "Baja", "anotacion": "Anotación"}.get(nota.prioridad, "Media")
        fecha_mostrar = nota.fecha_evento.strftime("%d/%m/%Y") if nota.fecha_evento else nota.fecha
        self.view.lbl_editor_titulo.value = nota.titulo
        self.view.lbl_editor_meta.value = f"{etiqueta} · {fecha_mostrar}" + (f" · 📎 {nota.nombre_adjunto}" if nota.nombre_adjunto else "")
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
            self.view.lbl_editor_meta.value = ""
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

    # --- ADJUNTOS ---
    async def abrir_selector_imagen(self, e):
        self._asegurar_overlay()
        archivos = await self.view.selector_archivo.pick_files(
            allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE,
        )
        self._procesar_archivo_seleccionado(archivos)

    async def abrir_selector_documento(self, e):
        self._asegurar_overlay()
        archivos = await self.view.selector_archivo.pick_files(
            allow_multiple=False, file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["pdf", "doc", "docx", "xls", "xlsx", "txt"],
        )
        self._procesar_archivo_seleccionado(archivos)

    def _procesar_archivo_seleccionado(self, archivos):
        if archivos:
            archivo = archivos[0]
            self._ruta_adjunto_nota_actual = archivo.path
            self._nombre_adjunto_nota_actual = archivo.name
            self.view.lbl_adjunto_nota.value = f"📎 {archivo.name}"
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