# modules/login/view.py
import flet as ft

class LoginView(ft.Container):
    def __init__(self, controlador):
        super().__init__(
            expand=True,
            alignment=ft.Alignment(0, 0)
        )
        self.controlador = controlador

        # --- SOLUCIÓN: Usamos ft.Icons para que el motor gráfico no falle ---
        self.txt_usuario = ft.TextField(
            label="Usuario", 
            width=400, 
            prefix_icon=ft.Icons.PERSON
        )
        self.txt_password = ft.TextField(
            label="Contraseña", 
            width=400, 
            prefix_icon=ft.Icons.LOCK, 
            password=True
        )
        self.btn_ingresar = ft.ElevatedButton(
            "Iniciar Sesión", 
            width=400, 
            on_click=self.controlador.validar_login
        )
        
        # --- SOLUCIÓN: Usamos ft.Colors ---
        self.lbl_error = ft.Text("", color=ft.Colors.ERROR)

        self.content = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        # --- SOLUCIÓN: ft.Icons y ft.Colors juntos ---
                        ft.Icon(ft.Icons.LOCK_PERSON, size=60, color=ft.Colors.PRIMARY),
                        ft.Text("Bienvenido a FTB", size=30, weight=ft.FontWeight.BOLD),
                        self.txt_usuario,
                        self.txt_password,
                        self.lbl_error,
                        self.btn_ingresar
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                ),
                padding=20
            ),
            elevation=10
        )