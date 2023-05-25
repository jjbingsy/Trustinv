from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.uix.recycleview import MDRecycleView as RecycleView
from kivymd.uix.navigationdrawer import MDNavigationDrawerMenu
from kivymd.uix.imagelist.imagelist import MDSmartTile
from kivymd.uix.dialog import MDDialog
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
import sqlite3
import subprocess
from pathlib import Path
import threading

from trustmod.vars.env_001 import IDOLSDB_PATH as IDP, IMAGE_DIRECTORY as IDD, MEDIA_DIRECTORIES as MDD, SIMLINK_DIRECTORY as SDD
jj = '''

https://kivymd.readthedocs.io/en/1.1.1/components/navigationdrawer/index.html
SELECT i.shared_key, COUNT(DISTINCT fi.film_name) AS distinct_film_count FROM idols i JOIN film_idols fi ON i.link = fi.idol_link GROUP BY i.shared_key ORDER BY distinct_film_count ASC, i.shared_key ASC;



SELECT i1.shared_key, i1.name FROM idols AS i1 JOIN (SELECT shared_key, MIN(link) AS min_link FROM idols GROUP BY shared_key ) AS i2 ON i1.shared_key = i2.shared_key AND i1.link = i2.min_link;

'''
ssss = '''SELECT i.shared_key, COUNT(fi.film_name) AS film_count FROM idols i JOIN film_idols fi ON i.link = fi.idol_link GROUP BY i.shared_key ORDER BY film_count ;
'''


HH = '''SELECT 
    i.shared_key, 
    i.name 
FROM 
    idols AS i
JOIN 
    (
        SELECT 
            shared_key, 
            idol_link
        FROM 
            (
                SELECT 
                    i.shared_key,
                    fi.idol_link,
                    COUNT(*) as count
                FROM 
                    idols AS i
                JOIN 
                    film_idols AS fi 
                ON 
                    i.link = fi.idol_link
                GROUP BY 
                    i.shared_key, 
                    fi.idol_link
            ) 
        WHERE 
            count = 
            (
                SELECT 
                    MAX(count) 
                FROM 
                    (
                        SELECT 
                            shared_key, 
                            COUNT(*) as count
                        FROM 
                            idols 
                        JOIN 
                            film_idols 
                        ON 
                            idols.link = film_idols.idol_link
                        GROUP BY 
                            shared_key
                    ) 
                WHERE 
                    shared_key = i.shared_key
            )
    ) AS subquery 
ON 
    i.shared_key = subquery.shared_key AND 
    i.link = subquery.idol_link;
'''
KV = '''

<DrawerClickableItem@MDNavigationDrawerItem>
    focus_color: "#e7e4c0"
    text_color: "#4a4939"
    icon_color: "#4a4939"
    ripple_color: "#c5bdd2"
    selected_color: "#0c6c4d"


MDScreen:
    id: mdscr
    MDNavigationLayout:
        id: mdl
        MDScreenManager:
            id: mdsm
            MDScreen:
                id: mdssss
                MDBoxLayout:
                    id: mbll
                    orientation: 'vertical'
                    MDTopAppBar:
                        title: "Navigation Drawer"
                        elevation: 4
                        pos_hint: {"top": 1}
                        md_bg_color: "#e7e4c0"
                        specific_text_color: "#4a4939"
                        left_action_items:
                            [['menu', lambda x: nav_drawer.set_state("open")], ["dots-vertical", lambda x: app.myOp.click1(60)]]
                    MyRec:
                        id: rec
                        viewclass: 'Button'
                        MDRecycleGridLayout:
                            id: rggdfdferr
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
            MyNavigatorDrawer:
                DrawerClickableItem:
                    icon: "gmail"
                    right_text: "+99"
                    text_right_color: "#4a4939"
                    text: "Inbox"
                    on_release: app.myOp.click1(324)

            

'''


class MyNavigatorDrawer(MDNavigationDrawerMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    
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
    films2 = [{'source': f'{IDD}/{i[0]}.jpg', 'text' : i[0] } for i in films]
    return films2




class MyRec(RecycleView):
    def __init__(self, **kwargs):
        MDApp.get_running_app().myOp.myRC(self)
        super().__init__(**kwargs)
        #self.data = films_from_idols(83, 43) # [{'text': str(x)} for x in range(50)]

        self.data = films_from_idols(43) # [{'text': str(x)} for x in range(50)]
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
            print ("MY-ID = ", self.ids)



class ContentNavigationDrawer(MDBoxLayout):
    pass


class Example(MDApp):
    myOp = ObjectProperty()
    def callback(self):
        print ("callback")
    def build(self):
        self.myOp = MyOp(self)
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)


Example().run()