import flet as ft
import winreg
import math
import os
from assets.CBGenerator import CBGenerator


class GUI:

    def __init__(self):
        self.picker = ft.FilePicker(on_result=lambda f: self.change_dir(f.path))    # FilePicker instance
        self.path = get_desktop_path()
        self.OWN = False
        self.page = None


    def main(self, page: ft.Page):
        self.page = page
        self.page.title = "CPGenerator"
        self.page.vertical_alignment = "center"
        self.page.horizontal_alignment = "center"
        self.page.window_resizable = False
        self.page.window_maximizable = False
        self.page.window_width = 600
        self.page.window_height = 800
        self.page.padding=0

        self.page.overlay.append(self.picker)
        


        # HEADER CONTAINER
        self.header = ft.Container(
            content = ft.Text("Coloring Pages Generator",
                              size=35,
                              color="blue",
                              weight="bold",
                              style=ft.TextStyle(shadow=ft.BoxShadow(spread_radius=5, blur_radius=4, color="black"))),
            border_radius=30,
            width=self.page.window_width*0.8,
            height=self.page.window_height*0.12,
            bgcolor=ft.colors.BLUE_GREY_800,
            alignment=ft.alignment.center,
            margin=20,
            border=ft.border.all(2, "blue"),
            shadow=ft.BoxShadow(spread_radius=6, blur_radius=10, color="black")
        )

        # CATEGORY/WORDS INPUT CONTAINER
        self.category_input = ft.Container(
            content = ft.TextField(hint_text="e.g. spring",
                                   label="Category",
                                   input_filter=ft.InputFilter(allow=True, regex_string=r"[a-zA-Z]", replacement_string=""),
                                   width=self.page.window_width*0.56,
                                   height=self.page.window_height*0.07,
                                   text_vertical_align=0.5,
                                   hint_style=ft.TextStyle(color="blue"),
                                   border_color="blue",
                                   text_align="center",
                                   color="blue",
                                   border_radius=21,
                                   label_style=ft.TextStyle(color="blue", weight="bold")),
            border_radius=30,
            width=self.page.window_width*0.8,
            height=self.page.window_height*0.1,
            bgcolor=ft.colors.BLUE_GREY_900,
            alignment=ft.alignment.center,
            margin=20,
            border=ft.border.all(2, "blue"),
            shadow=ft.BoxShadow(spread_radius=4, blur_radius=10, color="black")
        )

        # AMOUNT INPUT CONTAINER
        self.amount_input = ft.Container(
            content = ft.TextField(hint_text="eg. 20",
                                   label="Amount",
                                   hint_style=ft.TextStyle(color="blue"),
                                   input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""),
                                   width=self.page.window_width*0.56,
                                   height=self.page.window_height*0.07,
                                   text_vertical_align=0.5,
                                   text_align="center",
                                   border_color="blue",
                                   color="blue",
                                   border_radius=21,
                                   label_style=ft.TextStyle(color="blue", weight="bold")),
            border_radius=30,
            width=self.page.window_width*0.8,
            height=self.page.window_height*0.1,
            bgcolor=ft.colors.BLUE_GREY_900,
            alignment=ft.alignment.center,
            margin=20,
            border=ft.border.all(2, "blue"),
            shadow=ft.BoxShadow(spread_radius=4, blur_radius=10, color="black"))
        


        # FILE PICKER CONTAINER
        file_path_selector = ft.Container(
            content = ft.IconButton(icon="folder", icon_size=50, on_click=lambda e: self.picker.get_directory_path()),
            border_radius=30,
            width=self.page.window_width*0.8,
            height=self.page.window_height*0.1,
            bgcolor=ft.colors.BLUE_GREY_900,
            alignment=ft.alignment.center,
            margin=20,
            border=ft.border.all(2, "blue"),
            shadow=ft.BoxShadow(spread_radius=4, blur_radius=10, color="black"))


        # BUTTONS CONTAINER
        self.buttons = ft.Container(
            content = ft.Row(
                [
                    ft.IconButton(icon=ft.icons.RESTART_ALT_ROUNDED, icon_size=50, on_click=self.reset),
                    ft.IconButton(icon=ft.icons.PLAY_ARROW_ROUNDED, icon_size=50, on_click=self.start),
                    ft.IconButton(icon=ft.icons.LIST_ALT_ROUNDED, icon_size=50, on_click=self.own_words),

                ], alignment=ft.MainAxisAlignment.CENTER, spacing=50
            ),
            border_radius=30,
            width=self.page.window_width*0.8,
            height=self.page.window_height*0.1,
            bgcolor=ft.colors.BLUE_GREY_900,
            alignment=ft.alignment.center,
            margin=20,
            border=ft.border.all(2, "blue"),
            shadow=ft.BoxShadow(spread_radius=4, blur_radius=10, color="black"))
        

        # MAIN CONTAINER
        container = ft.Container(
                content=ft.Container(
                         content=ft.Column(controls=[self.header, self.category_input, self.amount_input, file_path_selector, self.buttons]),
                         bgcolor=ft.colors.BLUE_GREY_200,
                         opacity=0.9,
                         alignment=ft.alignment.center,
                         margin=30,
                         border_radius=30,
                         width=self.page.width * 0.95,
                         height=700,
                         border=ft.border.all(2, "blue"),
                         shadow=ft.BoxShadow(spread_radius=5, blur_radius=4, color="black")),
                image_src="assets/data/bg.jpg",
                image_fit=ft.ImageFit.COVER,
                expand=True,
                padding=0,
                margin=0,
                alignment=ft.alignment.center)

        self.page.add(container)


    def reset(self, e):
        self.amount_input.shadow.color = "black"
        self.category_input.shadow.color = "black"

        try:
            self.amount_input.content.value = ""
        except Exception:
            pass
        try:
            self.category_method()
        except Exception:
            pass
        self.page.update()


    def start(self, e):
        ERROR_GATE = False
        try:
            AM = round(int(self.amount_input.content.value), -1)
            if AM < 10:
                raise Exception
            self.amount_input.shadow.color = "black"
        except Exception:       # AMOUNT ERROR
            if not self.OWN:    # We don't specify the amount when we use our own words
                ERROR_GATE = True
                self.amount_input.shadow.color = "#781414"

        try:
            CAT = self.category_input.content.value
            if CAT.strip() == "":
                raise Exception
            self.category_input.shadow.color = "black"
        except Exception:       # CATEGORY ERROR
            ERROR_GATE = True
            self.category_input.shadow.color = "#781414"
        self.page.update()
        
        ### GENERATE COLORING PAGES
        if not ERROR_GATE:
            if os.path.exists(self.path):
                generator = CBGenerator(self.path)
                if self.OWN:
                    #print(self.path, AM, split_words(CAT))
                    generator.run(amount=AM, words=split_words(CAT))
                else:
                    #print(self.path, AM, CAT)
                    generator.run(amount=AM, category=CAT)


    def own_words(self, e):
        try:
            if not self.OWN:
                self.words_method()
            else:
                self.category_method()
        except Exception as e:
            print("ERROR", e)
            pass
        self.page.update()


    def change_dir(self, path):
        if path:
            self.path = path
        else:
            self.path = get_desktop_path()
        self.path = self.path.replace("\\", "/")
        if not self.path.endswith("/"):
            self.path += "/"


    def category_method(self):
        self.OWN = False
        self.category_input.content.label = "Category"
        self.category_input.content.value = ""
        self.category_input.content.prefix_text = None
        self.category_input.content.suffix_text = None
        self.category_input.content.input_filter=ft.InputFilter(allow=True, regex_string=r"[a-zA-Z]", replacement_string="")
        self.category_input.content.hint_text = "e.g. spring"


    def words_method(self):
        self.OWN = True
        self.category_input.content.label = "Words"
        self.category_input.content.value = ""
        self.category_input.content.prefix_text = "[  "
        self.category_input.content.suffix_text = "  ]"
        self.category_input.content.input_filter=ft.InputFilter(allow=True, regex_string=r"[a-zA-Z, ]", replacement_string="")
        self.category_input.content.hint_text = "e.g. tree, banana, sun"


KEYPATH = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"


def get_desktop_path():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEYPATH, 0, winreg.KEY_READ)
    try:
        value, _ = winreg.QueryValueEx(key, "Desktop")
        return value
    except Exception as e:
        print(f"error: {e}")
    finally:
        winreg.CloseKey(key)
    return None


def split_words(words: str) -> list[str]:
    if "," not in words:
        t = list(set(words.split(" ")))
        if "" in t:
            t.remove("")
        return t
    else:
        return words.replace(" ", "").split(",")