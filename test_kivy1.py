from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivymd.app import MDApp
import os

KV = '''
BoxLayout:
    orientation: 'vertical'
    MDSmartTile:
        id: smart_tile
        radius: 24
        box_radius: [0, 0, 24, 24]
        box_color: 1, 1, 1, .2
        size_hint_y: None
        height: "320dp"
    MDLabel:
        id: label
        size_hint_y: None
        height: self.texture_size[1]
        halign: 'center'
        valign: 'middle'
        text_size: self.size
'''

class MyApp(MDApp):
    def build(self):
        return Builder.load_string(KV)
    
    def on_start(self):
        image_path = "cats.jpg"
        if os.path.exists(image_path):
            self.root.ids.smart_tile.source = image_path
        else:
            self.root.ids.label.text = "Image not found"

MyApp().run()


# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.label import Label
# from kivy.uix.textinput import TextInput
# from kivy.properties import StringProperty, ObjectProperty

# class MyWidget(BoxLayout):
#     text_input = ObjectProperty(None)
#     label = ObjectProperty(None)
#     text = StringProperty('')

#     def __init__(self, **kwargs):
#         super(MyWidget, self).__init__(**kwargs)
#         self.text_input = TextInput()
#         self.label = Label(text=self.text)
#         self.add_widget(self.text_input)
#         self.add_widget(self.label)
#         self.text_input.bind(text=self.on_text)

#     def on_text(self, instance, value):
#         self.text = value
#         self.label.text = self.text

# class MyApp(App):
#     def build(self):
#         return MyWidget()

# if __name__ == '__main__':
#     MyApp().run()





# # Garbage
# # from kivymd.app import MDApp
# # from kivymd.uix.screen import MDScreen
# # from kivymd.uix.button import MDRectangleFlatButton


# # class MainApp(MDApp):

# #     def build(self):
# #         self.theme_cls.theme_style = "Dark"
# #         self.theme_cls.primary_palette = "Orange"

#     #     return (
#     #         MDScreen(
#     #             MDRectangleFlatButton(
#     #                 text="Hello, World",
#     #                 pos_hint={"center_x": 0.5, "center_y": 0.5},
#     #             )
#     #         )
#     #     )
