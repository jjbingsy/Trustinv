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
from trustmod.vars.env_001 import IDOLSDB_PATH as IDP, IMAGE_DIRECTORY as IDD, MEDIA_DIRECTORIES as MDD, SIMLINK_DIRECTORY as SDD, IDOLS2DB_PATH as IDB2


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

    label = StringProperty('')


    #texti = StringProperty('')
    series_shared_key = NumericProperty(0)
    description = StringProperty('')
    menu_items = ObjectProperty()
    series_link = StringProperty('')
    series_name = StringProperty('')

    def change_idol(self, *args):
        self.idol_index += 1 

    def on_idol_index(self, *args):
        if self.idol_index >= len(self.idols):
            self.idol_index = 0
        #self.label = f"{self.film_name} - {self.idols[self.idol_index][1]}"
        self.idol_name = self.idols[self.idol_index][1]
        self.shared_key = self.idols[self.idol_index][0]



    def __init__(self, **kwargs):
        super(MyTile, self).__init__(**kwargs)

    def on_film_name(self, *args):
        self.source = f'{IDD}/{self.film_name}.jpg'
        # if self.idols[0] == 0:
        #     self.label = f"{self.film_name} - {self.series_name}"
        # else:
        #     self.label = f"{self.film_name} - {MDApp.get_running_app().msl.shared_key_name[self.idols[self.idol_index]]}"
        
    def on_idols(self, *args):
        
        #print (f"on_idols: {self.label}")
        # if self.film_name != "" and self.label == '':
        #     self.label = f"{self.film_name} - {self.idols[self.idol_index][1]}"
        
        # if self.idols:
        #     self.label += f" {self.idols[0][1]} "
        if self.idols and self.idols[0]:
            self.shared_key =  self.idols[0]
        #print (f"on_idols: {self.label} {self.idols[0]}")
        if self.shared_key > 0:
            #self.label = MDApp.get_running_app().msl.shared_key_name[self.shared_key]
            self.idol_name = MDApp.get_running_app().msl.shared_key_name[self.shared_key]
        else:
            #self.label = self.series_name
            self.idol_name = self.series_name

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
        self.msl.intial_data2()
        #self.msl.collector.data = [{'text': str(x)} for x in range(50)]    


class MyRec(RecycleView):
    def __init__(self, **kwargs):
        super(MyRec, self).__init__(**kwargs)
        MDApp.get_running_app().msl.collector = self
