# modules/tasks/view.py
import flet as ft
from datetime import date, timedelta, datetime

NOMBRES_DIAS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
NOMBRES_MESES = ["ene", "feb", "mar", "abr", "may", "jun",
                  "jul", "ago", "sep", "oct", "nov", "dic"]

COLORES_PRIORIDAD = {
    "alta": "#e53935",
    "media": "#fdd835",
    "baja": "#3949ab",
}
ETIQUETAS_PRIORIDAD = {
    "alta": "Alta",
    "media": "Media",
    "baja": "Baja",
    "anotacion": "Anotación",
}
COLORES_ANOTACION = ["#26a69a", "#f28b44", "#e53935", "#8e24aa", "#3949ab", "#43a047"]


class TasksView(ft.Container):
    def __init__(self, controlador):
        super().__init__(expand=True)
        self.controlador = controlador

        # ============================================================
        # DIÁLOGO: TAREA (crear / editar) — antes "Sección"
        # ============================================================
        self.txt_titulo_dialogo_categoria = ft.Text("Nueva Tarea")
        self.txt_nombre_cat = ft.TextField(label="Nombre de la tarea", width=300)
        self.drop_color_cat = ft.Dropdown(
            label="Color",
            width=300,
            value="#26a69a",
            options=[
                ft.DropdownOption(key="#26a69a", text="Turquesa"),
                ft.DropdownOption(key="#f28b44", text="Naranja"),
                ft.DropdownOption(key="#e53935", text="Rojo"),
                ft.DropdownOption(key="#8e24aa", text="Morado"),
                ft.DropdownOption(key="#3949ab", text="Azul"),
            ]
        )
        self.dialogo_categoria = ft.AlertDialog(
            title=self.txt_titulo_dialogo_categoria,
            content=ft.Column([self.txt_nombre_cat, self.drop_color_cat], tight=True),
            actions=[
                ft.TextButton(content="Cancelar", on_click=self.controlador.cerrar_dialogos),
                ft.ElevatedButton(
                    content="Guardar", bgcolor="#f28b44", color="white",
                    on_click=self.controlador.guardar_categoria
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # ============================================================
        # DIÁLOGO: SECCIÓN (crear / editar) — nueva
        # ============================================================
        self.txt_titulo_dialogo_seccion = ft.Text("Nueva Sección")
        self.txt_nombre_seccion = ft.TextField(label="Nombre de la sección", width=300)
        self.drop_color_seccion = ft.Dropdown(
            label="Color",
            width=300,
            value="#26a69a",
            options=[
                ft.DropdownOption(key="#26a69a", text="Turquesa"),
                ft.DropdownOption(key="#f28b44", text="Naranja"),
                ft.DropdownOption(key="#e53935", text="Rojo"),
                ft.DropdownOption(key="#8e24aa", text="Morado"),
                ft.DropdownOption(key="#3949ab", text="Azul"),
            ]
        )
        self.dialogo_seccion = ft.AlertDialog(
            title=self.txt_titulo_dialogo_seccion,
            content=ft.Column([self.txt_nombre_seccion, self.drop_color_seccion], tight=True),
            actions=[
                ft.TextButton(content="Cancelar", on_click=self.controlador.cerrar_dialogos),
                ft.ElevatedButton(
                    content="Guardar", bgcolor="#26a69a", color="white",
                    on_click=self.controlador.guardar_seccion
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # ============================================================
        # DIÁLOGO: NOTA (crear / editar)
        # ============================================================
        self.txt_titulo_dialogo_nota = ft.Text("Nueva Nota")
        self.txt_titulo_nota = ft.TextField(label="Título", width=360)
        self.txt_descripcion_nota = ft.TextField(
            label="Descripción", width=360, multiline=True, min_lines=3, max_lines=5
        )

        # Selector de sección (solo visible si no había una sección ya activa)
        self.drop_seccion_nota = ft.Dropdown(label="Agregar a la sección", width=360, options=[], visible=True)
        self.lbl_seccion_fija_nota = ft.Text("", size=13, color="grey", visible=False)

        # Prioridad
        self.drop_prioridad_nota = ft.Dropdown(
            label="Prioridad",
            width=170,
            value="media",
            options=[
                ft.DropdownOption(key="alta", text="Alta"),
                ft.DropdownOption(key="media", text="Media"),
                ft.DropdownOption(key="baja", text="Baja"),
                ft.DropdownOption(key="anotacion", text="Anotación"),
            ],
            on_select=self.controlador.prioridad_cambiada,
        )
        self.fila_color_anotacion = ft.Row(
            [ft.Text("Color:", size=12, color="grey")] + [
                ft.GestureDetector(
                    content=ft.Container(width=22, height=22, bgcolor=c, border_radius=11),
                    on_tap=lambda e, c=c: self.controlador.color_anotacion_elegido(c),
                )
                for c in COLORES_ANOTACION
            ],
            spacing=6, visible=False,
        )

        # Fecha y hora del evento
        self.lbl_fecha_evento_nota = ft.Text("Sin fecha", size=13, color="grey")
        self.btn_agendar_evento = ft.OutlinedButton(
            content=ft.Row([ft.Icon(ft.Icons.CALENDAR_MONTH, size=18), ft.Text("Fecha")], spacing=6, tight=True),
            on_click=self.controlador.abrir_selector_fecha_nota,
        )
        self.date_picker_nota = ft.DatePicker(
            first_date=datetime(2020, 1, 1), last_date=datetime(2035, 12, 31),
            current_date=datetime.now(), on_change=self.controlador.fecha_evento_seleccionada,
        )

        self.lbl_hora_inicio_nota = ft.Text("--:--", size=13, color="grey")
        self.btn_hora_inicio = ft.OutlinedButton(
            content=ft.Row([ft.Icon(ft.Icons.SCHEDULE, size=18), ft.Text("Inicio")], spacing=6, tight=True),
            on_click=self.controlador.abrir_selector_hora_inicio,
        )
        self.lbl_hora_fin_nota = ft.Text("--:--", size=13, color="grey")
        self.btn_hora_fin = ft.OutlinedButton(
            content=ft.Row([ft.Icon(ft.Icons.SCHEDULE, size=18), ft.Text("Fin")], spacing=6, tight=True),
            on_click=self.controlador.abrir_selector_hora_fin,
        )
        self.time_picker_inicio = ft.TimePicker(on_change=self.controlador.hora_inicio_seleccionada)
        self.time_picker_fin = ft.TimePicker(on_change=self.controlador.hora_fin_seleccionada)

        # Adjuntos
        self.lbl_adjunto_nota = ft.Text("Sin adjunto", size=13, color="grey")
        self.btn_adjuntar_imagen = ft.OutlinedButton(
            content=ft.Row([ft.Icon(ft.Icons.IMAGE, size=18), ft.Text("Imagen")], spacing=6, tight=True),
            on_click=self.controlador.abrir_selector_imagen,
        )
        self.btn_adjuntar_documento = ft.OutlinedButton(
            content=ft.Row([ft.Icon(ft.Icons.ATTACH_FILE, size=18), ft.Text("Documento")], spacing=6, tight=True),
            on_click=self.controlador.abrir_selector_documento,
        )
        self.selector_archivo = ft.FilePicker()

        self.dialogo_nota = ft.AlertDialog(
            title=self.txt_titulo_dialogo_nota,
            content=ft.Column(
                [
                    self.txt_titulo_nota,
                    self.txt_descripcion_nota,
                    self.drop_seccion_nota,
                    self.lbl_seccion_fija_nota,
                    self.drop_prioridad_nota,
                    self.fila_color_anotacion,
                    ft.Row([self.btn_agendar_evento, self.lbl_fecha_evento_nota], spacing=10),
                    ft.Row(
                        [self.btn_hora_inicio, self.lbl_hora_inicio_nota,
                         self.btn_hora_fin, self.lbl_hora_fin_nota],
                        spacing=10,
                    ),
                    ft.Row([self.btn_adjuntar_imagen, self.btn_adjuntar_documento], spacing=10),
                    self.lbl_adjunto_nota,
                ],
                tight=True, spacing=10, scroll=ft.ScrollMode.AUTO, height=420,
            ),
            actions=[
                ft.TextButton(content="Cancelar", on_click=self.controlador.cerrar_dialogos),
                ft.ElevatedButton(
                    content="Guardar", bgcolor="#26a69a", color="white",
                    on_click=self.controlador.guardar_nueva_nota
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # ============================================================
        # DIÁLOGO: CONFIRMAR ELIMINACIÓN (reutilizable)
        # ============================================================
        self.txt_mensaje_confirmar = ft.Text("")
        self.dialogo_confirmar = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=self.txt_mensaje_confirmar,
            actions=[
                ft.TextButton(content="Cancelar", on_click=self.controlador.cerrar_dialogos),
                ft.ElevatedButton(
                    content="Eliminar", bgcolor="#e53935", color="white",
                    on_click=self.controlador.confirmar_eliminacion,
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # ============================================================
        # SELECTOR DE FECHA FLOTANTE (calendario semanal → mes)
        # ============================================================
        self.date_picker = ft.DatePicker(
            first_date=datetime(2020, 1, 1), last_date=datetime(2035, 12, 31),
            current_date=datetime.now(), on_change=self.controlador.fecha_seleccionada,
        )

        # ============================================================
        # COLUMNA 1: TAREAS (antes "Secciones" — lista de Categorías)
        # ============================================================
        self.lista_categorias = ft.Column(spacing=8, expand=True, scroll=ft.ScrollMode.AUTO)

        self.col_secciones = ft.Column(
            width=190,
            controls=[
                ft.Row([
                    ft.Text("Tareas", size=22, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_MONTH, color="grey", size=18),
                        ft.Icon(ft.Icons.MORE_HORIZ, color="grey", size=18),
                    ], spacing=5)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=10),
                self.lista_categorias,
                ft.ElevatedButton(
                    content="+ Crear Tarea", bgcolor="#f28b44", color="white", width=190,
                    icon=ft.Icons.COLOR_LENS,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=lambda e: self.controlador.abrir_dialogo_categoria(e)
                )
            ]
        )

        # ============================================================
        # COLUMNA 2: SECCIONES (nueva — lista de Secciones de la Tarea activa)
        # ============================================================
        self.lbl_tarea_activa = ft.Text("", size=12, color="grey", weight=ft.FontWeight.W_500)
        self.lista_secciones = ft.Column(spacing=8, expand=True, scroll=ft.ScrollMode.AUTO)

        self.btn_crear_seccion = ft.ElevatedButton(
            content="+ Crear Sección", bgcolor="#26a69a", color="white", width=200,
            disabled=True,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=lambda e: self.controlador.abrir_dialogo_seccion(e),
        )

        self.col_subsecciones = ft.Column(
            width=200,
            controls=[
                ft.Text("Secciones", size=20, weight=ft.FontWeight.BOLD),
                self.lbl_tarea_activa,
                ft.Container(height=6),
                self.lista_secciones,
                self.btn_crear_seccion,
            ]
        )

        # ============================================================
        # COLUMNA 3: LISTA DE NOTAS (antes "Notas")
        # ============================================================
        self.lbl_seccion_activa = ft.Text("", size=12, color="grey", weight=ft.FontWeight.W_500)

        self.toolbar_notas = ft.Container(
            bgcolor="#f0f2f5",
            border_radius=10,
            padding=ft.Padding(left=4, top=4, right=4, bottom=4),
            content=ft.Row(
                [
                    ft.IconButton(icon=ft.Icons.ADD_CIRCLE_OUTLINE, tooltip="Nueva nota", icon_size=18,
                                  on_click=lambda e: self.controlador.abrir_dialogo_nota(e)),
                    ft.IconButton(icon=ft.Icons.NOTIFICATIONS_OUTLINED, tooltip="Recordatorio (fecha)", icon_size=18,
                                  on_click=lambda e: self.controlador.abrir_dialogo_nota(e, enfocar_fecha=True)),
                    ft.IconButton(icon=ft.Icons.SCHEDULE, tooltip="Agendar hora", icon_size=18,
                                  on_click=lambda e: self.controlador.abrir_dialogo_nota(e, enfocar_hora=True)),
                    ft.PopupMenuButton(
                        icon=ft.Icons.FLAG_OUTLINED, tooltip="Prioridad", icon_size=18,
                        items=[
                            ft.PopupMenuItem(content="Alta",
                                              on_click=lambda e: self.controlador.abrir_dialogo_nota(e, prioridad_inicial="alta")),
                            ft.PopupMenuItem(content="Media",
                                              on_click=lambda e: self.controlador.abrir_dialogo_nota(e, prioridad_inicial="media")),
                            ft.PopupMenuItem(content="Baja",
                                              on_click=lambda e: self.controlador.abrir_dialogo_nota(e, prioridad_inicial="baja")),
                        ],
                    ),
                    ft.IconButton(icon=ft.Icons.STICKY_NOTE_2_OUTLINED, tooltip="Anotación", icon_size=18,
                                  on_click=lambda e: self.controlador.abrir_dialogo_nota(e, es_anotacion=True)),
                    ft.IconButton(icon=ft.Icons.IMAGE_OUTLINED, tooltip="Adjuntar imagen", icon_size=18,
                                  on_click=lambda e: self.controlador.abrir_dialogo_nota_con_adjunto(e, tipo="imagen")),
                    ft.IconButton(icon=ft.Icons.ATTACH_FILE, tooltip="Adjuntar documento", icon_size=18,
                                  on_click=lambda e: self.controlador.abrir_dialogo_nota_con_adjunto(e, tipo="documento")),
                ],
                spacing=0, wrap=True,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )

        self.lista_notas_ui = ft.Column(spacing=8, expand=True, scroll=ft.ScrollMode.AUTO)

        self.btn_crear_nota = ft.ElevatedButton(
            content="+ Crear Nota", width=230, bgcolor="#f0f2f5", color="#333333", disabled=True,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            on_click=lambda e: self.controlador.abrir_dialogo_nota(e),
        )

        self.col_lista = ft.Column(
            width=230,
            controls=[
                ft.Text("Lista de notas", size=20, weight=ft.FontWeight.BOLD),
                self.lbl_seccion_activa,
                ft.Container(height=6),
                self.lista_notas_ui,
                self.btn_crear_nota,
            ]
        )

        # ============================================================
        # COLUMNA 4: EDITOR DE NOTA
        # ============================================================
        self.lbl_editor_titulo = ft.Text("Selecciona una nota", color="white", size=20, weight=ft.FontWeight.BOLD)
        self.lbl_editor_meta = ft.Text("", color="white", size=12)

        self.txt_editor_contenido = ft.TextField(
            multiline=True, expand=True, disabled=True, border=ft.InputBorder.NONE,
            on_change=self.controlador.actualizar_texto_nota,
        )

        self.col_editor = ft.Container(
            expand=True, bgcolor="white", border_radius=10,
            content=ft.Column(
                expand=True, spacing=8,
                controls=[
                    self.toolbar_notas,
                    ft.Container(
                        bgcolor="#26a69a", padding=20, border_radius=10, width=float("inf"),
                        content=ft.Column([self.lbl_editor_titulo, self.lbl_editor_meta], spacing=4)
                    ),
                    ft.Container(
                        padding=20, expand=True,
                        content=ft.Column([
                            ft.Container(content=self.txt_editor_contenido, expand=True),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                controls=[
                                    ft.OutlinedButton(
                                        content="Guardar Borrador",
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20), color="#555555")
                                    ),
                                    ft.ElevatedButton(
                                        content="Guardar", bgcolor="#26a69a", color="white",
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))
                                    )
                                ]
                            )
                        ])
                    )
                ]
            )
        )

        # ============================================================
        # MANIJAS DE REDIMENSIONADO (arrastrar para ajustar anchos)
        # ============================================================
        self.manija_1 = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.RESIZE_LEFT_RIGHT, drag_interval=10,
            on_pan_update=self._redimensionar_col1,
            content=ft.Container(width=6, bgcolor="#eeeeee"),
        )
        self.manija_2 = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.RESIZE_LEFT_RIGHT, drag_interval=10,
            on_pan_update=self._redimensionar_col2,
            content=ft.Container(width=6, bgcolor="#eeeeee"),
        )
        self.manija_3 = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.RESIZE_LEFT_RIGHT, drag_interval=10,
            on_pan_update=self._redimensionar_col3,
            content=ft.Container(width=6, bgcolor="#eeeeee"),
        )

        # ============================================================
        # CALENDARIO SEMANAL DINÁMICO
        # ============================================================
        self.dia_headers = []
        self.dia_contenedores = []
        columnas_dias = []

        for nombre in NOMBRES_DIAS:
            header = ft.Text(nombre, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
            contenedor = ft.Container(
                bgcolor="#f4f6f9", border_radius=10, width=80, height=130, padding=5,
                content=ft.Stack([], expand=True)
            )
            self.dia_headers.append(header)
            self.dia_contenedores.append(contenedor)
            columnas_dias.append(
                ft.Column([header, contenedor], horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=80)
            )

        self.lbl_rango_semana = ft.Text("", size=12, color="grey")
        self.fila_dias_calendario = ft.Row(columnas_dias, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        self.manija_calendario = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.RESIZE_UP_DOWN, drag_interval=10,
            on_pan_update=self._redimensionar_calendario,
            content=ft.Container(height=8, border_radius=4, bgcolor="#eeeeee",
                                  margin=ft.Margin(left=0, top=8, right=0, bottom=0)),
        )
        self.btn_colapsar_calendario = ft.IconButton(
            icon=ft.Icons.EXPAND_LESS, tooltip="Contraer/expandir calendario",
            on_click=self._alternar_calendario,
        )

        self.seccion_horario = ft.Container(
            padding=15, bgcolor="white", border_radius=15, margin=20,
            content=ft.Column([
                ft.Row(
                    [
                        ft.Column(
                            [ft.Text("Horario de Actividades", weight=ft.FontWeight.BOLD, size=16), self.lbl_rango_semana],
                            spacing=0,
                        ),
                        ft.Row(
                            [
                                ft.IconButton(icon=ft.Icons.CHEVRON_LEFT, tooltip="Semana anterior",
                                              on_click=self.controlador.semana_anterior),
                                ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, tooltip="Ver mes",
                                              on_click=self.controlador.abrir_selector_fecha),
                                ft.IconButton(icon=ft.Icons.CHEVRON_RIGHT, tooltip="Semana siguiente",
                                              on_click=self.controlador.semana_siguiente),
                                self.btn_colapsar_calendario,
                            ],
                            spacing=0,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                self.fila_dias_calendario,
                self.manija_calendario,
            ])
        )

        self.content = ft.Column([
            ft.Row([
                self.col_secciones,
                self.manija_1,
                self.col_subsecciones,
                self.manija_2,
                self.col_lista,
                self.manija_3,
                self.col_editor
            ], expand=True, vertical_alignment=ft.CrossAxisAlignment.STRETCH),
            self.seccion_horario
        ], expand=True)

        hoy = date.today()
        self.actualizar_semana(hoy - timedelta(days=hoy.weekday()))

    # ================================================================
    # Redimensionado con arrastre de las 3 columnas de listas
    # ================================================================
    def _redimensionar_col1(self, e: ft.DragUpdateEvent):
        self.col_secciones.width = max(150, min(350, self.col_secciones.width + e.local_delta.x))
        if self.page:
            self.page.update()

    def _redimensionar_col2(self, e: ft.DragUpdateEvent):
        self.col_subsecciones.width = max(150, min(400, self.col_subsecciones.width + e.local_delta.x))
        if self.page:
            self.page.update()

    def _redimensionar_col3(self, e: ft.DragUpdateEvent):
        self.col_lista.width = max(180, min(450, self.col_lista.width + e.local_delta.x))
        if self.page:
            self.page.update()

    def _redimensionar_calendario(self, e: ft.DragUpdateEvent):
        nuevo_alto = max(80, min(400, self.dia_contenedores[0].height + e.local_delta.y))
        for contenedor in self.dia_contenedores:
            contenedor.height = nuevo_alto
        if self.page:
            self.page.update()

    def _alternar_calendario(self, e):
        self.fila_dias_calendario.visible = not self.fila_dias_calendario.visible
        self.manija_calendario.visible = self.fila_dias_calendario.visible
        self.btn_colapsar_calendario.icon = (
            ft.Icons.EXPAND_LESS if self.fila_dias_calendario.visible else ft.Icons.EXPAND_MORE
        )
        if self.page:
            self.page.update()

    # ================================================================
    # Repinta el calendario semanal a partir del lunes de esa semana
    # ================================================================
    def actualizar_semana(self, fecha_inicio):
        hoy = date.today()
        for i in range(7):
            dia = fecha_inicio + timedelta(days=i)
            self.dia_headers[i].value = f"{NOMBRES_DIAS[i]} {dia.day}"
            es_hoy = dia == hoy
            self.dia_contenedores[i].bgcolor = "#e0f7f5" if es_hoy else "#f4f6f9"
            self.dia_contenedores[i].border = ft.Border.all(2, "#26a69a") if es_hoy else None

        fin = fecha_inicio + timedelta(days=6)
        if fecha_inicio.month == fin.month:
            self.lbl_rango_semana.value = f"{fecha_inicio.day} - {fin.day} {NOMBRES_MESES[fin.month - 1]} {fin.year}"
        else:
            self.lbl_rango_semana.value = (
                f"{fecha_inicio.day} {NOMBRES_MESES[fecha_inicio.month - 1]} - "
                f"{fin.day} {NOMBRES_MESES[fin.month - 1]} {fin.year}"
            )

    def _minutos(self, hora_str):
        h, m = hora_str.split(":")
        return int(h) * 60 + int(m)

    def pintar_eventos_semana(self, fecha_inicio, notas):
        MINUTOS_DIA = 24 * 60
        eventos_por_dia = {i: [] for i in range(7)}
        for nota in notas:
            if not nota.fecha_evento:
                continue
            indice = (nota.fecha_evento - fecha_inicio).days
            if 0 <= indice <= 6:
                eventos_por_dia[indice].append(nota)

        for indice, eventos_dia in eventos_por_dia.items():
            contenedor = self.dia_contenedores[indice]
            alto_total = contenedor.height or 130
            controles_stack = []

            con_hora = [n for n in eventos_dia if n.hora_inicio]
            sin_hora = [n for n in eventos_dia if not n.hora_inicio]

            for i, nota in enumerate(sin_hora):
                color = self._color_prioridad(nota)
                controles_stack.append(
                    ft.Container(
                        top=i * 22, left=0, right=0, height=20, bgcolor=color, border_radius=4, padding=2,
                        content=ft.Text(nota.titulo, size=9, color="white", max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                        on_click=lambda e, n=nota: self.controlador.abrir_dialogo_nota(e, nota=n),
                    )
                )

            offset_sin_hora = len(sin_hora) * 22
            alto_timeline = max(20, alto_total - offset_sin_hora)

            for nota in con_hora:
                minutos_inicio = self._minutos(nota.hora_inicio)
                top = offset_sin_hora + (minutos_inicio / MINUTOS_DIA) * alto_timeline
                if nota.hora_fin:
                    duracion = max(15, self._minutos(nota.hora_fin) - minutos_inicio)
                else:
                    duracion = 30
                alto_bloque = max(18, (duracion / MINUTOS_DIA) * alto_timeline)
                rango_hora = nota.hora_inicio + (f" - {nota.hora_fin}" if nota.hora_fin else "")
                color = self._color_prioridad(nota)

                controles_stack.append(
                    ft.Container(
                        top=top, left=2, right=2, height=alto_bloque, bgcolor=color, border_radius=6, padding=4,
                        content=ft.Column(
                            [
                                ft.Text(nota.titulo, size=9, color="white", weight=ft.FontWeight.BOLD,
                                        max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(rango_hora, size=8, color="white"),
                            ],
                            spacing=0, tight=True,
                        ),
                        on_click=lambda e, n=nota: self.controlador.abrir_dialogo_nota(e, nota=n),
                    )
                )

            contenedor.content = ft.Stack(controles_stack, expand=True)

    # ================================================================
    # Color de acento según la prioridad de la nota (o su color de
    # anotación, si es de tipo "anotacion").
    # ================================================================
    def _color_prioridad(self, nota):
        if nota.prioridad == "anotacion":
            return nota.color_anotacion or "#9e9e9e"
        return COLORES_PRIORIDAD.get(nota.prioridad, COLORES_PRIORIDAD["media"])

    # ================================================================
    # Fila visual de una Tarea (Categoria), con menú de 3 puntos.
    # ================================================================
    def crear_item_categoria(self, categoria):
        return ft.Container(
            content=ft.Row([
                ft.Text(categoria.nombre, color="white", weight="bold", expand=True),
                ft.PopupMenuButton(
                    icon=ft.Icons.MORE_VERT, icon_color="white",
                    items=[
                        ft.PopupMenuItem(content="Editar", icon=ft.Icons.EDIT,
                                          on_click=lambda e, c=categoria: self.controlador.abrir_dialogo_categoria(e, categoria=c)),
                        ft.PopupMenuItem(content="Eliminar", icon=ft.Icons.DELETE,
                                          on_click=lambda e, c=categoria: self.controlador.eliminar_categoria(c)),
                    ],
                ),
            ]),
            bgcolor=categoria.color, padding=15, border_radius=10,
            on_click=lambda e, c=categoria: self.controlador.seleccionar_categoria(c),
        )

    # ================================================================
    # Fila visual de una Sección, con menú de 3 puntos.
    # ================================================================
    def crear_item_seccion(self, seccion):
        return ft.Container(
            content=ft.Row([
                ft.Text(seccion.nombre, color="white", weight="bold", expand=True),
                ft.PopupMenuButton(
                    icon=ft.Icons.MORE_VERT, icon_color="white",
                    items=[
                        ft.PopupMenuItem(content="Editar", icon=ft.Icons.EDIT,
                                          on_click=lambda e, s=seccion: self.controlador.abrir_dialogo_seccion(e, seccion=s)),
                        ft.PopupMenuItem(content="Eliminar", icon=ft.Icons.DELETE,
                                          on_click=lambda e, s=seccion: self.controlador.eliminar_seccion(s)),
                    ],
                ),
            ]),
            bgcolor=seccion.color, padding=13, border_radius=10,
            on_click=lambda e, s=seccion: self.controlador.seleccionar_seccion(s),
        )

    # ================================================================
    # Tarjeta visual de una Nota: barra de color por prioridad, etiqueta
    # de prioridad, fecha, y menú de 3 puntos.
    # ================================================================
    def crear_item_nota(self, nota):
        color = self._color_prioridad(nota)
        etiqueta = ETIQUETAS_PRIORIDAD.get(nota.prioridad, "Media")
        fecha_mostrar = nota.fecha_evento.strftime("%d/%m") if nota.fecha_evento else nota.fecha

        controles_meta = [
            ft.Container(
                content=ft.Text(etiqueta, size=9, color="white"),
                bgcolor=color, padding=ft.Padding(left=6, top=2, right=6, bottom=2), border_radius=8,
            ),
            ft.Text(fecha_mostrar, color="grey", size=11),
        ]
        if nota.nombre_adjunto:
            controles_meta.append(ft.Icon(ft.Icons.ATTACH_FILE, size=12, color="grey"))

        return ft.Container(
            bgcolor="#f7f7f7", border_radius=10, padding=12,
            border=ft.Border(left=ft.BorderSide(width=6, color=color)),
            on_click=lambda e, n=nota: self.controlador.seleccionar_nota(n),
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(nota.titulo, weight="bold", color="black87"),
                            ft.Row(controles_meta, spacing=6),
                        ],
                        spacing=4, expand=True,
                    ),
                    ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(content="Editar", icon=ft.Icons.EDIT,
                                              on_click=lambda e, n=nota: self.controlador.abrir_dialogo_nota(e, nota=n)),
                            ft.PopupMenuItem(content="Eliminar", icon=ft.Icons.DELETE,
                                              on_click=lambda e, n=nota: self.controlador.eliminar_nota(n)),
                        ],
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )