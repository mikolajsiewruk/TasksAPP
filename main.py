import mysql.connector
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from  kivy.uix.popup import Popup

class TasksApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connection_to_db = mysql.connector.connect(
            host='sql11.freemysqlhosting.net',
            user='sql11683696',
            password='I2mbJRFBxu',
            port=3306,
            database='sql11683696'
        )
        self.cursor = self.connection_to_db.cursor()
        self.userID= None
    def build(self):
        self.connection_to_db = mysql.connector.connect(
            host='sql11.freemysqlhosting.net',
            user='sql11683696',
            password='I2mbJRFBxu',
            port=3306,
            database='sql11683696'
        )
    def show_error(self, message):
        content = Label(text=message)
        popup = Popup(title="Error", content=content, size_hint=(None, None), size=(400, 200))
        popup.open()
    def on_stop(self):
        self.cursor.close()
        self.connection_to_db.close()
class LoginWindow(Screen,TasksApp):
    def __init__(self, **kwargs):
        super(LoginWindow, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.cursor = self.app.cursor
    def login(self):
        username=self.ids.username.text
        password=self.ids.password.text
        sql_statement1=f'''select * from Users where nickname='{username}' and password='{password}';'''
        self.cursor.execute(sql_statement1)
        users=self.cursor.fetchone()
        if users:
            self.app.userID = users[0]
            self.manager.get_screen("menu").on_preferences_set(self.app.userID)
            self.manager.current = "menu"
        else:
            error_message='Invalid credentials'
            self.app.show_error(error_message)
    def registration_form(self):
        self.manager.current="registration"
class MenuWindow(Screen):
    def __init__(self,**kwargs):
        super(MenuWindow,self).__init__(**kwargs)
        self.app=App.get_running_app()
        self.cursor=self.app.cursor
        self.userID=self.app.userID
    def on_preferences_set(self, user_id):
        self.userID = user_id
    def printid(self):
        print(self.userID)
class Registration(Screen,TasksApp):
    def __init__(self, **kwargs):
        super(Registration, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.cursor = self.app.cursor
    def register(self):
        nickname=self.ids.nickname.text
        password=self.ids.passw.text
        name=self.ids.name.text
        surname=self.ids.surname.text
        uni=self.ids.university.text
        parameters=(nickname,password,name,surname,uni,)
        sql_statement1 = '''Insert Into Users(nickname,password,Name,Surname,University) Values(%s,%s,%s,%s,%s)'''
        try:
            self.cursor.execute(sql_statement1,parameters)
            self.connection_to_db.commit()
            sql_statement2=f'''Select * from Users where nickname='{nickname}';'''
            self.cursor.execute(sql_statement2)
            results=self.cursor.fetchone()
            self.app.userID = results[0]
            self.manager.current="setpreferences"
        except mysql.connector.IntegrityError:
            error_message = 'Nickname taken'
            self.app.show_error(error_message)
class SetPreferences(Screen):
    def __init__(self, **kwargs):
        super(SetPreferences, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.connection_to_db=self.app.connection_to_db
        self.cursor = self.app.cursor
    def setpreferences(self):
        user_ID=self.app.userID
        parameters=(user_ID,self.ids.ects.text,self.ids.duedate.text,self.ids.gradepercentage.text,self.ids.difficulty.text,self.ids.time_consumption.text,self.ids.likability.text,self.ids.importance.text,self.ids.sudenness.text,)
        sql_statement='''Insert into Preferences(UserID,Ects,due_date,grade_percentage,difficulty,time_consumption,likability,importance,sudenness) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) '''
        self.cursor.execute(sql_statement,parameters)
        self.connection_to_db.commit()
        sql_statement1=f'''select * from Users where id={user_ID}'''
        self.cursor.execute(sql_statement1)
        results=self.cursor.fetchone()
        if results:
            self.app.userID=results[0]
            self.manager.get_screen("menu").on_preferences_set(self.app.userID)
            self.manager.current="menu"
class WindowManager(ScreenManager):
    pass




if __name__ == '__main__':
    TasksApp().run()