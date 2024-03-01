import sqlite3
from kivymd.app import  MDApp
from kivy.properties import ObjectProperty,StringProperty
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker

from kivymd.uix.button import MDFloatingActionButton,MDTextButton,MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import OneLineListItem,ThreeLineListItem,OneLineAvatarIconListItem,MDList,IconLeftWidget,OneLineIconListItem
from kivymd.uix.slider import MDSlider
from kivymd.uix.button import MDFloatingActionButton,MDTextButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable

from datetime import datetime
from kivy.properties import ListProperty
from database import Database
class Test(MDApp):
    task_list_dialog = None
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.db=Database()
    def build(self):
        self.theme_cls.primary_palette = "Teal"
    def on_start(self):
        self.refresh_tasks_in_menu()
    def show_tasks(self):
        self.task_list_dialog=MDDialog(title="Add Assignment",type="custom",content_cls=AddingDialog(self.refresh_tasks_in_menu))
        self.task_list_dialog.open()
    def refresh_tasks_in_menu(self):
        self.root.ids.shortest.clear_widgets()
        self.root.ids.important.clear_widgets()

        shortest = self.db.get_5shortest()
        for task in shortest:
            self.add_task_to_list(task, self.root.ids.shortest)

        important = self.db.get_5important()
        for task in important:
            self.add_task_to_list(task, self.root.ids.important)

    def add_task_to_list(self, task, target_list):
        task_list = list(task)
        if task_list[1] is None:
            task_list[1] = '0'
        b = ThreeLineListItem(id=str(task_list[3]), text=task_list[0], secondary_text=str(task_list[1]),
                              tertiary_text=task_list[2])
        b.bind(on_release=self.print_id)
        target_list.add_widget(b)
    def print_id(self,instance):
        itemid=instance.id
        attributes=self.db.get_attributes(itemid)
        self.adding_dialog=MDDialog(title="Edit Assignment",type="custom",content_cls=UpdateDialog(str(attributes[0]),str(attributes[1]),str(attributes[2]),str(attributes[3]),str(attributes[4]),str(attributes[5]),str(attributes[6]),str(attributes[7]),str(attributes[8]),str(attributes[9]),self.refresh_tasks_in_menu))
        self.adding_dialog.open()
    def show_data_table(self):
        self.root.current = "data_table"
    def update_prefs(self):
        prefs=self.root.get_screen("preferences")
        ects=prefs.ids.ects
        val=ects.value
        print(val)
    def pref_value(self,column):
        return self.db.get_preference_value(column)
