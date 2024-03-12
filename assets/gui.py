import flet as ft


class GUI:

    def main(page: ft.Page):
        page.title = "TEST"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.window_resizable = False
        page.window_maximizable = False
        page.window_width = 600
        page.window_height = 800
        
        stack = ft.Stack([
            ft.Container(
                image_src="assets/data/bg.jpg",
                image_fit=ft.ImageFit.COVER,
                expand=True,
                padding=0,
                margin=0
            )

        ], width=600, height=800)

        page.add(stack)

    def start(e):
        print("START", e)