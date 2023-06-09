from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.properties import ObjectProperty

from kivymd.uix.button import MDRaisedButton




class MyButton(MDRaisedButton):
    label_obj = ObjectProperty(None)
    text_field = ObjectProperty(None)
    def on_release(self, *args):
        self.label_obj.text = self.text_field.text


class MainApp(MDApp):
    #text_input = StringProperty()

    def build(self):
        return Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    
    MDTextField:
        id: my_text_field
        hint_text: "Enter something"
        
    MyButton:
        label_obj: my_label
        text_field: my_text_field
        text: "Display Text"
        pos_hint: {"center_x": 0.5}

    MDLabel:
        id: my_label
        halign: 'center'

''')

MainApp().run()
