from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.recycleview import MDRecycleView as RecycleView
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.button import MDIconButton
from kivymd.uix.imagelist.imagelist import MDSmartTile
from kivymd.uix.list.list import OneLineListItem, MDList
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.properties import ObjectProperty, ListProperty
from kivymd.uix.button import MDRaisedButton
import itertools
from icecream import ic
from pathlib import Path


from ..main import MainScreenLogic, FilmTileLogic
from trustmod.vars.env_001 import IDOLSDB_PATH as IDP, IMAGE_DIRECTORY as IDD, MEDIA_DIRECTORIES as MDD, SIMLINK_DIRECTORY as SDD, IDOLS2DB_PATH as IDB2






class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class MyButton(MDRaisedButton):
    label_obj = ObjectProperty(None)
    text_field = ObjectProperty(None)
    def on_release(self, *args):
        self.label_obj.text = self.text_field.text

class MultiIdolsIconButton(MDIconButton):
    pass


class MyBar(MDTopAppBar):
    def __init__(self, **kwargs):
        MDApp.get_running_app().msl.mybar = self
        super().__init__(**kwargs)

class MyMDList(MDList):
    mydrawer = ObjectProperty(None)
    def add_file (self, file_name):
        self.mydrawer.nav_drawer.set_state("close")
        self.msl.intial_data2 (file_path=file_name)
        print (f"add_file: {file_name}")

    def __init__(self, **kwargs):
        self.msl = MDApp.get_running_app().msl
        self.msl.mdlist = self
        super().__init__(**kwargs)

        files = Path("./stuff").glob("*.txt")
        for file in files:

            self.add_widget(OneLineListItem(
                text=str(file),
                on_release=lambda x: self.add_file(file)
                

                ) 
                
                            )
            print (f"fileeeeeeeeeeeeee: {file}")

class MyTile (MDSmartTile):
    tile_logic = ObjectProperty(None)
    film_name = StringProperty('')
    disabled_multi_idol = BooleanProperty(True)
    disabled_series = BooleanProperty(True)
    second_header = StringProperty('') #title is composed of film_name and this second_header

    def on_tile_logic(self, *args):
        self.second_header = self.tile_logic.category_name
        self.disabled_series = self.tile_logic.series_key < 1
        self.disabled_multi_idol = not self.tile_logic.categories

    def change_idol(self, *args):
        next_cat = self.tile_logic.next_category()
        if next_cat:
            self.second_header = next_cat

    def on_film_name(self, *args):
        self.source = f'{IDD}/{self.film_name}.jpg'
        
    def on_release(self, *args):
        MDApp.get_running_app().msl.mybar.title = self.tile_logic.film_desc





class MyBoxLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        MDApp.get_running_app().msl.container = self
        

class MainScreenApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.msl = MainScreenLogic()

    def build(self):
        print (f"MainScreenApp: {type(self.msl)}")
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.msl.intial_data2()


class MyRec(RecycleView):
    def __init__(self, **kwargs):
        super(MyRec, self).__init__(**kwargs)
        MDApp.get_running_app().msl.collector = self
