from kivy.app import App
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown


from kivy.uix.togglebutton import ToggleButtonBehavior


from kivy.adapters.models import SelectableDataItem


from kivy.lang import Builder



Builder.load_string("""


#: import ListAdapter kivy.adapters.listadapter.ListAdapter


#: import Factory kivy.factory.Factory



<MyListItem>:


 height: 50



 on_state: root.is_selected = args[1] =="down"


 state:"down" if root.is_selected else"normal"



 BoxLayout:


 spacing: 10



 CheckBox:


 on_state: root.is_selected = args[1] =="down"


 state:"down" if root.is_selected else"normal"


 # on_state: root.state = args[1]


 # state: root.state



 Label:


 text: root.name



<Page>:


 orientation:"vertical"



 ListView:


 id: LV


 adapter: ListAdapter(data=root.data, cls=Factory.MyListItem, args_converter=root.args_converter, selection_mode="multiple", propagate_selection_to_data=True)



 Button:


 size_hint_y: None


 text:"print selection"


 on_press: print(LV.adapter.selection)


""")



class MyListItem(ToggleButtonBehavior, SelectableView, BoxLayout):


 name = StringProperty()



 def __repr__(self):


 return"%s(name=%r)" % (type(self).__name__, self.name)



 def on_state(self, me, state):


 print me, state


 if state =="down":


 self.select()


 else:


 self.deselect()


 # self.is_selected = state =="down"



class DataItem(SelectableDataItem):


 def __init__(self, name, **kwargs):


 super(DataItem, self).__init__(**kwargs)


 self.name = name



 def __repr__(self):


 return"%s(name=%r, is_selected=%r)" % (type(self).__name__, self.name, self.is_selected)



class Page(BoxLayout):


 data = ListProperty()



 def __init__(self, **kwargs):


 super(Page, self).__init__(**kwargs)


 self.data = [DataItem("Item {}".format(i), is_selected=True) for i in range(10)]



 def args_converter(self, index, data_item):


 return {


"index": index,


"name": data_item.name,


 }



class ExampleApp(App):


 def build(self):


 return Page()



if __name__ =="__main__":


 ExampleApp().run()