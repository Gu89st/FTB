# core/main_window.py
import flet as ft
from modules.login.Controller import LoginController

class MainWindow:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Vida Sync - FTB"
        
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

        # --- 1. BARRA SUPERIOR BLINDADA ---
        self.page.appbar = ft.AppBar(
            leading=ft.Icon("space_dashboard_rounded", color="#00b4d8"), # Color turquesa en hex
            leading_width=40,
            title=ft.Text("Vida Sync", weight=ft.FontWeight.BOLD),
            center_title=False,
            bgcolor="#f4f6f9", # Un color gris muy claro y seguro
            actions=[
                ft.Container(
                    content=ft.TextField(hint_text="Search...", width=200, height=40, text_size=14, prefix_icon="search"),
                    padding=10
                ),
                ft.IconButton("notifications_outlined"),
                ft.Row([
                    ft.CircleAvatar(content=ft.Text("ML"), bgcolor="#00b4d8", color="white", radius=15),
                    ft.Text("Mariana López", weight=ft.FontWeight.W_500),
                    ft.IconButton("keyboard_arrow_down")
                ]),
                ft.Container(width=10) 
            ]
        )

        # --- 2. MENÚ LATERAL BLINDADO ---
        self.menu_lateral = ft.NavigationRail(
            selected_index=1, 
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            destinations=[
                ft.NavigationRailDestination(icon="account_balance_wallet_outlined", selected_icon="account_balance_wallet", label="Finanzas"),
                ft.NavigationRailDestination(icon="notes_outlined", selected_icon="notes", label="Notas"),
                ft.NavigationRailDestination(icon="fitness_center_outlined", selected_icon="fitness_center", label="Gym"),
                ft.NavigationRailDestination(icon="settings_outlined", selected_icon="settings", label="Settings"),
            ],
            on_change=self.cambiar_modulo 
        )

        # --- 3. CONTENEDOR CENTRAL DINÁMICO ---
        self.contenedor_modulos = ft.Container(
            expand=True, 
            padding=20,
            content=ft.Text("Cargando módulo de Notas...", size=20, color="grey")
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
        self.page.update()

    def cambiar_modulo(self, e):
        indice_seleccionado = e.control.selected_index
        self.contenedor_modulos.content = None 

        if indice_seleccionado == 0:
            self.contenedor_modulos.content = ft.Text("Aquí irá la vista de Finanzas", size=30)
        elif indice_seleccionado == 1:
            self.contenedor_modulos.content = ft.Text("Aquí irá la vista de Notas (To-Do)", size=30)
        elif indice_seleccionado == 2:
            self.contenedor_modulos.content = ft.Text("Aquí irá la vista de Gym", size=30)
        elif indice_seleccionado == 3:
            self.contenedor_modulos.content = ft.Text("Aquí irán las Configuraciones", size=30)

        self.page.update()