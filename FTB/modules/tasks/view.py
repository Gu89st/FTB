# modules/tasks/view.py
import flet as ft
from datetime import date, timedelta, datetime

NOMBRES_DIAS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
NOMBRES_MESES = ["ene", "feb", "mar", "abr", "may", "jun",
                  "jul", "ago", "sep", "oct", "nov", "dic"]


class TasksView(ft.Container):
    def __init__(self, controlador):
        super().__init__(expand=True)
        self.controlador = controlador

        # ============================================================
        # DIÁLOGO: SECCIÓN (crear / editar)
        # ============================================================
        self.txt_titulo_dialogo_categoria = ft.Text("Nueva Sección")
        self.txt_nombre_cat = ft.TextField(label="Nombre de la sección", width=300)
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
            content=ft.Column([
                self.txt_nombre_cat,
                self.drop_color_cat
            ], tight=True),
            actions=[
                ft.TextButton(content="Cancelar", on_click=self.controlador.cerrar_dialogos),
                ft.ElevatedButton(
                    content="Guardar",
                    bgcolor="#f28b44", color="white",
                    on_click=self.controlador.guardar_categoria
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # ============================================================
        # DIÁLOGO: NOTA (crear / editar)
        # ============================================================
        self.txt_titulo_dialogo_nota = ft.Text("Nueva Nota")
        self.txt_titulo_nota = ft.TextField(label="Título", width=340)
        self.txt_descripcion_nota = ft.TextField(
            label="Descripción", width=340, multiline=True, min_lines=3, max_lines=5
        )

        # Selector de sección: solo se muestra si no había una sección
        # ya activa al abrir el diálogo (ver abrir_dialogo_nota).
        self.drop_seccion_nota = ft.Dropdown(
            label="Agregar a la sección",
            width=340,
            options=[],
            visible=True,
        )
        self.lbl_seccion_fija_nota = ft.Text("", size=13, color="grey", visible=False)

        self.lbl_fecha_evento_nota = ft.Text("Sin fecha", size=13, color="grey")
        self.btn_agendar_evento = ft.OutlinedButton(
            content=ft.Row(
                [ft.Icon(ft.Icons.CALENDAR_MONTH, size=18), ft.Text("Agendar evento")],
                spacing=6, tight=True,
            ),
            on_click=self.controlador.abrir_selector_fecha_nota,
        )
        self.date_picker_nota = ft.DatePicker(
            first_date=datetime(2020, 1, 1),
            last_date=datetime(2035, 12, 31),
            current_date=datetime.now(),
            on_change=self.controlador.fecha_evento_seleccionada,
        )

        # Hora de inicio / fin del evento
        self.lbl_hora_inicio_nota = ft.Text("--:--", size=13, color="grey")
        self.btn_hora_inicio = ft.OutlinedButton(
            content=ft.Row(
                [ft.Icon(ft.Icons.SCHEDULE, size=18), ft.Text("Hora inicio")],
                spacing=6, tight=True,
            ),
            on_click=self.controlador.abrir_selector_hora_inicio,
        )
        self.lbl_hora_fin_nota = ft.Text("--:--", size=13, color="grey")
        self.btn_hora_fin = ft.OutlinedButton(
            content=ft.Row(
                [ft.Icon(ft.Icons.SCHEDULE, size=18), ft.Text("Hora fin")],
                spacing=6, tight=True,
            ),
            on_click=self.controlador.abrir_selector_hora_fin,
        )
        self.time_picker_inicio = ft.TimePicker(on_change=self.controlador.hora_inicio_seleccionada)
        self.time_picker_fin = ft.TimePicker(on_change=self.controlador.hora_fin_seleccionada)

        self.dialogo_nota = ft.AlertDialog(
            title=self.txt_titulo_dialogo_nota,
            content=ft.Column(
                [
                    self.txt_titulo_nota,
                    self.txt_descripcion_nota,
                    self.drop_seccion_nota,
                    self.lbl_seccion_fija_nota,
                    ft.Row(
                        [self.btn_agendar_evento, self.lbl_fecha_evento_nota],
                        spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [self.btn_hora_inicio, self.lbl_hora_inicio_nota,
                         self.btn_hora_fin, self.lbl_hora_fin_nota],
                        spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                tight=True, spacing=12,
            ),
            actions=[
                ft.TextButton(content="Cancelar", on_click=self.controlador.cerrar_dialogos),
                ft.ElevatedButton(
                    content="Guardar",
                    bgcolor="#26a69a", color="white",
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
                    content="Eliminar",
                    bgcolor="#e53935", color="white",
                    on_click=self.controlador.confirmar_eliminacion,
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # ============================================================
        # SELECTOR DE FECHA FLOTANTE (calendario semanal → mes)
        # ============================================================
        self.date_picker = ft.DatePicker(
            first_date=datetime(2020, 1, 1),
            last_date=datetime(2035, 12, 31),
            current_date=datetime.now(),
            on_change=self.controlador.fecha_seleccionada,
        )

        # ============================================================
        # COLUMNA 1: SECCIONES
        # ============================================================
        self.lista_categorias = ft.Column(
            spacing=8,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        self.col_secciones = ft.Column(
            width=220,
            controls=[
                ft.Row([
                    ft.Text("Secciones", size=24, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_MONTH, color="grey", size=18),
                        ft.Icon(ft.Icons.MORE_HORIZ, color="grey", size=18),
                    ], spacing=5)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=10),
                self.lista_categorias,

                ft.ElevatedButton(
                    content="+ Crear Sección",
                    bgcolor="#f28b44",
                    color="white",
                    width=220,
                    icon=ft.Icons.COLOR_LENS,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=lambda e: self.controlador.abrir_dialogo_categoria(e)
                )
            ]
        )

        # ============================================================
        # COLUMNA 2: LISTA DE NOTAS
        # ============================================================
        self.lbl_categoria_seleccionada = ft.Text(
            "", size=13, color="grey", weight=ft.FontWeight.W_500
        )

        self.lista_notas_ui = ft.Column(
            spacing=8,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        self.btn_crear_nota = ft.ElevatedButton(
            content="+ Crear Nota",
            width=250,
            bgcolor="#f0f2f5",
            color="#333333",
            disabled=True,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            on_click=lambda e: self.controlador.abrir_dialogo_nota(e),
        )

        self.col_lista = ft.Column(
            width=250,
            controls=[
                ft.Row(
                    [
                        ft.Text("Notas", size=20, weight=ft.FontWeight.BOLD),
                        self.lbl_categoria_seleccionada,
                    ],
                    spacing=8,
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Container(height=10),
                self.lista_notas_ui,
                self.btn_crear_nota,
            ]
        )

        # ============================================================
        # COLUMNA 3: EDITOR DE NOTA
        # ============================================================
        self.lbl_editor_titulo = ft.Text(
            "Selecciona una nota", color="white", size=20, weight=ft.FontWeight.BOLD
        )

        self.txt_editor_contenido = ft.TextField(
            multiline=True,
            expand=True,
            disabled=True,
            border=ft.InputBorder.NONE,
            on_change=self.controlador.actualizar_texto_nota,
        )

        self.col_editor = ft.Container(
            expand=True,
            bgcolor="white",
            border_radius=10,
            content=ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    ft.Container(
                        bgcolor="#26a69a", padding=20,
                        border_radius=10,
                        width=float("inf"),
                        content=self.lbl_editor_titulo
                    ),
                    ft.Container(
                        padding=20,
                        expand=True,
                        content=ft.Column([
                            ft.Container(content=self.txt_editor_contenido, expand=True),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                controls=[
                                    ft.OutlinedButton(
                                        content="Guardar Borrador",
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=20),
                                            color="#555555"
                                        )
                                    ),
                                    ft.ElevatedButton(
                                        content="Guardar",
                                        bgcolor="#26a69a", color="white",
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
        # MANIJAS DE REDIMENSIONADO (arrastrar para ajustar anchos/alto)
        # ============================================================
        self.manija_secciones = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.RESIZE_LEFT_RIGHT,
            drag_interval=10,
            on_pan_update=self._redimensionar_secciones,
            content=ft.Container(width=6, bgcolor="#eeeeee"),
        )
        self.manija_lista = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.RESIZE_LEFT_RIGHT,
            drag_interval=10,
            on_pan_update=self._redimensionar_lista,
            content=ft.Container(width=6, bgcolor="#eeeeee"),
        )

        # ============================================================
        # C4: CALENDARIO SEMANAL DINÁMICO
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
                ft.Column(
                    [header, contenedor],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    width=80,
                )
            )

        self.lbl_rango_semana = ft.Text("", size=12, color="grey")

        self.fila_dias_calendario = ft.Row(columnas_dias, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        self.manija_calendario = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.RESIZE_UP_DOWN,
            drag_interval=10,
            on_pan_update=self._redimensionar_calendario,
            content=ft.Container(height=8, border_radius=4, bgcolor="#eeeeee", margin=ft.Margin(left=0, top=8, right=0, bottom=0)),
        )

        self.btn_colapsar_calendario = ft.IconButton(
            icon=ft.Icons.EXPAND_LESS,
            tooltip="Contraer/expandir calendario",
            on_click=self._alternar_calendario,
        )

        self.seccion_horario = ft.Container(
            padding=15, bgcolor="white", border_radius=15, margin=20,
            content=ft.Column([
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("Horario de Actividades", weight=ft.FontWeight.BOLD, size=16),
                                self.lbl_rango_semana,
                            ],
                            spacing=0,
                        ),
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.CHEVRON_LEFT,
                                    tooltip="Semana anterior",
                                    on_click=self.controlador.semana_anterior,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.CALENDAR_MONTH,
                                    tooltip="Ver mes",
                                    on_click=self.controlador.abrir_selector_fecha,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.CHEVRON_RIGHT,
                                    tooltip="Semana siguiente",
                                    on_click=self.controlador.semana_siguiente,
                                ),
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
                self.manija_secciones,
                self.col_lista,
                self.manija_lista,
                self.col_editor
            ], expand=True, vertical_alignment=ft.CrossAxisAlignment.STRETCH),
            self.seccion_horario
        ], expand=True)

        # Pinta la semana actual desde el arranque
        hoy = date.today()
        self.actualizar_semana(hoy - timedelta(days=hoy.weekday()))

    # ================================================================
    # Redimensionado con arrastre (drag) de los tres paneles y del
    # bloque de calendario. Los límites min/max evitan que el usuario
    # colapse o desborde el layout arrastrando de más.
    # ================================================================
    def _redimensionar_secciones(self, e: ft.DragUpdateEvent):
        nuevo_ancho = self.col_secciones.width + e.local_delta.x
        self.col_secciones.width = max(160, min(400, nuevo_ancho))
        if self.page:
            self.page.update()

    def _redimensionar_lista(self, e: ft.DragUpdateEvent):
        nuevo_ancho = self.col_lista.width + e.local_delta.x
        self.col_lista.width = max(180, min(450, nuevo_ancho))
        if self.page:
            self.page.update()

    def _redimensionar_calendario(self, e: ft.DragUpdateEvent):
        nuevo_alto = self.dia_contenedores[0].height + e.local_delta.y
        nuevo_alto = max(80, min(400, nuevo_alto))
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
            self.dia_contenedores[i].border = (
                ft.Border.all(2, "#26a69a") if es_hoy else None
            )

        fin = fecha_inicio + timedelta(days=6)
        if fecha_inicio.month == fin.month:
            self.lbl_rango_semana.value = (
                f"{fecha_inicio.day} - {fin.day} {NOMBRES_MESES[fin.month - 1]} {fin.year}"
            )
        else:
            self.lbl_rango_semana.value = (
                f"{fecha_inicio.day} {NOMBRES_MESES[fecha_inicio.month - 1]} - "
                f"{fin.day} {NOMBRES_MESES[fin.month - 1]} {fin.year}"
            )

    # ================================================================
    # Convierte "HH:MM" a minutos desde medianoche.
    # ================================================================
    def _minutos(self, hora_str):
        h, m = hora_str.split(":")
        return int(h) * 60 + int(m)

    # ================================================================
    # Pinta las notas con fecha_evento dentro de la semana mostrada.
    # Las que tienen hora_inicio se ubican verticalmente según esa hora
    # (línea de tiempo de 00:00 a 23:59 sobre el alto del día). Las que
    # no tienen hora quedan como una franja compacta arriba del todo.
    # Cada bloque es clickeable y abre el detalle/edición de la nota.
    # ================================================================
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

            # Notas sin hora: franja compacta arriba del todo
            for i, nota in enumerate(sin_hora):
                controles_stack.append(
                    ft.Container(
                        top=i * 22, left=0, right=0, height=20,
                        bgcolor="#26a69a", border_radius=4, padding=2,
                        content=ft.Text(
                            nota.titulo, size=9, color="white",
                            max_lines=1, overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        on_click=lambda e, n=nota: self.controlador.abrir_dialogo_nota(e, nota=n),
                    )
                )

            offset_sin_hora = len(sin_hora) * 22
            alto_timeline = max(20, alto_total - offset_sin_hora)

            # Notas con hora: posicionadas proporcionalmente según hora_inicio
            for nota in con_hora:
                minutos_inicio = self._minutos(nota.hora_inicio)
                top = offset_sin_hora + (minutos_inicio / MINUTOS_DIA) * alto_timeline

                if nota.hora_fin:
                    minutos_fin = self._minutos(nota.hora_fin)
                    duracion = max(15, minutos_fin - minutos_inicio)
                else:
                    duracion = 30
                alto_bloque = max(18, (duracion / MINUTOS_DIA) * alto_timeline)

                rango_hora = nota.hora_inicio + (f" - {nota.hora_fin}" if nota.hora_fin else "")
                controles_stack.append(
                    ft.Container(
                        top=top, left=2, right=2, height=alto_bloque,
                        bgcolor="#26a69a", border_radius=6, padding=4,
                        content=ft.Column(
                            [
                                ft.Text(
                                    nota.titulo, size=9, color="white", weight=ft.FontWeight.BOLD,
                                    max_lines=1, overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                ft.Text(rango_hora, size=8, color="white"),
                            ],
                            spacing=0, tight=True,
                        ),
                        on_click=lambda e, n=nota: self.controlador.abrir_dialogo_nota(e, nota=n),
                    )
                )

            contenedor.content = ft.Stack(controles_stack, expand=True)

    # ================================================================
    # Construye la fila visual de una sección, con menú de 3 puntos
    # (Editar / Eliminar).
    # ================================================================
    def crear_item_categoria(self, categoria):
        return ft.Container(
            content=ft.Row([
                ft.Text(categoria.nombre, color="white", weight="bold", expand=True),
                ft.PopupMenuButton(
                    icon=ft.Icons.MORE_VERT,
                    icon_color="white",
                    items=[
                        ft.PopupMenuItem(
                            content="Editar",
                            icon=ft.Icons.EDIT,
                            on_click=lambda e, c=categoria: self.controlador.abrir_dialogo_categoria(e, categoria=c),
                        ),
                        ft.PopupMenuItem(
                            content="Eliminar",
                            icon=ft.Icons.DELETE,
                            on_click=lambda e, c=categoria: self.controlador.eliminar_categoria(c),
                        ),
                    ],
                ),
            ]),
            bgcolor=categoria.color, padding=10, border_radius=10,
            on_click=lambda e, c=categoria: self.controlador.seleccionar_categoria(c),
        )

    # ================================================================
    # Construye la tarjeta visual de una nota, con menú de 3 puntos
    # (Editar / Eliminar).
    # ================================================================
    def crear_item_nota(self, nota):
        return ft.Card(
            elevation=1,
            content=ft.Container(
                bgcolor="#e0f2f1", padding=15, border_radius=10,
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(nota.titulo, weight="bold", color="black87"),
                                ft.Text(nota.fecha, color="grey", size=12),
                            ],
                            spacing=2, expand=True,
                        ),
                        ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT,
                            items=[
                                ft.PopupMenuItem(
                                    content="Editar",
                                    icon=ft.Icons.EDIT,
                                    on_click=lambda e, n=nota: self.controlador.abrir_dialogo_nota(e, nota=n),
                                ),
                                ft.PopupMenuItem(
                                    content="Eliminar",
                                    icon=ft.Icons.DELETE,
                                    on_click=lambda e, n=nota: self.controlador.eliminar_nota(n),
                                ),
                            ],
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                on_click=lambda e, n=nota: self.controlador.seleccionar_nota(n),
            ),
        )