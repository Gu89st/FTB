# modules/tasks/view.py
import flet as ft

class TasksView(ft.Container):
    def __init__(self, controlador):
        super().__init__(expand=True)
        self.controlador = controlador

        # --- COMPONENTES DEL POPUP (CUADRO DE DIÁLOGO) ---
        self.txt_nombre_cat = ft.TextField(label="Nombre de la Sección", width=300)
        self.drop_color_cat = ft.Dropdown(
            label="Elige un Color",
            width=300,
            options=[
                ft.dropdown.Option("#f28b44", text="Naranja"),
                ft.dropdown.Option("#26a69a", text="Turquesa"),
                ft.dropdown.Option("#6abf69", text="Verde"),
                ft.dropdown.Option("#42a5f5", text="Azul"),
                ft.dropdown.Option("#ab47bc", text="Morado")
            ],
            value="#26a69a" # Valor por defecto (Turquesa)
        )
        
        # Este es el popup que se mostrará en pantalla
        self.dialogo_categoria = ft.AlertDialog(
            title=ft.Text("Nueva Sección"),
            content=ft.Column([self.txt_nombre_cat, self.drop_color_cat], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=self.controlador.cerrar_dialogo_categoria),
                ft.ElevatedButton("Guardar", bgcolor="#26a69a", color="white", on_click=self.controlador.guardar_categoria)
            ]
        )

        # --- COLUMNA 1: CATEGORÍAS ---
        self.col_secciones = ft.Column(
            width=220,
            controls=[
                ft.Text("Notas", size=24, weight=ft.FontWeight.BOLD),
                ft.Container(height=10),
                
                # Aquí mostraremos las categorías dinámicas más adelante
                ft.ElevatedButton("Ideas Proyectos (Ejemplo)", bgcolor="#f28b44", color="white", width=200, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
                
                ft.Container(expand=True),
                
                # ¡BOTÓN CONECTADO AL CONTROLADOR!
                ft.ElevatedButton("+ Crear Sección", bgcolor="#f28b44", color="white", width=200, icon="color_lens", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), on_click=self.controlador.abrir_dialogo_categoria)
            ]
        )

        # --- COLUMNA 2: LISTA DE NOTAS (Sin cambios) ---
        self.col_lista = ft.Column(
            width=250,
            controls=[
                ft.Card(
                    elevation=2,
                    content=ft.Container(
                        padding=15, bgcolor="#e0f2f1", border_radius=10,
                        content=ft.Column([
                            ft.Text("App Feature Ideas", weight=ft.FontWeight.BOLD),
                            ft.Text("Nov 15", color="grey", size=12)
                        ])
                    )
                ),
                ft.Container(expand=True),
                ft.ElevatedButton("+ Crear Nota", width=250, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
            ]
        )

        # --- COLUMNA 3: EDITOR DE NOTA (Sin cambios) ---
        self.col_editor = ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    bgcolor="#26a69a", padding=15, border_radius=10, width=float("inf"),
                    content=ft.Text("App Feature Ideas", color="white", size=20, weight=ft.FontWeight.BOLD)
                ),
                ft.TextField(multiline=True, min_lines=10, border=ft.InputBorder.NONE, hint_text="Escribe aquí..."),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.OutlinedButton("Guardar Borrador", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))),
                        ft.ElevatedButton("Guardar", bgcolor="#26a69a", color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)))
                    ]
                )
            ]
        )

        # --- ENSAMBLAJE FINAL ---
        self.content = ft.Row(expand=True, spacing=20, controls=[
            self.col_secciones, ft.VerticalDivider(width=1, color="#eeeeee"),
            self.col_lista, ft.VerticalDivider(width=1, color="#eeeeee"),
            self.col_editor
        ])