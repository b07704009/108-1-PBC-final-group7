
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

studentidlist = []
passwordlist = []

class LoginWindow(Screen):
    studentid = ObjectProperty(None)
    password = ObjectProperty(None)

    def btn(self):
        if self.studentid.text == '' or self.password.text == '':
            pass
        else:
            studentidlist.append(self.studentid.text)
            passwordlist.append(self.password.text)
            print(studentidlist)
            print(passwordlist)
            self.studentid.text = ''
            self.password.text = ''  # 跑完後清空填寫欄位


class ImageButton(ButtonBehavior, Image):
    pass


class ShareOffWindow(Screen):
    pass


class ShareOnWindow(Screen):
    pass


class MainWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('my.kv')


class MyMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()
