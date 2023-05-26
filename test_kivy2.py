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
                            [['menu', lambda x: nav_drawer.set_state("open")], ['menu', lambda x: app.myOp.rc.ii()]]
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

class MyOp():
    def __init__(self, myapp):
        self.app = myapp

    def myRC(self, myRC):
        self.rc = myRC

    def click1(self, new_idol):
        self.rc.jj(new_idol)
        print (type (self.rc))
        print ("click1")
        for i in self.rc.ids:
            print (type(i))





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
    act_option = StringProperty('')
    menu_items = ObjectProperty()
    def on_release(self, *args):
        if self.act_option == 'idol':
            MDApp.get_running_app().myOp.rc.jj(self.texti)
        elif self.act_option == 'play':
            thread = threading.Thread(target=playme, args=(self.texti,))
            thread.start()
            print (self.texti)
            return super().on_release(*args)
        


def films_from_idols(idols):
    conn = sqlite3.connect(IDP)
    c = conn.cursor()
    q1 = f"select DISTINCT i.shared_key from idols i join fiLm_idols f on i.link = f.idol_link WHERE film_name = '{idols}';"
    c.execute(q1)
    results = c.fetchone()
    q2 = f"select distinct fi.film_name from film_idols fi join idols i on fi.idol_link = i.link   where i.shared_key = {results[0]};"
    c.execute(q2)
    films = c.fetchall()
    print (IDP)
    films2 = [{'source': f'{IDD}/{i[0]}.jpg', 'texti' : i[0], 'act_option':'play' } for i in films]
    return films2

def getSharedKey():
    q1 = '''
    select i.shared_key, count(distinct fi.film_name) c from film_idols fi join idols i on fi.idol_link = i.link group by i.shared_key having shared_key not null and c > 1 order by c desc;
    '''
    q2 = '''
    select fi.film_name, count(distinct i.shared_key) c from film_idols fi join idols i on fi.idol_link = i.link group by fi.film_name having c = 1 and i.shared_key = ?;
    '''

    conn = sqlite3.connect(IDP)
    kk = []
    cursor = conn.cursor()
    cursor.execute(q1)
    results = cursor.fetchall()
    for i in results:
        shared_key = i[0]
        cursor.execute(q2, (shared_key,))
        results2 = cursor.fetchone()
        if results2:
            #print (results2[0], shared_key)
            kk.append ( results2[0] )
    conn.close()
    films2 = [{'source': f'{IDD}/{i}.jpg', 'texti' : i, 'act_option': 'idol' } for i in kk]
    return films2




class MyRec(RecycleView):
    def __init__(self, **kwargs):
        MDApp.get_running_app().myOp.myRC(self)
        super().__init__(**kwargs)
        #self.data = films_from_idols(83, 43) # [{'text': str(x)} for x in range(50)]
        self.data = getSharedKey() # [{'text': str(x)} for x in range(50)]


    def jj(self, new_idol):
        ss = None
        for i in self.children:
            print (type(i))
            ss = i
            if i:
                self.data = {'source': f'{IDD}/ADN-195.jpg', 'text' : "ADN-195" }
                i.clear_widgets()
                self.data = films_from_idols(new_idol) # [{'text': str(x)} for x in range(50)]
            # self.ids.rgg.clear_widgets()

    def ii(self):
        ss = None
        for i in self.children:
            print (type(i))
            ss = i
            if i:
                self.data = {'source': f'{IDD}/ADN-195.jpg', 'text' : "ADN-195" }
                i.clear_widgets()
                self.data = getSharedKey()
            # self.ids.rgg.clear_widgets()




class ContentNavigationDrawer(MDBoxLayout):
    pass


class Example(MDApp):
    myOp = ObjectProperty()
    def build(self):
        self.myOp = MyOp(self)
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)


Example().run()