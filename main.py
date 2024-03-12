import sqlite3
from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import (BaseListItem, OneLineListItem, OneLineAvatarIconListItem, MDList, IconLeftWidget,
                             ThreeLineAvatarIconListItem, IRightBodyTouch)
from kivymd.uix.slider import MDSlider
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable


class Database:
    def __init__(self):
        self.connection_to_db = sqlite3.connect("app1.db")
        self.cursor = self.connection_to_db.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS Tasks(IdT INTEGER NOT NULL CONSTRAINT Tasks_pk PRIMARY KEY AUTOINCREMENT, Assignment TEXT NOT NULL, Course TEXT, ECTS INTEGER, Due_date TEXT NOT NULL, Grade_percentage REAL, Difficulty INTEGER, Time_consumption INTEGER, Likability INTEGER, Status TEXT default 'To do');''')
        self.connection_to_db.commit()
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS Preferences(ECTS INTEGER default 1,Due_date INTEGER default 1, Grade_percentage INTEGER default 1, Difficulty INTEGER default 1,Time_consumption INTEGER default 1,Likability INTEGER default 1,Importance INTEGER default 1) ''')
        self.connection_to_db.commit()
        if not self.cursor.execute("SELECT * FROM Preferences").fetchone():
            self.cursor.execute(
                "INSERT INTO Preferences(ECTS,Due_date,Grade_percentage,Difficulty,Time_consumption,Likability,Importance) VALUES (1,1,1,1,1,1,1)")
            self.connection_to_db.commit()
        if not self.cursor.execute("SELECT * FROM Tasks").fetchall():
            self.cursor.execute(
                "INSERT INTO Tasks(Assignment,Course,ECTS,Due_date,Grade_percentage,Difficulty,Time_consumption,Likability,Status)VALUES ('Sample task','Sample course',2,'2024/01/01',0.5,1,1,1,'To do')")
            self.connection_to_db.commit()

    def add_tasks(self, assignment, duedate, course=None, ects=None, gradeperc=None, diff=None, time=None, like=None):
        sql = f"INSERT INTO Tasks(Assignment,Course,ECTS,Due_date,Grade_percentage,Difficulty,Time_consumption,Likability) VALUES('{assignment}','{course}','{ects}','{duedate}','{gradeperc}','{diff}','{time}','{like}');"
        self.cursor.execute(sql)
        self.connection_to_db.commit()

    def get_5shortest(self):
        sql = "SELECT Assignment,Course,Due_date,IdT FROM Tasks WHERE status='To do' ORDER BY Due_date  LIMIT 5"
        results = self.cursor.execute(sql).fetchall()
        return results

    def get_5important(self):
        sql = "SELECT Assignment,ECTS*Grade_percentage AS Importance,Due_date,IdT FROM Tasks WHERE status='To do' ORDER BY Importance DESC LIMIT 5"
        results = self.cursor.execute(sql).fetchall()
        return results

    def get_attributes(self, idt):
        sql = f'SELECT * FROM TASKS WHERE IdT={idt}'
        return self.cursor.execute(sql).fetchone()

    def alter_task(self, idt, assignment, duedate, course, ects, gradeperc, diff, time, like, status):
        sql = f'''UPDATE Tasks SET Assignment='{assignment}',Course='{course}', ECTS='{ects}', Grade_percentage='{gradeperc}', Due_date='{duedate}', Difficulty='{diff}', Time_consumption='{time}', Likability='{like}', Status='{status}' WHERE IdT='{idt}';'''
        self.cursor.execute(sql)
        self.connection_to_db.commit()

    def remove_task(self, idt):
        sql = f"DELETE FROM Tasks WHERE IdT='{idt}';"
        self.cursor.execute(sql)
        self.connection_to_db.commit()

    def mark_as_completed(self, idt):
        sql = f"UPDATE Tasks SET Status ='Done' WHERE IdT='{idt}'"
        self.cursor.execute(sql)
        self.connection_to_db.commit()

    def get_preference_value(self, column):
        sql = f'''SELECT {column} FROM Preferences'''
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result[0]

    def update_preferences_values(self, ects, duedate, gradeperc, difficulty, time, like, importance):
        sql = f'''UPDATE Preferences SET ECTS='{ects}',Due_date='{duedate}', Grade_percentage='{gradeperc}',Difficulty='{difficulty}', Time_consumption='{time}', Likability='{like}',Importance='{importance}'; '''
        self.cursor.execute(sql)
        self.connection_to_db.commit()

    def get_task_list(self):
        weights = self.cursor.execute("SELECT * FROM Preferences").fetchone()
        user_preferences = f'ECTS*{weights[0]} DESC ,Due_date * {weights[1]} DESC,Grade_percentage * {weights[2]} DESC ,Difficulty *{weights[3]} DESC,Time_consumption * {weights[4]} DESC,Likability *{weights[5]} DESC,Importance * {weights[6]} DESC'
        rows = self.cursor.execute(
            f"SELECT IdT, Assignment, Course, ECTS, Grade_percentage, Due_date, Difficulty, Time_consumption, Likability, ECTS*Grade_percentage AS Importance FROM Tasks WHERE Status = 'To do' ORDER BY {user_preferences}").fetchall()
        row_data = [(str(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]) for row in
                    rows]
        return row_data

    def get_archive(self):
        weights = self.cursor.execute("SELECT * FROM Preferences").fetchone()
        user_preferences = f'ECTS*{weights[0]} DESC ,Due_date * {weights[1]} DESC,Grade_percentage * {weights[2]} DESC ,Difficulty *{weights[3]} DESC,Time_consumption * {weights[4]} DESC,Likability *{weights[5]} DESC,Importance * {weights[6]} DESC'
        rows = self.cursor.execute(
            f"SELECT IdT, Assignment, Course, ECTS, Grade_percentage, Due_date, Difficulty, Time_consumption, Likability, ECTS*Grade_percentage AS Importance FROM Tasks WHERE Status = 'Done' ORDER BY {user_preferences}").fetchall()
        row_data = [(str(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]) for row in
                    rows]
        return row_data

    def get_more_info(self, idt):
        sql = f'''SELECT ECTS, Grade_percentage, Difficulty, Time_consumption, Likability FROM Tasks WHERE IdT='{idt}'; '''
        info = self.cursor.execute(sql).fetchone()
        return info

    def get_theme(self):
        sql = "SELECT Theme FROM Preferences"
        color = self.cursor.execute(sql).fetchone()
        return color[0]

    def update_theme(self, theme):
        sql = f"UPDATE Preferences SET Theme='{theme}'"
        self.cursor.execute(sql)
        self.connection_to_db.commit()


