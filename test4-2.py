from kivy.lang import Builder
from pathlib import Path
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivymd.uix.imagelist.imagelist import MDSmartTile
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.widget import MDWidget

from kivymd.uix.button import MDIconButton
from kivymd.app import MDApp
from kivymd.uix.recycleview import MDRecycleView as RecycleView

link_path = "F:/data/link.windows"
KV = '''
<DrawerClickableItem@MDNavigationDrawerItem>
    focus_color: "#e7e4c0"
    text_color: "#4a4939"
    icon_color: "#4a4939"
    ripple_color: "#c5bdd2"
    selected_color: "#0c6c4d"


<DrawerLabelItem@MDNavigationDrawerItem>
    text_color: "#4a4939"
    icon_color: "#4a4939"
    focus_behavior: False
    selected_color: "#4a4939"
    _no_ripple_effect: True


    
<MyRec>:
    viewclass: 'Button'
    RecycleBoxLayout:
        padding: ('0dp', '100dp', '0dp', '0dp')
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'

MDScreen:

    MDNavigationLayout:

        MDScreenManager:

            MDScreen:

                MDTopAppBar:
                    title: "Navigation Drawer"
                    elevation: 4
                    pos_hint: {"top": 1}
                    md_bg_color: "#e7e4c0"
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")],["dots-vertical", lambda x: app.root.callback(x)],["dots-vertical", lambda x: app.root.callbackx(x)]]
                MDBoxLayout:
                    MyRec:

        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)

            MDNavigationDrawerMenu:

                MDNavigationDrawerHeader:
                    title: "Header title"
                    title_color: "#4a4939"
                    text: "Header text"
                    spacing: "4dp"
                    padding: "12dp", 0, 0, "56dp"

                MDNavigationDrawerLabel:
                    text: "Mail"

                DrawerClickableItem:
                    icon: "gmail"
                    right_text: "+99"
                    text_right_color: "#4a4939"
                    text: "Inbox"

                DrawerClickableItem:
                    icon: "send"
                    text: "Outbox"

                MDNavigationDrawerDivider:

                MDNavigationDrawerLabel:
                    text: "Labels"

                DrawerLabelItem:
                    icon: "information-outline"
                    text: "Label"

                DrawerLabelItem:
                    icon: "information-outline"
                    text: "Label"
'''

class MyWidget(MDWidget):
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
        self.data = [{'text': str(x)} for x in range(50)]
        MDApp.get_running_app().rv = self


class Example(MDApp):
    def callback(self, instance):
        print(instance)
    def callbackx(self, instance):
        print(instance)
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)


Example().run()