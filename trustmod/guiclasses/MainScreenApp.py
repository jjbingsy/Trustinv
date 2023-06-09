from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.recycleview import MDRecycleView as RecycleView
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.button import MDIconButton
from kivymd.uix.imagelist.imagelist import MDSmartTile
from kivymd.uix.list.list import OneLineListItem
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.properties import ObjectProperty, ListProperty
import itertools
from icecream import ic



from ..main import MainScreenLogic, FilmTileLogic
from trustmod.vars.env_001 import IDOLSDB_PATH as IDP, IMAGE_DIRECTORY as IDD, MEDIA_DIRECTORIES as MDD, SIMLINK_DIRECTORY as SDD, IDOLS2DB_PATH as IDB2




class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()




class MultiIdolsIconButton(MDIconButton):
    pass


class MyBar(MDTopAppBar):
    def __init__(self, **kwargs):
        MDApp.get_running_app().msl.mybar = self
        super().__init__(**kwargs)



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