# noinspection PyMethodMayBeStatic,PyAttributeOutsideInit
class Tasks(MDApp):
    task_list_dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.active_tasks = set()
        self.current_theme = self.db.get_theme()
        self.colors_dict = {"Pink": {"bg_color": (0.996078431372549, 0.9725490196078431, 1, 1),
                                     "primary_text_color": (0.59608, 0.25098, 0.38431, 1),
                                     "secondary_text_color": (0.59608, 0.25098, 0.38431, 0.75),
                                     "header_color": (0.45098, 0.18824, 0.28627, 1),
                                     "slider_color": (0.63529, 0.26667, 0.40784, 1)},
                            "Blue": {"bg_color": (0.73725, 0.91373, 1.00000, 0.1),
                                     "primary_text_color": (0.00000, 0.52941, 0.60000, 1),
                                     "secondary_text_color": (0.00000, 0.52941, 0.60000, 0.75),
                                     "header_color": (0.00000, 0.44314, 0.50196, 1),
                                     "slider_color": (0.00000, 0.61961, 0.70196, 1)}}
        self.theme = self.colors_dict[self.current_theme]
        self.bg_color = self.theme["bg_color"]
        self.primary_text_color = self.theme["primary_text_color"]
        self.secondary_text_color = self.theme["secondary_text_color"]
        self.header_color = self.theme["header_color"]
        self.slider_color = self.theme["slider_color"]
        self.chosen_theme = self.current_theme

    def build(self):
        self.theme_cls.primary_palette = "Blue"

    def on_start(self):
        self.refresh_tasks_in_menu()

    def show_tasks(self):
        self.task_list_dialog = MDDialog(title="Add Assignment", type="custom",
                                         content_cls=AddingDialog(self.refresh_tasks_in_menu))
        self.task_list_dialog.open()

    def submit_preferences_changes(self):
        ects = self.root.ids.ECTS.value
        due_date = self.root.ids.Due_date.value
        grade_perc = self.root.ids.Grade_percentage.value
        diff = self.root.ids.Difficulty.value
        time = self.root.ids.Time_consumption.value
        like = self.root.ids.Likability.value
        importance = self.root.ids.Importance.value
        self.db.update_preferences_values(ects, due_date, grade_perc, diff, time, like, importance)
        self.refresh_other_screens()

    def refresh_tasks_in_menu(self):
        self.active_tasks.clear()
        self.root.ids.shortest.clear_widgets()
        self.root.ids.important.clear_widgets()
        self.refresh_other_screens()
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
        b = ListItemWithCheckbox(IconLeftWidget(id=str(task_list[3]), theme_text_color="Custom", icon="menu",
                                                icon_color=self.primary_text_color, on_release=self.more_info_dialog),
                                 id=str(task_list[3]), text=task_list[0], secondary_text=str(task_list[1]),
                                 tertiary_text=task_list[2], theme_text_color='Custom',
                                 text_color=self.primary_text_color, secondary_theme_text_color='Custom',
                                 secondary_text_color=self.secondary_text_color, tertiary_theme_text_color='Custom',
                                 tertiary_text_color=self.secondary_text_color, bg_color=self.bg_color, divider='Inset',
                                 divider_color=(0, 1, 0, 1))
        b.divider = "Full"
        b.divider_color = self.header_color
        b.bind(on_release=self.print_id)
        target_list.add_widget(b)

    def print_id(self, instance):
        itemid = instance.id
        attributes = self.db.get_attributes(itemid)
        self.adding_dialog = MDDialog(title="Edit Assignment", type="custom",
                                      content_cls=UpdateDialog(str(attributes[0]), str(attributes[1]),
                                                               str(attributes[2]), str(attributes[3]),
                                                               str(attributes[5]), str(attributes[4]),
                                                               str(attributes[6]), str(attributes[7]),
                                                               str(attributes[8]), str(attributes[9]),
                                                               self.refresh_tasks_in_menu))
        self.adding_dialog.open()

    def refresh_other_screens(self):
        screen_manager = self.root.ids.screen_manager
        data_table_screen = screen_manager.get_screen("custom_sort")
        all_task_screen = screen_manager.get_screen("all_tasks")
        archive_screen = screen_manager.get_screen("archive")
        data_table_screen.create_screen()
        all_task_screen.create_task_widgets()
        archive_screen.create_screen()

    def pref_value(self, column):
        return self.db.get_preference_value(column)

    def more_info_dialog(self, instance):
        info = self.db.get_more_info(instance.id)
        dialog = MDDialog(title="More info", type="custom",
                          content_cls=MoreInfoDialog(info[0], info[1], info[2], info[3], info[4]))
        dialog.open()

    def on_checkbox_active(self, checkbox, value):
        checkbox.id = checkbox.parent.parent.id
        if value:
            self.active_tasks.add(checkbox.parent.parent.id)
            for items in self.root.ids.important.children:
                if items.id == checkbox.id:
                    items.ids.check.active = True
            for items in self.root.ids.shortest.children:
                if items.id == checkbox.id:
                    items.ids.check.active = True
        else:
            self.active_tasks.discard(checkbox.parent.parent.id)
            for items in self.root.ids.important.children:
                if items.id == checkbox.id:
                    items.ids.check.active = False
            for items in self.root.ids.shortest.children:
                if items.id == checkbox.id:
                    items.ids.check.active = False

    def delete_selected(self):
        for ids in self.active_tasks:
            self.db.remove_task(ids)
        self.refresh_tasks_in_menu()

    def set_done(self):
        for ids in self.active_tasks:
            self.db.mark_as_completed(ids)
        self.refresh_tasks_in_menu()

    def set_theme(self):
        self.theme = self.colors_dict[self.current_theme]
        self.bg_color = self.theme["bg_color"]
        self.primary_text_color = self.theme["primary_text_color"]
        self.secondary_text_color = self.theme["secondary_text_color"]
        self.header_color = self.theme["header_color"]
        self.slider_color = self.theme["slider_color"]

    def update_theme(self):
        if not self.current_theme == self.chosen_theme:
            self.db.update_theme(self.chosen_theme)
            self.current_theme = self.db.get_theme()
            self.set_theme()

    def open_confirm(self):
        dialog = MDDialog(title="Close the app to continue", type="custom", content_cls=WarningDialog())
        dialog.open()


