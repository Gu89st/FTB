from .view import LoginView
from .model import LoginModel

class LoginController:
    def __init__(self, on_login_success):
        print("4. Conectando con la base de datos...")
        self.on_login_success = on_login_success
        self.model = LoginModel()
        self.view = LoginView(controlador=self)

    def obtener_vista(self):
        return self.view

    def validar_login(self, e):
        self.view.btn_ingresar.disabled = True
        self.view.update()

        usuario = self.view.txt_usuario.value
        password = self.view.txt_password.value

        credenciales_validas = self.model.verificar_credenciales(usuario, password)

        if credenciales_validas:
            self.view.lbl_error.value = ""
            self.on_login_success() 
        else:
            self.view.lbl_error.value = "Usuario o contraseña incorrectos"
            self.view.btn_ingresar.disabled = False
            self.view.update()