class UpdateDialog(MDBoxLayout):
    def __init__(self,id,assignment,course,ects,grade,due,diff,time,likable,status,refresh_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "5dp"
        self.size_hint_y = None
        self.height = "600dp"
        self.app=Database()
        self.id=id
        self.assignment=assignment
        self.course=course
        self.ects=ects
        self.grade_perc=grade
        self.due_date=due
        self.difficulty=diff
        self.time_consumption=time
        self.likability=likable
        self.status=status
        self.refresh_callback=refresh_callback

        self.assignment_text = MDTextField(hint_text="Assignment", text=self.assignment,required=True,helper_text_mode="on_error",helper_text="Assignment must not be empty")
        self.course_text = MDTextField(hint_text="Course", helper_text_mode="persistent",text=self.course)
        self.ects_text = MDTextField(hint_text="ECTS", text=self.ects)
        self.grade_perc_text = MDTextField(hint_text="Grade Percentage", text=self.grade_perc)
        self.due_date_text = MDTextField(hint_text="Due Date", text=self.due_date,date_format="yyyy/mm/dd",validator="date",required=True,helper_text_mode='on_error',helper_text="Enter a valid date YYYY/MM/DD")
        self.difficulty_text = MDTextField(hint_text="Difficulty", text=self.difficulty)
        self.time_consumption_text = MDTextField(hint_text="Time Consumption", text=self.time_consumption)
        self.likability_text = MDTextField(hint_text="Likability", text=self.likability)
        self.status_text = MDTextField(hint_text="Status", text=self.status)
        self.grid=MDBoxLayout(orientation="horizontal",size_hint_y=0.05, size_hint_x=1)
        self.cancel=MDFlatButton(text="Cancel")
        self.cancel.bind(on_release=self.close_dialog)
        self.add=MDFlatButton(text="Save changes")
        self.add.bind(on_release=self.save_changes)
        self.remove_button=MDFlatButton(text="REMOVE")
        self.remove_button.bind(on_release=self.confirm_removal)
        self.grid.add_widget(self.remove_button)
        self.change_status_button=MDFlatButton(text="COMPLETED")
        self.change_status_button.bind(on_release=self.set_done)
        self.grid.add_widget(self.change_status_button)
        self.grid.add_widget(self.cancel)
        self.grid.add_widget(self.add)

        self.layout = MDBoxLayout(orientation="vertical",size_hint_y=0.80)
        self.layout.add_widget(self.assignment_text)
        self.layout.add_widget(self.course_text)
        self.layout.add_widget(self.ects_text)
        self.layout.add_widget(self.grade_perc_text)
        self.layout.add_widget(self.due_date_text)
        self.layout.add_widget(self.difficulty_text)
        self.layout.add_widget(self.time_consumption_text)
        self.layout.add_widget(self.likability_text)
        self.layout.add_widget(self.status_text)
        self.add_widget(self.layout)
        self.add_widget(self.grid)
    def save_changes(self,instance):
        id=self.id
        assignment=self.assignment_text.text
        course = self.course_text.text
        ects = self.ects_text.text
        grade_perc = self.grade_perc_text.text
        due_date = self.due_date_text.text
        difficulty = self.difficulty_text.text
        time_consumption = self.time_consumption_text.text
        likability = self.likability_text.text
        status = self.status_text.text
        if assignment=='' or due_date=='':
            self.show_dialog(title="Error",text='Empty values in required inputs')
        if assignment!='' and due_date!='':
            try:
                self.app.alter_task(id,assignment,due_date,course,ects,grade_perc,difficulty,time_consumption,likability,status)
                self.confirmation_window=MDDialog(title="SAVE CHANGES?",type="custom",content_cls=WarningDialog())
                self.confirmation_window.open()
                self.refresh_callback()
            except  sqlite3.IntegrityError:
                self.show_dialog(title="Error", text='Insufficient data')

    def confirm_removal(self,instance):
        id=self.id
        self.app.remove_task(id)
        self.refresh_callback()
        self.parent.parent.parent.dismiss()
    def set_done(self,instance):
        id=self.id
        self.app.mark_as_completed(id)
        self.refresh_callback()
        self.parent.parent.parent.dismiss()

    def show_dialog(self, title, text):
        dialog = MDDialog(title=title, text=text, size_hint=(0.4, 0.2))
        dialog.open()
    def close_dialog(self,instance):
        self.parent.parent.parent.dismiss()


    def show_data_table(self):
        self.root.current = "data_table"

class CustomDialogContent(MDBoxLayout):
    city_hint_text = StringProperty("City")
    street_hint_text = StringProperty("Street")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "5dp"
        self.size_hint_y = None
        self.height = "300dp"

        self.assignment_text = MDTextField(hint_text="Assignment", required=True,
                                           helper_text_mode="on_error", helper_text="Assignment must not be empty")
        self.course_text = MDTextField(hint_text="Course")
        self.ects_text = MDTextField(hint_text="ECTS")
        self.grade_perc_text = MDTextField(hint_text="Grade Percentage")
        self.due_date_text = MDTextField(hint_text="Due Date", date_format="yyyy/mm/dd",
                                         validator="date", required=True, helper_text_mode='on_error',
                                         helper_text="Enter a valid date YYYY/MM/DD")
        self.difficulty_text = MDTextField(hint_text="Difficulty")
        self.time_consumption_text = MDTextField(hint_text="Time Consumption")
        self.likability_text = MDTextField(hint_text="Likability")
        self.layout = MDBoxLayout(orientation="vertical", size_hint_y=0.80)
        self.layout.add_widget(self.assignment_text)
        self.layout.add_widget(self.course_text)
        self.layout.add_widget(self.ects_text)
        self.layout.add_widget(self.grade_perc_text)
        self.layout.add_widget(self.due_date_text)
        self.layout.add_widget(self.difficulty_text)
        self.layout.add_widget(self.time_consumption_text)
        self.layout.add_widget(self.likability_text)
        self.grid = MDGridLayout()
        b1 = MDFlatButton(text="Cancel")
        b2 = MDFlatButton(text="Save")
        self.grid.add_widget(b1)
        self.grid.add_widget(b2)
        self.layout.add_widget(self.grid)
        self.city=MDTextField(hint_text=self.city_hint_text)
        self.add_widget(self.city)
        self.add_widget(MDTextField(hint_text=self.street_hint_text))
        self.b1=MDFloatingActionButton(icon="calendar")
        self.b1.bind(on_release=self.show_date_picker)
        self.add_widget(self.b1)
        self.add_widget(self.layout)
    def show_date_picker(self,instance):
        date_picker = MDDatePicker()
        date_picker.bind(on_save=lambda instance, value, date_range: self.on_date_picker_save(value))
        date_picker.open()
        print(self.city.text)

    def on_date_picker_save(self, selected_date):
        selected_date_str = selected_date.strftime("%Y-%m-%d")  # Format the selected date as a string
        print("Selected date:", selected_date_str)

class AddingDialog(MDBoxLayout):
    def __init__(self,refresh_callback, **kwargs):
        super().__init__(**kwargs)
        self.db=Database()
        self.orientation = "vertical"
        self.spacing = "5dp"
        self.size_hint_y = None
        self.height = "700dp"
        self.refresh_callback = refresh_callback

        self.assignment_text = MDTextField(hint_text="Assignment", required=True,
                                           helper_text_mode="on_error", helper_text="Assignment must not be empty")
        self.course_text = MDTextField(hint_text="Course")
        self.ects_text = MDTextField(hint_text="ECTS")
        self.grade_perc_text = MDTextField(hint_text="Grade Percentage")
        self.due_date_text = MDTextField(hint_text="Due Date", date_format="yyyy/mm/dd",
                                         validator="date", required=True, helper_text_mode='on_error',
                                         helper_text="Enter a valid date YYYY/MM/DD")
        self.difficulty_text = MDTextField(hint_text="Difficulty")
        self.time_consumption_text = MDTextField(hint_text="Time Consumption")
        self.likability_text = MDTextField(hint_text="Likability")
        self.layout = MDBoxLayout(orientation="vertical", size_hint_y=0.80)
        self.layout.add_widget(self.assignment_text)
        self.layout.add_widget(self.course_text)
        self.layout.add_widget(self.ects_text)
        self.layout.add_widget(self.grade_perc_text)
        self.layout.add_widget(self.due_date_text)
        self.layout.add_widget(self.difficulty_text)
        self.layout.add_widget(self.time_consumption_text)
        self.layout.add_widget(self.likability_text)
        self.grid=MDGridLayout(cols=2)
        b1=MDFlatButton(text="Cancel")
        b1.bind(on_release=self.close_dialog)
        b2=MDFlatButton(text="Save")
        b2.bind(on_release=self.confirm)
        self.grid.add_widget(b1)
        self.grid.add_widget(b2)
        self.layout.add_widget(self.grid)
        self.add_widget(self.layout)

    def close_dialog(self, instance):
        self.parent.parent.parent.dismiss()
    def confirm(self,instance):
        assignment=self.assignment_text.text
        course=self.course_text.text
        due_date=self.due_date_text.text
        ects=self.ects_text.text
        grade_perc=self.grade_perc_text.text
        difficulty=self.difficulty_text.text
        time_consumption=self.time_consumption_text.text
        likability=self.likability_text.text
        self.db.add_tasks(assignment,due_date,course,ects,grade_perc,difficulty,time_consumption,likability)
        self.refresh_callback()

class WarningDialog(MDBoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.app=Database()
        self.layout=MDBoxLayout()
        self.b1=MDFlatButton(text="CANCEL")
        self.b1.bind(on_release=self.close_dialog)
        self.b2=MDFlatButton(text="SAVE")
        self.b2.bind(on_release=self.app.comm)
        self.layout.add_widget(self.b1)
        self.layout.add_widget(self.b2)
        self.add_widget(self.layout)
    def close_dialog(self,instance):
        self.parent.parent.parent.dismiss()
class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class TaskTable(MDScreen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()
        self.db=self.app.db
        self.build()

    def build(self):


        layout = MDBoxLayout(orientation='vertical')

        self.data_table = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[
                ("Assignment", dp(50)),
                ("Course", dp(30)),
                ("Status", dp(30)),
                ("Due Date", dp(30)),
            ],
            row_data=self.db.get_tastk(),
            pos_hint={'center_x': 0.5,"y":0.05},
            size_hint=(1, 0.8)
        )
        layout.add_widget(self.data_table)

        self.add_widget(layout)
class DataTableScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.db = self.app.db
        self.build()

    def build(self):

        layout = MDBoxLayout(orientation='vertical',size_hint_x=1)



        self.data_table = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[
                ("Assignment", dp(50)),
                ("Course", dp(30)),
                ("Status", dp(30)),
                ("Due Date", dp(30)),
            ],
            row_data=self.db.get_tasks(),
            pos_hint={'center_x': 0.5, "y": 0.05},
            size_hint=(1, 0.8)
        )
        layout.add_widget(self.data_table)

        self.add_widget(layout)

        self.b1=MDTextButton(text="print")
        layout.add_widget(self.b1)


        self.row_data = self.get_rowdata()

    def get_rowdata(self):
        rows = self.db.cursor.execute("SELECT Assignment, Course, Status, Due_date FROM Tasks").fetchall()
        row_data = [(str(row[0]), row[1], row[2], row[3],) for row in rows]
        return row_data
class PreferencesScreen(MDScreen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.db=Database()
    '''def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db=Database()
        self.layout=MDBoxLayout(orientation="vertical")
        self.items = [
            {"id": "ECTS", "text": "ECTS", "icon": "star", "value": self.db.get_preference_value("ECTS")},
            {"id": "Due_date", "text": "Due Date", "icon": "calendar-clock",
             "value": self.db.get_preference_value("Due_date")},
            {"id": "Grade_percentage", "text": "Grade Percentage", "icon": "percent",
             "value": self.db.get_preference_value("Grade_percentage")},
            {"id": "Difficulty", "text": "Difficulty", "icon": "fire",
             "value": self.db.get_preference_value("Difficulty")},
            {"id": "Time_consumption", "text": "Time consumption", "icon": "timer",
             "value": self.db.get_preference_value("Time_consumption")},
            {"id": "Likability", "text": "Likability", "icon": "heart",
             "value": self.db.get_preference_value("Likability")},
            {"id": "Importance", "text": "Importance", "icon": "exclamation",
             "value": self.db.get_preference_value("Importance")},
        ]
        for item_data in self.items:
            header = MDList(OneLineIconListItem(IconLeftWidget(icon=item_data["icon"]), text=item_data["text"]))
            slider=MDSlider(id=item_data["id"],value=item_data["value"])
            self.layout.add_widget(header)
            self.layout.add_widget(slider)



        self.prefs_list = self.create_prefs_list()
        self.add_widget(self.prefs_list)

    def create_prefs_list(self):
        prefs_list = MDList()
        self.items = [
            {"id": "ECTS", "text": "ECTS"},
            {"id": "Due_date", "text": "Due Date"},
            {"id": "Grade_percentage", "text": "Grade Percentage"},
            {"id": "Difficulty", "text": "Difficulty"},
            {"id": "Time_consumption", "text": "Time consumption"},
            {"id": "Likability", "text": "Likability"},
            {"id": "Importance", "text": "Importance"},
        ]
        for item_data in self.items:
            item = OneLineIconListItem(id=item_data["id"], text=item_data["text"])
            item.add_widget(IconLeftWidget(icon="tune"))
            item.bind(on_release=self.show_dialog)
            prefs_list.add_widget(item)
        return prefs_list

    def show_dialog(self,instance):
        id=instance.id
        self.dialog=MDDialog(title="Select Value",type="custom",content_cls=PreferencesDialog(id))
        self.dialog.open()'''
class PreferencesDialog(MDBoxLayout):
    def __init__(self,id, **kwargs):
        super().__init__(**kwargs)
        self.db=Database()
        self.orientation = "vertical"
        self.spacing = "5dp"
        self.size_hint_y = None
        self.height = "400dp"
        self.id=id
        self.orientation="vertical"
        checked=self.checked_value()
        print(checked)
        #self.items=[ItemConfirm(text="0"),ItemConfirm(text="1"),ItemConfirm(text="2"),ItemConfirm(text="3"),ItemConfirm(text="4"),ItemConfirm(text="5")]
        for i in range(0,6):
            text=f'{i}'
            item=ItemConfirm(text=f'{i}')
            self.add_widget(item)
        '''for item in self.items:
            if item.text==str(checked):
                item.checked=True
            self.add_widget(item)'''
        self.grid=MDGridLayout(cols=2)
        b1=MDFlatButton(text="cancel")
        b1.bind(on_release=self.print_id)
        self.grid.add_widget(b1)
        b2=MDFlatButton(text="confirm")
        self.grid.add_widget(b2)
        self.add_widget(self.grid)
    def checked_value(self):
        preference=self.db.get_preference_value(self.id)
        return preference[0]
    def print_id(self,instance):
        print(self.db.get_preference_value(self.id))

class SliderWidget(MDGridLayout):
    def __init__(self,preference,icon,value,**kwargs):
        super().__init__(**kwargs)
        self.rows=2
        self.icon= icon
        self.preference=preference
        self.value=value
        self.list=MDList(items=[OneLineIconListItem(IconLeftWidget(icon=self.icon),text=self.preference)])
        self.add_widget(self.list)
        self.slider=MDSlider(id=self.preference,value=self.value)
        #dodac reszte


class ItemConfirm(OneLineAvatarIconListItem):
    divider = None
    def __init__(self,**kwargs):
        super().__init__(**kwargs)



    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False

if __name__ == '__main__':
    Test().run()

