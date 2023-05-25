from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.uix.recycleview import MDRecycleView as RecycleView
from kivymd.uix.imagelist.imagelist import MDSmartTile
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
import sqlite3
import subprocess
from pathlib import Path
import threading

from trustmod.vars.env_001 import IDOLSDB_PATH as IDP, IMAGE_DIRECTORY as IDD, MEDIA_DIRECTORIES as MDD, SIMLINK_DIRECTORY as SDD


KV = '''
MDScreen:

    MDNavigationLayout:

        MDScreenManager:

            MDScreen:
                MDBoxLayout:
                    orientation: 'vertical'
                    MDTopAppBar:
                        title: "Navigation Drawer"
                        elevation: 4
                        pos_hint: {"top": 1}
                        md_bg_color: "#e7e4c0"
                        specific_text_color: "#4a4939"
                        left_action_items:
                            [['menu', lambda x: nav_drawer.set_state("open")]]
                    MyRec:
                        id: rec
                        viewclass: 'MyTile'
                        MDRecycleGridLayout:
                            id: rgg
                            padding: ('0dp', '10dp', '0dp', '0dp')
                            default_size: None, dp(340)
                            default_size_hint: 1, None
                            spacing: dp(4)
                            cols: 5
                            size_hint_y: None
                            height: self.minimum_height
                            orientation: 'lr-tb'


        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)

            ContentNavigationDrawer:
'''
def playme (txt1):
    # print (txt1)
    t = ["C:/Users/bing/Desktop/mpv/mpv.exe", "--fs", "--fs-screen=0", "--loop-playlist" ]
    i = "C:/Users/bing/Desktop/mpv/mpv.exe --fs --fs-screen=0 --loop-playlist" 
    files = Path(SDD).glob ( txt1.lower() + "*")
    #print (files)
    
    for ss2 in files:
        print (ss2)
        t.append(ss2)
        i = i + " " + str(ss2)
        
    subprocess.run(t)

class MyTile (MDSmartTile):
    texti = StringProperty('')
    menu_items = ObjectProperty()
    def on_release(self, *args):
        thread = threading.Thread(target=playme, args=(self.texti,))
        thread.start()
        print (self.texti)
        return super().on_release(*args)


def films_from_idols(idols):
    conn = sqlite3.connect(IDP)
    c = conn.cursor()
    q1 = f"select distinct fi.film_name from film_idols fi join idols i on fi.idol_link = i.link   where i.shared_key = {idols};"
    c.execute(q1)
    films = c.fetchall()
    print (IDP)
    films2 = [{'source': f'{IDD}/{i[0]}.jpg', 'texti' : i[0] } for i in films]
    return films2




class MyRec(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.data = films_from_idols(83, 43) # [{'text': str(x)} for x in range(50)]
        self.data = films_from_idols(43) # [{'text': str(x)} for x in range(50)]

class ContentNavigationDrawer(MDBoxLayout):
    pass


class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)


Example().run()