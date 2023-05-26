from kivymd.app import MDApp
from kivy.lang import Builder
#from kivy.uix.recycleview import RecycleView
from kivymd.app import MDApp
import threading
from kivy.lang import Builder
from kivymd.uix.recycleview import MDRecycleView as RecycleView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from pathlib import Path
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivymd.uix.imagelist.imagelist import MDSmartTile
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from bs4 import BeautifulSoup
import subprocess
import multiprocessing
import os
from kivymd.uix.button import MDIconButton
from kivymd.uix.navigationdrawer.navigationdrawer import MDNavigationDrawer
import sqlite3


from tt import parseTitle

link_path = "F:/data/link.windows"
images_path = "F:/trusti"

Window.maximize()
class MyScreen (MDBoxLayout):
    pass

class MyDrawer (MDNavigationDrawer):
    pass

class MenuIconButton(MDIconButton):
    menu_items = ObjectProperty()
    myTile = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #"on_release": lambda x="x": self.myTile.mm(x)

        #menu = MDDropdownMenu(items=menu_items, width_mult=4)
        self.menu = MDDropdownMenu(
            items=self.menu_items,
            width_mult=12
        )

    def open_menu(self):
        self.menu.caller = self
        self.menu.open()



class myTile (MDSmartTile):
    texti = StringProperty('')
    menu_items = ObjectProperty()

    def on_release(self, *args):
        print (self.texti)
        return super().on_release(*args)


    def tt(self):
        return self.texti

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        menu_itemsw = [
                {"viewclass": "OneLineListItem", "text": "k"},
                {"viewclass": "OneLineListItem", "text": self.texti},
                {"viewclass": "OneLineListItem", "text": self.tt(), "on_release": lambda x="x": self.mm(x)},
            ]

        


        mennu = MenuIconButton(
            #icon='dots-vertical',
            menu_items=menu_itemsw,
            pos_hint={'right': 1, 'top': 1}
        )
        mennu.myTile = self
        #mennu.menu_items = menu_itemsw
        self.add_widget(mennu)
    def mm(self, txt):
        print (self.texti)
        t = ["C:/Users/bing/Desktop/mpv/mpv.exe", "--fs", "--fs-screen=0", "--loop-playlist" ]
        i = "C:/Users/bing/Desktop/mpv/mpv.exe --fs --fs-screen=0 --loop-playlist" 
        files = Path(link_path).glob ( self.texti.lower() + "*")
        #print (self.texti)
        for s in files:
            t.append(s)
            i = i + " " + str(s)
        #os.system(i)
        #subprocess.run(t)



    def separate(self):
        t = ["C:/Users/bing/Desktop/mpv/mpv.exe", "--fs", "--fs-screen=0", "--loop-playlist" ]
        i = "C:/Users/bing/Desktop/mpv/mpv.exe --fs --fs-screen=0 --loop-playlist" 
        files = Path(link_path).glob ( self.texti.lower() + "*")
        print (self.texti)
        for s in files:
            t.append(s)
            i = i + " " + str(s)
        #subprocess.run(t)
        print (i, "oanother")


class MyRec (RecycleView):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        MDApp.get_running_app().rv = self
        
def playme (txt1):
    # print (txt1)
    t = ["C:/Users/bing/Desktop/mpv/mpv.exe", "--fs", "--fs-screen=0", "--loop-playlist" ]
    i = "C:/Users/bing/Desktop/mpv/mpv.exe --fs --fs-screen=0 --loop-playlist" 
    files = Path(link_path).glob ( txt1.lower() + "*")
    #print (files)
    
    for s in files:
        print (s)
        t.append(s)
        i = i + " " + str(s)
        
    subprocess.run(t)
    
class Wrk1App(MDApp):
    rv = ObjectProperty()
    txt1 = StringProperty()
    ii = ObjectProperty()
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        menu_items = [
        {
            "viewclass": "OneLineListItem",
            "text": i.name,
            "height": dp(56),
            "on_release": lambda x=f"F:/Runner1/Series/{i.name}": self.menu_callback(x),
            } for i in Path("F:/Runner1/Series").iterdir()
        ]
        menu_items2 = [
        {
            "viewclass": "OneLineListItem",
            "text": i.name,
            "height": dp(56),
            "on_release": lambda x=f"F:/Runner1/Idols/{i.name}": self.menu_callback(x),
            } for i in Path("F:/Runner1/Idols").iterdir()
        ]


        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=12,
        )
        self.menu2 = MDDropdownMenu(
            items=menu_items2,
            width_mult=12,
        )
        self.menu3 = MDDropdownMenu(
            width_mult=12,
        )

        return Builder.load_file ('EWrk1.kv')

    def callback (self, topmenu):
        self.menu.caller = topmenu
        self.menu.open()
    def callbackx (self, topmenu):
        self.menu2.caller = topmenu
        self.menu2.open()
    def callbacky (self, topmenu):
        self.txt1 = topmenu.texti
        self.ii = topmenu
        self.menu3.caller = topmenu
        self.menu3.open()

    def mm(self, txt1):
        thread = threading.Thread(target=playme, args=(txt1,))
        thread.start()
        
    def menu_callback(self, txt):
        #U = playSeries(txt)
        #self.rv.ids.toolbar = txt
        newpath = Path(txt)
        self.rv.ids.rgg.clear_widgets()
        self.rv.data = [{'source': str(x), 'texti': x.stem} for x in newpath.iterdir()]
        self.root.ids.toolbar.title = txt
        
        #print(txt)

    def cell_menu(self, objx):

        # Connect to the database
        conn = sqlite3.connect('tfilms.db')
        mtil = objx.parent.parent
        film = mtil.texti
        
        # Create a cursor object
        cur = conn.cursor()

        # Execute the query to retrieve the description string for film "XXX"
        cur.execute("SELECT description FROM films WHERE name=?", (film,))

        # Fetch the result
        result = cur.fetchone()

        # Close the cursor and database connection
        cur.close()
        conn.close()

        # Print the description string
        print(result[0])

        menu_items3 = [
        {
            "viewclass": "TwoLineListItem",
            "text": film,
            "secondary_text": result[0],
            "height": dp(56),
            "on_release": lambda x=film: self.mm(x),
            } 
        ]


        self.menu3.caller = objx
        self.menu3.items = menu_items3
        self.menu3.open()



if __name__ == '__main__':
    Wrk1App().run()
