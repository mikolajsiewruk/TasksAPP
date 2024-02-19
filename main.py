import mysql.connector
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput

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

    def build(self):
        self.connection_to_db = mysql.connector.connect(
            host='sql11.freemysqlhosting.net',
            user='sql11683696',
            password='I2mbJRFBxu',
            port=3306,
            database='sql11683696'
        )

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
        sql_statement1=f'''select * from Uzytkownicy where nickname='{username}' and password='{password}';'''
        self.cursor.execute(sql_statement1)
        users=self.cursor.fetchone()
        if users:
            print("wow")
            self.manager.current = "menu" # zrobic menu aplikacji
        else:
            print("not wow")

    def show_tables(self):
        q = '''Select * from Uzytkownicy'''
        self.cursor.execute(q)
        res = self.cursor.fetchall()
        print(res)


class MenuWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass




if __name__ == '__main__':
    TasksApp().run()