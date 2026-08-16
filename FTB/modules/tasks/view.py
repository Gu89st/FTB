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
        # DIÁLOGO: NUEVA SECCIÓN (categoría)
        # ============================================================
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
            title=ft.Text("Nueva Sección"),
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
        # DIÁLOGO: NUEVA NOTA
        # ============================================================
        self.txt_titulo_nota = ft.TextField(label="Título", width=340)
        self.txt_descripcion_nota = ft.TextField(
            label="Descripción", width=340, multiline=True, min_lines=3, max_lines=5
        )
        self.drop_seccion_nota = ft.Dropdown(
            label="Agregar a la sección",
            width=340,
            options=[],  # se llena dinámicamente al abrir el diálogo
        )
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

        self.dialogo_nota = ft.AlertDialog(
            title=ft.Text("Nueva Nota"),
            content=ft.Column(
                [
                    self.txt_titulo_nota,
                    self.txt_descripcion_nota,
                    self.drop_seccion_nota,
                    ft.Row(
                        [self.btn_agendar_evento, self.lbl_fecha_evento_nota],
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
        # SELECTOR DE FECHA FLOTANTE (mes actual y meses siguientes)
        # ============================================================
        self.date_picker = ft.DatePicker(
            first_date=datetime(2020, 1, 1),
            last_date=datetime(2035, 12, 31),
            current_date=datetime.now(),
            on_change=self.controlador.fecha_seleccionada,
        )

        # ============================================================
        # COLUMNA 1: SECCIONES (antes "Notas")
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
                    on_click=self.controlador.abrir_dialogo_categoria
                )
            ]
        )

        # ============================================================
        # COLUMNA 2: LISTA DE NOTAS (encabezado "Notas" + categoría activa)
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
            on_click=self.controlador.abrir_dialogo_nota,
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
        # C4: CALENDARIO SEMANAL DINÁMICO
        # ============================================================
        self.dia_headers = []       # ft.Text por día (nombre + número)
        self.dia_contenedores = []  # ft.Container por día (para resaltar "hoy")
        columnas_dias = []

        for nombre in NOMBRES_DIAS:
            header = ft.Text(nombre, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
            contenedor = ft.Container(
                bgcolor="#f4f6f9", border_radius=10, width=80, height=130, padding=5,
                content=ft.Column([], spacing=5)
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
                            ],
                            spacing=0,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(columnas_dias, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ])
        )

        self.content = ft.Column([
            ft.Row([
                self.col_secciones,
                ft.VerticalDivider(width=1, color="#eeeeee"),
                self.col_lista,
                ft.VerticalDivider(width=1, color="#eeeeee"),
                self.col_editor
            ], expand=True, vertical_alignment=ft.CrossAxisAlignment.STRETCH),
            self.seccion_horario
        ], expand=True)

        # Pinta la semana actual desde el arranque
        hoy = date.today()
        self.actualizar_semana(hoy - timedelta(days=hoy.weekday()))

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
    # Pinta como bloques las notas con fecha_evento dentro de la semana
    # mostrada actualmente. 'notas' es una lista de objetos Nota con
    # atributo fecha_evento (date) ya filtrados por el controlador.
    # ================================================================
    def pintar_eventos_semana(self, fecha_inicio, notas):
        for contenedor in self.dia_contenedores:
            contenedor.content.controls.clear()

        for nota in notas:
            if not nota.fecha_evento:
                continue
            indice = (nota.fecha_evento - fecha_inicio).days
            if 0 <= indice <= 6:
                bloque = ft.Container(
                    bgcolor="#26a69a",
                    border_radius=6,
                    padding=6,
                    content=ft.Text(
                        nota.titulo, size=10, color="white",
                        max_lines=2, overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                )
                self.dia_contenedores[indice].content.controls.append(bloque)