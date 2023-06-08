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
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.properties import ObjectProperty, ListProperty
import itertools
from icecream import ic



from ..main import MainScreenLogic, FilmTileLogic
from trustmod.vars.env_001 import IDOLSDB_PATH as IDP, IMAGE_DIRECTORY as IDD, MEDIA_DIRECTORIES as MDD, SIMLINK_DIRECTORY as SDD, IDOLS2DB_PATH as IDB2


class MultiIdolsIconButton(MDIconButton):
    pass


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
    tile_logic = ObjectProperty(None)
    film_name = StringProperty('')
    disabled_multi_idol = BooleanProperty(True)
    disabled_series = BooleanProperty(True)
    idols = ObjectProperty(None) # iterator or None
    second_header = StringProperty('') #title is composed of film_name and this second_header

    def load_series(self, *args):
        pass
        # ic (self.series_shared_key)
        # ic (MDApp.get_running_app().msl.series_name[self.series_shared_key])

    def on_tile_logic(self, *args):
        if self.tile_logic.series_shared_key > 0:
            self.disabled_series = False
        else:
            self.disabled_series = True
        if self.tile_logic.idols:
            self.disabled_multi_idol = False
        else:
            self.disabled_multi_idol = True
        if self.tile_logic.idol_shared_key > 0:
            self.second_header = MDApp.get_running_app().msl.shared_key_name[self.tile_logic.idol_shared_key]
        elif self.tile_logic.series_shared_key > 0:
            self.second_header = MDApp.get_running_app().msl.series_name[self.tile_logic.series_shared_key]
        else:
            self.second_header = ''

    def change_idol(self, *args):
        new_shared_key = next(self.tile_logic.idols)
        if new_shared_key > 0:
            self.idol_shared_key = new_shared_key
            self.second_header = MDApp.get_running_app().msl.shared_key_name[new_shared_key]
        elif self.tile_logic.series_shared_key > 0:
            self.second_header = MDApp.get_running_app().msl.series_name[self.tile_logic.series_shared_key]
        
        # if self.idols:
        #     self.idol_shared_key = next(self.idols)
        # else:
        #     self.idol_shared_key = 0
        # ic(MDApp.get_running_app().msl.shared_key_name[self.idol_shared_key])

    def on_idol_shared_key(self, *args):
        pass
        # self.second_header = ''
        # if self.series_dominant and self.series_shared_key > 0 and self.series_shared_key in MDApp.get_running_app().msl.series_name:
        #     self.second_header = MDApp.get_running_app().msl.series_name[self.series_shared_key]
        # elif self.idol_shared_key > 0 and self.idol_shared_key in MDApp.get_running_app().msl.shared_key_name:
        #     self.second_header = MDApp.get_running_app().msl.shared_key_name[self.idol_shared_key]
        # elif self.idol_shared_key == 0 and self.series_shared_key > 0 and self.series_shared_key in MDApp.get_running_app().msl.series_name:
        #     self.second_header = MDApp.get_running_app().msl.series_name[self.series_shared_key]
        # else:
        #     self.second_header = ''


    def on_idol_count(self, *args):
        pass
#         if self.idol_count > 1 and self.fixed:
#             print (self.idol_count)
#             self.add_widget ( MDIconButton( icon = "dots-vertical", on_release=self.change_idol  ))
# #        self.fixed = False




    def on_idol_index(self, *args):
        pass
        # if self.idol_index >= len(self.idols):
        #     self.idol_index = 0
        # #self.label = f"{self.film_name} - {self.idols[self.idol_index][1]}"
        # self.idol_name = self.idols[self.idol_index][1]
        # self.shared_key = self.idols[self.idol_index][0]



    def __init__(self, **kwargs):
        super(MyTile, self).__init__(**kwargs)

    def on_film_name(self, *args):
        self.source = f'{IDD}/{self.film_name}.jpg'
        # if self.idols[0] == 0:
        #     self.label = f"{self.film_name} - {self.series_name}"
        # else:
        #     self.label = f"{self.film_name} - {MDApp.get_running_app().msl.shared_key_name[self.idols[self.idol_index]]}"
        
    def on_idols(self, *args):
        pass
        # ic (len(self.idols))
        # if (len(self.idols) > 1) and self.fixed:
        #     ic (len(self.idols))
        #     self.add_widget ( MDIconButton( icon = "dots-vertical", on_release=self.change_idol  ))
        # self.fixed = False
        
        #print (f"on_idols: {self.label}")
        # if self.film_name != "" and self.label == '':
        #     self.label = f"{self.film_name} - {self.idols[self.idol_index][1]}"
        
        # if self.idols:
        #     self.label += f" {self.idols[0][1]} "
                                                                                # if self.idols and self.idols[0]:
                                                                                #     self.shared_key =  self.idols[0]
        #print (f"on_idols: {self.label} {self.idols[0]}")
                                                                                # if self.shared_key > 0:
                                                                                #     #self.label = MDApp.get_running_app().msl.shared_key_name[self.shared_key]
                                                                                #     self.idol_name = MDApp.get_running_app().msl.shared_key_name[self.shared_key]
                                                                                # else:
                                                                                #     #self.label = self.series_name
                                                                                #     self.idol_name = self.series_name

    def on_release(self, *args):
        if self.idol_shared_key > 0 and self.film_name in MDApp.get_running_app().msl.film_desc:
            MDApp.get_running_app().msl.mybar.title = MDApp.get_running_app().msl.film_desc[self.film_name]
        #maybe add description of series


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
        self.msl.intial_data2()
        #self.msl.collector.data = [{'text': str(x)} for x in range(50)]    


class MyRec(RecycleView):
    def __init__(self, **kwargs):
        super(MyRec, self).__init__(**kwargs)
        MDApp.get_running_app().msl.collector = self
