from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.recycleview import MDRecycleView as RecycleView
from kivymd.uix.button import MDRectangleFlatButton

from kivy.properties import StringProperty
from kivy.properties import ObjectProperty


class MainWidget(Widget):
    pass

class MyButton(MDRectangleFlatButton):
    texti = StringProperty('')
    act_option = StringProperty('')
    menu_items = ObjectProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MyLabel(MDLabel):
    pass
class MyBoxLayout(MDBoxLayout):
    pass

class MainScreenApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

class MyRec(RecycleView):
    def __init__(self, **kwargs):
        #MDApp.get_running_app().myOp.myRC(self)
        super().__init__(**kwargs)
        #self.data = [{'text': str(x)} for x in range(50)]
