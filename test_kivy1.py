from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ObjectProperty

class MyWidget(BoxLayout):
    text_input = ObjectProperty(None)
    label = ObjectProperty(None)
    text = StringProperty('')

    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        self.text_input = TextInput()
        self.label = Label(text=self.text)
        self.add_widget(self.text_input)
        self.add_widget(self.label)
        self.text_input.bind(text=self.on_text)

    def on_text(self, instance, value):
        self.text = value
        self.label.text = self.text

class MyApp(App):
    def build(self):
        return MyWidget()

if __name__ == '__main__':
    MyApp().run()





# Garbage
# from kivymd.app import MDApp
# from kivymd.uix.screen import MDScreen
# from kivymd.uix.button import MDRectangleFlatButton


# class MainApp(MDApp):

#     def build(self):
#         self.theme_cls.theme_style = "Dark"
#         self.theme_cls.primary_palette = "Orange"

    #     return (
    #         MDScreen(
    #             MDRectangleFlatButton(
    #                 text="Hello, World",
    #                 pos_hint={"center_x": 0.5, "center_y": 0.5},
    #             )
    #         )
    #     )