# noinspection PyShadowingNames
class UpdateDialog(MDBoxLayout):
    def __init__(self, id, assignment, course, ects, grade, due, diff, time, likable, status, refresh_callback,
                 **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "5dp"
        self.size_hint_y = None
        self.height = "600dp"
        self.app = Database()
        self.id = id
        self.assignment = assignment
        self.course = course
        self.ects = ects
        self.grade_perc = grade
        self.due_date = due
        self.difficulty = diff
        self.time_consumption = time
        self.likability = likable
        self.status = status
        self.refresh_callback = refresh_callback
        self.assignment_text = CustomInput(hint_text="Assignment", text=self.assignment, required=True,
                                           helper_text_mode="persistent", helper_text="Assignment must not be empty")
        self.course_text = CustomInput(hint_text="Course", text=self.course)
        self.ects_text = CustomInput(hint_text="ECTS", text=self.ects)
        self.grade_perc_text = CustomInput(hint_text="Grade Percentage", text=self.grade_perc,
                                           helper_text_mode="persistent", helper_text="Fractions from 0 to 1")
        self.due_date_text = CustomInput(hint_text="Due Date", text=self.due_date, date_format="yyyy/mm/dd",
                                         validator="date", required=True, helper_text_mode='persistent',
                                         helper_text="Enter a valid date YYYY/MM/DD")
        self.difficulty_text = CustomInput(hint_text="Difficulty", text=self.difficulty, helper_text_mode="persistent",
                                           helper_text="Numbers from 0 to 10")
        self.time_consumption_text = CustomInput(hint_text="Time Consumption", text=self.time_consumption,
                                                 helper_text_mode="persistent", helper_text="Numbers from 0 to 10")
        self.likability_text = CustomInput(hint_text="Likability", text=self.likability, helper_text_mode="persistent",
                                           helper_text="Numbers from 0 to 10")
        self.status_text = CustomInput(hint_text="Status", text=self.status, helper_text_mode="persistent",
                                       helper_text="To do/Done")
        self.grid = MDBoxLayout(orientation="horizontal", size_hint_y=0.05, size_hint_x=1)
        self.cancel = MDFlatButton(text="Cancel")
        self.cancel.bind(on_release=self.close_dialog)
        self.add = MDFlatButton(text="Save changes")
        self.add.bind(on_release=self.save_changes)
        self.remove_button = MDFlatButton(text="REMOVE")
        self.remove_button.bind(on_release=self.confirm_removal)
        self.grid.add_widget(self.remove_button)
        self.change_status_button = MDFlatButton(text="COMPLETED")
        self.change_status_button.bind(on_release=self.set_done)
        self.grid.add_widget(self.change_status_button)
        self.grid.add_widget(self.cancel)
        self.grid.add_widget(self.add)
        self.date_picker_button = MDFloatingActionButton(icon="calendar")
        self.date_picker_button.bind(on_release=self.show_datepicker)
        self.grid.add_widget(self.date_picker_button)
        self.layout = MDBoxLayout(orientation="vertical", size_hint_y=0.80)
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

    def save_changes(self, instance):
        id = self.id
        assignment = self.assignment_text.text
        course = self.course_text.text
        ects = self.ects_text.text
        grade_perc = self.grade_perc_text.text
        due_date = self.due_date_text.text
        difficulty = self.difficulty_text.text
        time_consumption = self.time_consumption_text.text
        likability = self.likability_text.text
        status = self.status_text.text
        if assignment == '' or due_date == '':
            self.show_dialog(title="Error", text='Empty values in required inputs')
        if assignment != '' and due_date != '':
            try:
                self.app.alter_task(id, assignment, due_date, course, ects, grade_perc, difficulty, time_consumption,
                                    likability, status)
                self.refresh_callback()
            except sqlite3.IntegrityError:
                self.show_dialog(title="Error", text='Insufficient data')

    def show_datepicker(self, instance):
        date_picker = CustomDatePicker()
        date_picker.bind(on_save=lambda instance, value, date_range: self.on_date_picker_save(value))
        date_picker.open()

    def on_date_picker_save(self, selected_date):
        selected_date_str = selected_date.strftime("%Y/%m/%d")
        self.due_date_text.text = selected_date_str

    def confirm_removal(self, instance):
        id = self.id
        self.app.remove_task(id)
        self.refresh_callback()
        self.parent.parent.parent.dismiss()

    def set_done(self, instance):
        id = self.id
        self.app.mark_as_completed(id)
        self.refresh_callback()
        self.parent.parent.parent.dismiss()

    # noinspection PyMethodMayBeStatic
    def show_dialog(self, title, text):
        dialog = MDDialog(title=title, text=text, size_hint=(0.4, 0.2))
        dialog.open()

    def close_dialog(self, instance):
        self.parent.parent.parent.dismiss()

    def show_data_table(self):
        self.root.current = "data_table"


# noinspection PyShadowingNames
class AddingDialog(MDBoxLayout):
    def __init__(self, refresh_callback, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.db = Database()
        self.orientation = "vertical"
        self.spacing = "5dp"
        self.size_hint_y = None
        self.height = "700dp"
        self.refresh_callback = refresh_callback
        self.assignment_text = CustomInput(hint_text="Assignment", required=True, helper_text_mode="persistent",
                                           helper_text="Assignment must not be empty")
        self.course_text = CustomInput(hint_text="Course")
        self.ects_text = CustomInput(hint_text="ECTS")
        self.grade_perc_text = CustomInput(hint_text="Grade Percentage", helper_text_mode="persistent",
                                           helper_text="Fractions from 0 to 1")
        self.due_date_text = CustomInput(hint_text="Due Date", date_format="yyyy/mm/dd", validator="date",
                                         required=True, helper_text_mode='persistent',
                                         helper_text="Enter a valid date YYYY/MM/DD")
        self.difficulty_text = CustomInput(hint_text="Difficulty", helper_text_mode="persistent",
                                           helper_text="Numbers from 0 to 10")
        self.time_consumption_text = CustomInput(hint_text="Time Consumption", helper_text_mode="persistent",
                                                 helper_text="Numbers from 0 to 10")
        self.likability_text = CustomInput(hint_text="Likability", helper_text_mode="persistent",
                                           helper_text="Numbers from 0 to 10")
        self.layout = MDBoxLayout(orientation="vertical", size_hint_y=0.80)
        self.layout.add_widget(self.assignment_text)
        self.layout.add_widget(self.course_text)
        self.layout.add_widget(self.ects_text)
        self.layout.add_widget(self.grade_perc_text)
        self.layout.add_widget(self.due_date_text)
        self.layout.add_widget(self.difficulty_text)
        self.layout.add_widget(self.time_consumption_text)
        self.layout.add_widget(self.likability_text)
        self.grid = MDGridLayout(cols=2)
        b1 = MDFlatButton(text="Cancel")
        b1.bind(on_release=self.close_dialog)
        b2 = MDFlatButton(text="Save")
        b2.bind(on_release=self.confirm)
        b3 = MDFloatingActionButton(icon="calendar")
        b3.bind(on_release=self.show_datepicker)
        self.grid.add_widget(b1)
        self.grid.add_widget(b2)
        self.grid.add_widget(b3)
        self.layout.add_widget(self.grid)
        self.add_widget(self.layout)

    def close_dialog(self, instance):
        self.parent.parent.parent.dismiss()

    def confirm(self, instance):
        assignment = self.assignment_text.text
        course = self.course_text.text
        due_date = self.due_date_text.text
        ects = self.ects_text.text
        grade_perc = self.grade_perc_text.text
        difficulty = self.difficulty_text.text
        time_consumption = self.time_consumption_text.text
        likability = self.likability_text.text
        self.db.add_tasks(assignment, due_date, course, ects, grade_perc, difficulty, time_consumption, likability)
        self.refresh_callback()
        self.app.refresh_other_screens()

    def show_datepicker(self, instance):
        date_picker = CustomDatePicker()
        date_picker.bind(on_save=lambda instance, value, date_range: self.on_date_picker_save(value))
        date_picker.open()

    def on_date_picker_save(self, selected_date):
        selected_date_str = selected_date.strftime("%Y/%m/%d")
        self.due_date_text.text = selected_date_str


class WarningDialog(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.spacing = "5dp"
        self.size_hint_y = None
        self.height = "50dp"
        layout = MDBoxLayout(orientation="horizontal")
        b1 = MDFlatButton(text="Cancel")
        b1.bind(on_release=self.close_dialog)
        b2 = MDRaisedButton(text="Close App")
        b2.bind(on_release=self.close)
        layout.add_widget(b1)
        layout.add_widget(b2)
        self.add_widget(layout)

    def close(self, instance):
        self.app.update_theme()
        self.app.stop()

    def close_dialog(self, instance):
        self.parent.parent.parent.dismiss()


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class PreferencesScreen(MDScreen):
    pass


class CustomSlider(MDSlider):
    def __init__(self, **kwargs):
        super(CustomSlider, self).__init__(**kwargs)
        self.thumb_size = dp(24)


# noinspection PyAttributeOutsideInit
class AllTaskView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.app = MDApp.get_running_app()
        self.list = MDList()
        self.scroll = MDScrollView()
        self.layout = MDBoxLayout(orientation="vertical")
        self.grid = MDBoxLayout(orientation="horizontal", size_hint=(1, 0.2), pos_hint={"y": 1}, padding=dp(10),
                                spacing=dp(10))
        self.create_task_widgets()

    def create_task_widgets(self):
        self.scroll.clear_widgets()
        self.list.clear_widgets()
        self.clear_widgets()
        self.tasks = self.db.get_task_list()
        self.app.active_tasks.clear()
        self.layout.clear_widgets()
        self.grid.clear_widgets()
        self.b1 = CustomButton(text="Delete selected", size_hint_x=1)
        self.b1.size_hint_x = 1
        self.b1.bind(on_release=self.delete_selected)
        self.grid.add_widget(self.b1)
        self.b2 = CustomButton(text="Set done", size_hint_x=1)
        self.b2.size_hint_x = 1
        self.b2.bind(on_release=self.set_done)
        self.grid.add_widget(self.b2)
        self.b3 = CustomButton(on_release=self.select_all, text="Select all", size_hint_x=1)
        self.b3.size_hint_x = 1
        self.grid.add_widget(self.b3)
        for task in self.tasks:
            button = ListItemWithCheckbox(IconLeftWidget(id=task[0], theme_text_color="Custom", icon="menu",
                                                         icon_color=self.app.primary_text_color,
                                                         on_release=self.more_info_dialog), id=task[0], text=task[1],
                                          secondary_text=task[2], tertiary_text=task[5], theme_text_color='Custom',
                                          text_color=self.app.primary_text_color, secondary_theme_text_color='Custom',
                                          secondary_text_color=self.app.secondary_text_color,
                                          tertiary_theme_text_color='Custom',
                                          tertiary_text_color=self.app.secondary_text_color, bg_color=self.app.bg_color)
            button.bind(on_release=self.app.print_id)
            button.divider = "Full"
            button.divider_color = self.app.header_color
            self.list.add_widget(button)
        self.scroll.add_widget(self.list)
        self.layout.add_widget(self.grid)
        self.layout.add_widget(self.scroll)
        self.add_widget(self.layout)

    def more_info_dialog(self, instance):
        info = self.db.get_more_info(instance.id)
        dialog = MDDialog(title="More info", type="custom",
                          content_cls=MoreInfoDialog(info[0], info[1], info[2], info[3], info[4]))
        dialog.open()

    def delete_selected(self, instance):
        for ids in self.app.active_tasks:
            self.db.remove_task(ids)
        self.app.refresh_tasks_in_menu()

    def set_done(self, instance):
        for ids in self.app.active_tasks:
            self.db.mark_as_completed(ids)
        self.app.refresh_tasks_in_menu()

    def select_all(self, instance):
        for items in self.list.children:
            if items.ids.check.active:
                items.ids.check.active = False
            else:
                items.ids.check.active = True


class MoreInfoDialog(MDBoxLayout):
    def __init__(self, ects, grade_perc, difficulty, time_consumption, likability, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "5dp"
        self.size_hint_y = None
        self.height = "250dp"
        self.ects = ects
        self.grade_perc = grade_perc
        self.difficulty = difficulty
        self.time_consumption = time_consumption
        self.likability = likability
        self.list = MDList()
        self.create_list()

    def create_list(self):
        items = [OneLineListItem(text=f"ECTS: {self.ects}"),
                 OneLineListItem(text=f"Grade percentage: {self.grade_perc}"),
                 OneLineListItem(text=f"Difficulty: {self.difficulty}"),
                 OneLineListItem(text=f"Time consumption: {self.time_consumption}"),
                 OneLineListItem(text=f"Likeability: {self.likability}")]
        for item in items:
            self.list.add_widget(item)
        self.add_widget(self.list)


# noinspection PyMethodMayBeStatic,PyAttributeOutsideInit
class BaseScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.db = Database()
        self.scroll = MDScrollView()
        self.checkbox_state = False
        self.create_screen()

    def create_screen(self):
        self.clear_widgets()
        self.create_table()
        self.add_widget(self.scroll)
        self.layout = MDBoxLayout(orientation="horizontal", size_hint=(1, 0.2), padding=dp(10), spacing=dp(10))
        self.b1 = CustomButton(text='Remove selected')
        self.b1.bind(on_release=self.delete_selected)
        self.layout.add_widget(self.b1)
        self.b2 = CustomButton(text="Done")
        self.b2.bind(on_release=self.set_done)
        self.layout.add_widget(self.b2)
        self.add_widget(self.layout)

    def create_table(self):
        self.scroll.clear_widgets()
        self.table_get_rows = self.get_table_data()
        self.data_table = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[
                ("ID", dp(20)),
                ("Assignment", dp(50), self.sort_on_assignment),
                ("Course", dp(40), self.sort_on_course),
                ("ECTS", dp(15), self.sort_on_ects),
                ("%", dp(15), self.sort_on_perc),
                ("Due Date", dp(20), self.sort_on_date),
                ("D", dp(20), self.sort_on_difficulty),
                ("T", dp(20), self.sort_on_time),
                ("L", dp(20), self.sort_on_like),
                ("I", dp(20), self.sort_on_importance)
            ],
            row_data=self.table_get_rows,
            elevation=2,
            sorted_on="Course",
            rows_num=10)
        self.data_table.bind(on_row_press=self.on_row_press)
        self.data_table.bind(on_check_press=self.on_check_press)
        self.scroll.add_widget(self.data_table)

    def on_row_press(self, table, row):
        if not self.checkbox_state:
            row_num = int(row.index / len(table.column_data))
            row_data = table.row_data[row_num]
            dialog = MDDialog(title="Update task", type="custom",
                              content_cls=UpdateDialog(row_data[0], row_data[1], row_data[2], str(row_data[3]),
                                                       str(row_data[4]), row_data[5], str(row_data[6]),
                                                       str(row_data[7]), str(row_data[8]), self.get_dialog_status(),
                                                       self.create_table))
            dialog.open()
        self.checkbox_state = False

    def on_check_press(self, instance_table, current_row):
        self.checkbox_state = True
        if current_row[0] not in self.app.active_tasks:
            self.app.active_tasks.add(current_row[0])
        else:
            self.app.active_tasks.discard(current_row[0])

    def sort_on_assignment(self, data):
        indexes, sorted_data = zip(*sorted(enumerate(data), key=lambda item: item[1][1]))
        return indexes, sorted_data

    def sort_on_course(self, data):
        indexes, sorted_data = zip(*sorted(enumerate(data), key=lambda item: item[1][2]))
        return indexes, sorted_data

    def sort_on_ects(self, data):
        indexes, sorted_data = zip(*sorted(enumerate(data), key=lambda item: item[1][3]))
        return indexes, sorted_data

    def sort_on_perc(self, data):
        indexes, sorted_data = zip(*sorted(enumerate(data), key=lambda item: float(item[-1][4])))
        return indexes, sorted_data

    def sort_on_date(self, data):
        indexes, sorted_data = zip(*sorted(enumerate(data), key=lambda item: item[1][5]))
        return indexes, sorted_data

    def sort_on_difficulty(self, data):
        indexes, sorted_data = zip(*sorted(enumerate(data), key=lambda item: item[1][6]))
        return indexes, sorted_data

    def sort_on_time(self, data):
        indexes, sorted_data = zip(*sorted(enumerate(data), key=lambda item: item[1][7]))
        return indexes, sorted_data

    def sort_on_like(self, data):
        indexes, sorted_data = zip(*sorted(enumerate(data), key=lambda item: item[1][8]))
        return indexes, sorted_data

    def sort_on_importance(self, data):
        indexes, sorted_data = zip(*sorted(enumerate(data), key=lambda item: item[1][9]))
        return indexes, sorted_data

    def get_table_data(self):
        raise NotImplementedError("Subclasses must implement get_table_data method")

    def get_dialog_status(self):
        raise NotImplementedError("Subclasses must implement get_dialog_status method")

    def delete_selected(self, instance):
        for ids in self.app.active_tasks:
            self.db.remove_task(ids)
        self.app.refresh_tasks_in_menu()

    def set_done(self, instance):
        for ids in self.app.active_tasks:
            self.db.mark_as_completed(ids)
        self.app.refresh_tasks_in_menu()


class CustomSort(BaseScreen):
    def get_table_data(self):
        return self.db.get_task_list()

    def get_dialog_status(self):
        return 'To do'


class Archive(BaseScreen):
    def get_table_data(self):
        return self.db.get_archive()

    def get_dialog_status(self):
        return 'Done'


class Settings(MDScreen):
    pass


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    pass


class ListItemWithCheckbox(ThreeLineAvatarIconListItem, BaseListItem):
    def get_checkbox(self):
        return self.ids.right_checkbox


class TestItem(ThreeLineAvatarIconListItem, BaseListItem):
    pass


class CustomButton(MDRectangleFlatButton):
    pass


class CustomCheckbox(MDCheckbox):
    pass


class CustomInput(MDTextField):
    pass


class CustomDatePicker(MDDatePicker):
    pass


class ItemConfirm(OneLineAvatarIconListItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def set_icon(self, instance_check):
        self.app.chosen_theme = self.text
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False


if __name__ == '__main__':
    Tasks().run()
