# modules/tasks/view.py
import flet as ft

class TasksView(ft.Container):
    def __init__(self, controlador):
        super().__init__(expand=True)
        self.controlador = controlador

        # --- COLUMNA 1: CATEGORÍAS---
        self.col_secciones = ft.Column(
            width=220,
            controls=[
                ft.Row([
                    ft.Text("Notas", size=24, weight=ft.FontWeight.BOLD), 
                    ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_MONTH, color="grey", size=18),
                        ft.Icon(ft.Icons.MORE_HORIZ, color="grey", size=18),
                    ], spacing=5)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=10),
                ft.Container(expand=True), 
                ft.ElevatedButton(
                    "+ Crear Sección", 
                    bgcolor="#f28b44", 
                    color="white", 
                    width=220, 
                    icon=ft.Icons.COLOR_LENS, 
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                )
            ]
        )

        # --- COLUMNA 2: LISTA DE NOTAS ---
        self.col_lista = ft.Column(
            width=250,
            controls=[
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "+ Crear Nota", 
                    width=250, 
                    bgcolor="#f0f2f5", 
                    color="#333333",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))
                )
            ]
        )

        # --- COLUMNA 3: EDITOR DE NOTA ---
        self.col_editor = ft.Container(
            expand=True,
            bgcolor="white",
            border_radius=10,
            content=ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    # Cabecera Turquesa
                    ft.Container(
                        bgcolor="#26a69a", padding=20, 
                        border_radius=10, 
                        width=float("inf"), 
                        content=ft.Text("App Feature Ideas", color="white", size=20, weight=ft.FontWeight.BOLD)
                    ),
                    ft.Container(
                        padding=20,
                        expand=True,
                        content=ft.Column([
                            ft.Container(expand=True), 
                            ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                controls=[
                                    ft.OutlinedButton("Guardar Borrador", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20), color="#555555")),
                                    ft.ElevatedButton("Guardar", bgcolor="#26a69a", color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)))
                                ]
                            )
                        ])
                    )
                ]
            )
        )

        # --- C4: CALENDARIO ---
        dias = ["Lun", "Luns", "Miércoles", "Jiercoles", "Fr", "Sa", "Sun"]
        columnas_dias = []
        
        for dia in dias:
            bloques = [] 
            columnas_dias.append(
                ft.Column([
                    ft.Text(dia, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, width=80),
                    ft.Container(bgcolor="#f4f6f9", border_radius=10, width=80, height=130, padding=5, content=ft.Column(bloques, spacing=5))
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )

        self.seccion_horario = ft.Container(
            padding=15, bgcolor="white", border_radius=15, margin=20,
            content=ft.Column([
                ft.Text("Horario de Actividades", weight=ft.FontWeight.BOLD, size=16),
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