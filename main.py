
import sys
from kivy.uix.boxlayout import BoxLayout
from kivy.uix import dropdown
from kivy.uix.popup import Popup
from mysql.connector.errors import Error
import mysql.connector
from kivy.garden.mapview import MapView, MapMarker
import kivy
from kivy.app import App
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.base import runTouchApp

studentidlist = []
passwordlist = []

studentidmem = ['000']
parking_place = ['a']

config = {
        'host': 'johnny.heliohost.org',
        'user': 'pbcbike_root',
        'password': 'password0987',
        'database': 'pbcbike_pbc108'
}
dbforpbc = mysql.connector.connect(**config)
cursor = dbforpbc.cursor()


def connect_to_db():
    global dbforpbc
    dbforpbc = mysql.connector.connect(**config)
    global cursor
    cursor = dbforpbc.cursor()


class Map(MapView):
    pass


def login_success_or_not(login_id, password):
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)  # errno, sqlstate, msg values
        print("Please try again later")
    else:
        cursor.execute("SELECT student_id, password FROM users WHERE student_id = '%s'" % login_id)
        result = cursor.fetchall()
        if len(result) != 1:
            return False
        else:
            if result[0][1] == password:
                return True
            else:
                return False


class LoginWindow(Screen):

    studentid = ObjectProperty(None)
    password = ObjectProperty(None)


    def login_btn(self):
        if login_success_or_not(self.studentid.text, self.password.text) is True:
            studentidmem[0] = self.studentid.text
            self.reset()
            kv.current = 'shareon'

        else:
            pop = Popup(title='Invalid Login',
                        content=Label(text='Invalid username or password.'),
                        size_hint=(None, None), size=(400, 400))
            pop.open()

    def reset(self):
        self.studentid.text = ""
        self.password.text = ""


class ImageButton(ButtonBehavior, Image):
    pass


class ShareOnWindow(Screen):
    def btnbasicinformation(self):
        pass





class WindowManager(ScreenManager):
    pass


class CustomDropDown(BoxLayout):
    pass


class Mybikepark(Screen):
    mainbtn = ObjectProperty(None)

    def valuereturn(self, str):
        parking_place[0] = str



    def update_location(self):
        try:
            connect_to_db()
        except mysql.connector.Error as e:
            print("Error:", e)  # errno, sqlstate, msg values
            print("Please try again later")
        else:
            cursor.execute("SELECT place_id FROM parking_space where p_name = '%s' " % parking_place[0])
            print(parking_place[0])
            update_id = cursor.fetchall()[0][0]
            cursor.execute("UPDATE users SET current_location_id = '%s' WHERE student_id = '%s'" % (update_id, studentidmem[0]))
            dbforpbc.commit()
            cursor.close()
            dbforpbc.close()




class Basicinformation(Screen):
    pass


class Pastfeed(Screen):
    pass





kv = Builder.load_file('my.kv',  encoding="utf-8")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()
