import sys
from kivy.garden.mapview import MapView, MapMarker
import kivy
from kivy.app import App
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.base import runTouchApp

studentidlist = []
passwordlist = []


class Map(MapView):
    pass


class CustomDropDown(DropDown):
    def dropdowntest():

        dropdown = DropDown()

        mainbutton = Button(text='Hello', size_hint=(0.6, 0))
        mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        return runTouchApp(mainbutton)


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
    def btnbasicinformation(self):
        pass


class MainWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class Mybikepark(Screen):
    pass


class Basicinformation(Screen):
    pass


class Pastfeed(Screen):
    pass


class Successfulrent(Screen):
    pass


class Bikeavailable(Screen):
    pass


class Bikerent(Screen):
    pass


kv = Builder.load_file('my.kv',  encoding="utf-8")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()
