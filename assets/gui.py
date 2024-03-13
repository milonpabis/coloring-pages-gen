import flet as ft


class GUI:

    def main(page: ft.Page):
        page.title = "TEST"
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"
        page.window_resizable = False
        page.window_maximizable = False
        page.window_width = 600
        page.window_height = 800
        page.padding=0

        header = ft.Container(
            content = ft.Text("Coloring Pages Generator",
                              size=35,
                              color="blue",
                              weight="bold",
                              style=ft.TextStyle(shadow=ft.BoxShadow(spread_radius=5, blur_radius=4, color="black"))),
            border_radius=30,
            width=page.window_width*0.8,
            height=page.window_height*0.12,
            bgcolor=ft.colors.BLUE_GREY_800,
            alignment=ft.alignment.center,
            margin=20,
            border=ft.border.all(2, "blue"),
            shadow=ft.BoxShadow(spread_radius=6, blur_radius=10, color="black")
        )

        category_input = ft.Container(
            content = ft.TextField(hint_text="e.g. spring",
                                   label="Category",
                                   width=page.window_width*0.56,
                                   height=page.window_height*0.07,
                                   hint_style=ft.TextStyle(color="blue"),
                                   border_color="blue",
                                   color="blue",
                                   border_radius=21,
                                   label_style=ft.TextStyle(color="blue", weight="bold")),
            border_radius=30,
            width=page.window_width*0.8,
            height=page.window_height*0.1,
            bgcolor=ft.colors.BLUE_GREY_900,
            alignment=ft.alignment.center,
            margin=20,
            border=ft.border.all(2, "blue"),
            shadow=ft.BoxShadow(spread_radius=4, blur_radius=10, color="black")
        )

        amount_input = ft.Container(
            content = ft.TextField(hint_text="20",
                                   label="Amount",
                                   hint_style=ft.TextStyle(color="blue"),
                                   width=page.window_width*0.56,
                                   height=page.window_height*0.07,
                                   border_color="blue",
                                   color="blue",
                                   border_radius=21,
                                   label_style=ft.TextStyle(color="blue", weight="bold")),
            border_radius=30,
            width=page.window_width*0.8,
            height=page.window_height*0.1,
            bgcolor=ft.colors.BLUE_GREY_900,
            alignment=ft.alignment.center,
            margin=20,
            border=ft.border.all(2, "blue"),
            shadow=ft.BoxShadow(spread_radius=4, blur_radius=10, color="black"))
        



        file_path_selector = ft.Container(
            content = ft.IconButton(icon="folder", icon_size=50),
            border_radius=30,
            width=page.window_width*0.8,
            height=page.window_height*0.1,
            bgcolor=ft.colors.BLUE_GREY_900,
            alignment=ft.alignment.center,
            margin=20,
            border=ft.border.all(2, "blue"),
            shadow=ft.BoxShadow(spread_radius=4, blur_radius=10, color="black"))



        buttons = ft.Container(
            content = ft.Row(
                [
                    ft.IconButton(icon=ft.icons.RESTART_ALT_ROUNDED, icon_size=50),
                    ft.IconButton(icon=ft.icons.PLAY_ARROW_ROUNDED, icon_size=50),
                    ft.IconButton(icon=ft.icons.LIST_ALT_ROUNDED, icon_size=50),

                ], alignment=ft.MainAxisAlignment.CENTER, spacing=50
            ),
            border_radius=30,
            width=page.window_width*0.8,
            height=page.window_height*0.1,
            bgcolor=ft.colors.BLUE_GREY_900,
            alignment=ft.alignment.center,
            margin=20,
            border=ft.border.all(2, "blue"),
            shadow=ft.BoxShadow(spread_radius=4, blur_radius=10, color="black"))
        
        container = ft.Container(
                content=ft.Container(
                         content=ft.Column(controls=[header, category_input, amount_input, file_path_selector, buttons]),
                         bgcolor=ft.colors.BLUE_GREY_200,
                         opacity=0.9,
                         alignment=ft.alignment.center,
                         margin=30,
                         border_radius=30,
                         width=page.width * 0.95,
                         height=700,
                         border=ft.border.all(2, "blue"),
                         shadow=ft.BoxShadow(spread_radius=5, blur_radius=4, color="black")),
                image_src="assets/data/bg.jpg",
                image_fit=ft.ImageFit.COVER,
                expand=True,
                padding=0,
                margin=0,
                alignment=ft.alignment.center)

        page.add(container)

    def start(e):
        print("START", e)