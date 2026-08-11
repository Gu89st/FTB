# main.py
import flet as ft
from core.main_window import MainWindow

def main(page: ft.Page):
    app = MainWindow(page)
if __name__ == "__main__":
  
    ft.run(main) 