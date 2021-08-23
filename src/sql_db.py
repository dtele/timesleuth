import mysql.connector

from process_listener import ProcessDetails
from tracker import Tracker


class SQL:
    def __init__(self, db_name: str, host: str, user: str, passwd: str):
        try:
            self.db = mysql.connector.connect(host=host, user=user, passwd=passwd)
            self.dbcursor = self.db.cursor()
            self.dbcursor.execute(f'create database {db_name}')
        except mysql.connector.errors.DatabaseError:
            pass

        self.db_main = mysql.connector.connect(host=host, user=user, passwd=passwd, database=db_name)
        self.sql = self.db_main.cursor()

    def write(self, process_details: ProcessDetails):
        insert_cmd = 'insert into activity(pid, title, exe_name, process_start, process_end, runtime) values(%s, %s, %s, %s, %s, %s)'
        vals = [(process_details.pid,
                 process_details.title,
                 process_details.exe_name,
                 process_details.process_start,
                 process_details.process_end,
                 process_details.runtime)]

        try:
            self.sql.execute('create table activity(pid int, title varchar(256), exe_name varchar(256), process_start datetime, process_end datetime, runtime varchar(32))')
            self.sql.executemany(insert_cmd, vals)
        except mysql.connector.errors.ProgrammingError:
            self.sql.executemany(insert_cmd, vals)

        self.db_main.commit()


db_manager = SQL(db_name='activity_tracker', host='localhost', user='root', passwd='heskell')
tracker = Tracker(callback_function=db_manager.write)
