# core/main_window.py
import flet as ft
from modules.login.Controller import LoginController
from modules.tasks.controller import TasksController

class MainWindow:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "FTB"

        self.page.window.width = 1100
        self.page.window.height = 750
        self.page.theme_mode = ft.ThemeMode.LIGHT

        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START

        self.mostrar_login()

    def mostrar_login(self):
        self.page.appbar = None
        self.page.controls.clear()

        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        controlador_login = LoginController(on_login_success=self.mostrar_dashboard)
        self.page.add(controlador_login.obtener_vista())
        self.page.update()

    def mostrar_dashboard(self):
        self.page.controls.clear()

        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START

        # --- 1. BARRA SUPERIOR ---
        self.page.appbar = ft.AppBar(
            leading=ft.Icon(ft.Icons.SPACE_DASHBOARD_ROUNDED, color="#00b4d8"),
            leading_width=40,
            title=ft.Text("FTB", weight=ft.FontWeight.BOLD),
            center_title=False,
            bgcolor="#f4f6f9",
            actions=[
                ft.Container(
                    content=ft.TextField(hint_text="Search...", width=200, height=40, text_size=14, prefix_icon=ft.Icons.SEARCH),
                    padding=10
                ),
                ft.IconButton(icon=ft.Icons.NOTIFICATIONS_OUTLINED),
                ft.Container(width=10)
            ]
        )

        # --- 2. MENÚ LATERAL ---
        self.menu_lateral = ft.NavigationRail(
            selected_index=1,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, selected_icon=ft.Icons.ACCOUNT_BALANCE_WALLET, label="Finanzas"),
                ft.NavigationRailDestination(icon=ft.Icons.NOTES_OUTLINED, selected_icon=ft.Icons.NOTES, label="Notas"),
                ft.NavigationRailDestination(icon=ft.Icons.FITNESS_CENTER_OUTLINED, selected_icon=ft.Icons.FITNESS_CENTER, label="Gym"),
                ft.NavigationRailDestination(icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS, label="Settings"),
            ],
            on_change=self.cambiar_modulo
        )

        # --- 3. CONTENEDOR CENTRAL DINÁMICO ---
        self.contenedor_modulos = ft.Container(
            expand=True,
            padding=20,
        )

        # --- 4. ENSAMBLAJE DE LA PANTALLA ---
        cuerpo_principal = ft.Row(
            controls=[
                self.menu_lateral,
                ft.VerticalDivider(width=1),
                self.contenedor_modulos
            ],
            expand=True
        )

        self.page.add(cuerpo_principal)

        # Carga el módulo correspondiente al índice ya seleccionado (Notas)
        # sin esperar a un clic del usuario, ya que on_change del
        # NavigationRail no se dispara por setear selected_index a mano.
        self.cargar_modulo(self.menu_lateral.selected_index)

        self.page.update()

    def cambiar_modulo(self, e):
        self.cargar_modulo(e.control.selected_index)
        self.page.update()

    def cargar_modulo(self, indice_seleccionado):
        self.contenedor_modulos.content = None

        if indice_seleccionado == 0:
            self.contenedor_modulos.content = ft.Text("Aquí irá la vista de Finanzas", size=30)
        elif indice_seleccionado == 1:
            controlador_notas = TasksController()
            self.contenedor_modulos.content = controlador_notas.obtener_vista()
            # Carga las secciones/notas ya existentes en la base de datos.
            # es_inicio=True evita que intente refrescar la pantalla antes
            # de que la vista esté montada en la página.
            controlador_notas.refrescar_ui_categorias(es_inicio=True)
        elif indice_seleccionado == 2:
            self.contenedor_modulos.content = ft.Text("Aquí irá la vista de Gym", size=30)
        elif indice_seleccionado == 3:
            self.contenedor_modulos.content = ft.Text("Aquí irán las Configuraciones", size=30)