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
from kivy.properties import ObjectProperty

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
    texti = StringProperty('')
    idol_name = StringProperty('')
    shared_key = NumericProperty(0)
    description = StringProperty('')
    menu_items = ObjectProperty()
    series_link = StringProperty('')
    series_name = StringProperty('')
    def __init__(self, **kwargs):
        super(MyTile, self).__init__(**kwargs)
        # print (f"Source: {self.source} {self.idol_name} {self.act_option} ")
        # for key, value in kwargs.items():
        #     print(f"The key is {key} and the value is {value}")
    # def on_kv_post(self, base_widget):
    #     super(MyTile, self).on_kv_post(base_widget)
    #     print(f'MyLabel created with text: {base_widget.source}')
    def on_idol_name(self, instance, value):
        print(f'MyLabel text changed to: {value}')    
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
        self.theme_cls.primary_palette = "Orange"
        self.msl.intial_data()
        #self.msl.collector.data = [{'text': str(x)} for x in range(50)]    


class MyRec(RecycleView):
    def __init__(self, **kwargs):
        super(MyRec, self).__init__(**kwargs)
        MDApp.get_running_app().msl.collector = self
