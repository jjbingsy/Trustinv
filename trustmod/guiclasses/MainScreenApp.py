from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.widget import Widget
from kivymd.uix.label import MDLabel

from kivymd.uix.button import MDRectangleFlatButton

class MainWidget(Widget):
    pass

class MyButton(MDRectangleFlatButton):
    pass

class MyLabel(MDLabel):
    pass

class MainScreenApp(MDApp):
    pass
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

