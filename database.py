import sqlite3

class Database():
    def __init__(self):
        self.connection_to_db=sqlite3.connect("app1.db")
        self.cursor=self.connection_to_db.cursor()
        self.create_tables()
    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Tasks(IdT INTEGER NOT NULL CONSTRAINT Tasks_pk PRIMARY KEY AUTOINCREMENT, Assignment TEXT NOT NULL, Course TEXT, ECTS INTEGER, Due_date TEXT NOT NULL, Grade_percentage REAL, Difficulty INTEGER, Time_consumption INTEGER, Likability INTEGER, Status TEXT default 'To do');''')
        self.connection_to_db.commit()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Preferences(ECTS INTEGER default 1,Due_date INTEGER default 1, Grade_percentage INTEGER default 1, Difficulty INTEGER default 1,Time_consumption INTEGER default 1,Likability INTEGER default 1,Importance INTEGER default 1) ''')
        self.connection_to_db.commit()
        if not self.cursor.execute("SELECT * FROM Preferences").fetchone():
            self.cursor.execute("INSERT INTO Preferences(ECTS,Due_date,Grade_percentage,Difficulty,Time_consumption,Likability,Importance) VALUES (1,1,1,1,1,1,1)")
            self.connection_to_db.commit()
        if not self.cursor.execute("SELECT * FROM Tasks").fetchall():
            self.cursor.execute("INSERT INTO Tasks(Assignment,Course,ECTS,Due_date,Grade_percentage,Difficulty,Time_consumption,Likability,Status)VALUES ('Sample task','Sample course',2,'2024/01/01',0.5,1,1,1,'To do')")
            self.connection_to_db.commit()
    def add_tasks(self,assignment,duedate,course=None,ects=None,gradeperc=None,diff=None,time=None,like=None):
        sql=f"INSERT INTO Tasks(Assignment,Course,ECTS,Due_date,Grade_percentage,Difficulty,Time_consumption,Likability) VALUES('{assignment}','{course}','{ects}','{duedate}','{gradeperc}','{diff}','{time}','{like}');"
        parameters=(assignment,course,ects,duedate,gradeperc,diff,time,like)
        self.cursor.execute(sql)
        self.connection_to_db.commit()
    def get_tasks(self):
        weights = self.cursor.execute("SELECT * FROM Preferences").fetchone()
        user_preferences = f'ECTS*{weights[0]} DESC ,Due_date * {weights[1]} DESC,Grade_percentage * {weights[2]} DESC ,Difficulty *{weights[3]} DESC,Time_consumption * {weights[4]} DESC,Likability *{weights[5]} DESC,Importance * {weights[6]} DESC'
        rows = self.cursor.execute(f"SELECT Assignment, Course, Status, Due_date, ECTS*Grade_percentage AS Importance FROM Tasks ORDER BY {user_preferences}").fetchall()
        row_data = [(str(row[0]), row[1], row[2], row[3],) for row in rows]
        return row_data
    def get_5shortest(self):
        sql="SELECT Assignment,Course,Due_date,IdT FROM Tasks WHERE status='To do' ORDER BY Due_date  LIMIT 5"
        results=self.cursor.execute(sql).fetchall()
        return results
    def get_5important(self):
        sql = "SELECT Assignment,ECTS*Grade_percentage AS Importance,Due_date,IdT FROM Tasks WHERE status='To do' ORDER BY Importance DESC LIMIT 5"
        results = self.cursor.execute(sql).fetchall()
        return results
    def get_attributes(self,id):
        sql=f'SELECT * FROM TASKS WHERE IdT={id}'
        return self.cursor.execute(sql).fetchone()
    def alter_task(self,id,assignment,duedate,course,ects,gradeperc,diff,time,like,status):
        sql=f'''UPDATE Tasks SET Assignment='{assignment}',Course='{course}', ECTS='{ects}', Grade_percentage='{gradeperc}', Due_date='{duedate}', Difficulty='{diff}', Time_consumption='{time}', Likability='{like}', Status='{status}' WHERE IdT='{id}';'''
        self.cursor.execute(sql)
        self.connection_to_db.commit()
    def remove_task(self,id):
        sql=f"DELETE FROM Tasks WHERE IdT='{id}';"
        self.cursor.execute(sql)
        self.connection_to_db.commit()
    def mark_as_completed(self,id):
        sql=f"UPDATE Tasks SET Status ='Done' WHERE IdT='{id}'"
        self.cursor.execute(sql)
        self.connection_to_db.commit()
    def get_preference_value(self,column):
        sql=f'''SELECT {column} FROM Preferences'''
        self.cursor.execute(sql)
        result=self.cursor.fetchone()
        return result[0]
    def update_preferences_values(self,ects,duedate,gradeperc,difficulty,time,like,importance):
        sql=f'''UPDATE Preferences SET ECTS='{ects}',Due_date='{duedate}', Grade_percentage='{gradeperc}',Difficulty='{difficulty}', Time_consumption='{time}', Likability='{like}',Importance='{importance}'; '''
        self.cursor.execute(sql)
        self.connection_to_db.commit()
    def comm(self,instance):
        print(self.cursor.execute("Select * from Tasks").fetchall())
    def get_task_list(self):
        weights = self.cursor.execute("SELECT * FROM Preferences").fetchone()
        user_preferences = f'ECTS*{weights[0]} DESC ,Due_date * {weights[1]} DESC,Grade_percentage * {weights[2]} DESC ,Difficulty *{weights[3]} DESC,Time_consumption * {weights[4]} DESC,Likability *{weights[5]} DESC,Importance * {weights[6]} DESC'
        rows = self.cursor.execute(f"SELECT IdT, Assignment, Course, ECTS, Grade_percentage, Due_date, Difficulty, Time_consumption, Likability, ECTS*Grade_percentage AS Importance FROM Tasks WHERE Status = 'To do' ORDER BY {user_preferences}").fetchall()
        row_data = [(str(row[0]), row[1], row[2], row[3],row[4],row[5],row[6],row[7],row[8],row[9]) for row in rows]
        return row_data
    def get_more_info(self,id):
        sql=f'''SELECT ECTS, Grade_percentage, Difficulty, Time_consumption, Likability FROM Tasks WHERE IdT='{id}'; '''
        info = self.cursor.execute(sql).fetchone()
        return info