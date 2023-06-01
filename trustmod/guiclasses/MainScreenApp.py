from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.recycleview import MDRecycleView as RecycleView
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.imagelist.imagelist import MDSmartTile
from kivymd.uix.list.list import OneLineListItem
from kivymd.uix.toolbar import MDTopAppBar
from kivy.properties import StringProperty, NumericProperty
from kivy.properties import ObjectProperty, ListProperty

from ..main import MainScreenLogic


class MyBar(MDTopAppBar):
    def __init__(self, **kwargs):
        MDApp.get_running_app().msl.mybar = self
        super().__init__(**kwargs)

class MyButton(MDRectangleFlatButton):
    texti = StringProperty('')
    act_option = StringProperty('')
    menu_items = ObjectProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MyTile (MDSmartTile):
    idols = ListProperty([])
    idol_index = NumericProperty(0)
    idol_name = StringProperty('')
    shared_key = NumericProperty(0)

    film_name = StringProperty('')

    label = StringProperty('still blank')


    #texti = StringProperty('')
    description = StringProperty('')
    menu_items = ObjectProperty()
    series_link = StringProperty('')
    series_name = StringProperty('')

    def change_idol(self, *args):
        self.idol_index += 1

    def on_idol_index(self, *args):
        if self.idol_index >= len(self.idols):
            self.idol_index = 0
        self.label = f"{self.film_name} - {self.idols[self.idol_index][1]}"
        self.idol_name = self.idols[self.idol_index][1]
        self.shared_key = self.idols[self.idol_index][0]



    def __init__(self, **kwargs):
        super(MyTile, self).__init__(**kwargs)

    def on_film_name(self, *args):
        if self.idol_index >= len(self.idols):
            self.idol_index = 0
        self.label = f"{self.film_name} - {self.idols[self.idol_index][1]}"

    def on_idols(self, *args):
        if self.idols:
            self.label = f"{self.film_name} - {self.idols[0][1]}"
            self.idol_name = self.idols[0][1]
            self.shared_key = self.idols[0][0]

    def on_release(self, *args):
        MDApp.get_running_app().msl.mybar.title = self.description
    #     MDApp.get_running_app().msl.playme2(self.texti)
    #     print (self.texti)


class MyLabel(OneLineListItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



class MyBoxLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        MDApp.get_running_app().msl.container = self
        



class MainScreenApp(MDApp):
    msl = ObjectProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.msl = MainScreenLogic()

    def build(self):
        print (f"MainScreenApp: {type(self.msl)}")
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.msl.intial_data()
        #self.msl.collector.data = [{'text': str(x)} for x in range(50)]    


class MyRec(RecycleView):
    def __init__(self, **kwargs):
        super(MyRec, self).__init__(**kwargs)
        MDApp.get_running_app().msl.collector = self
