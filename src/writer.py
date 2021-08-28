import sqlite3

from listener import ProcessDetails


class Writer:
    def __init__(self, db_name: str):
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()

        try:
            self.cursor.execute('create table activity(pid int, title varchar(256), exe_name varchar(256), process_start datetime(6), process_end datetime(6))')
        except sqlite3.OperationalError:
            pass

    def write(self, process_details: ProcessDetails) -> None:
        vals = (process_details.pid,
                process_details.title,
                process_details.exe_name,
                process_details.process_start,
                process_details.process_end)

        self.cursor.execute('insert into activity(pid, title, exe_name, process_start, process_end) values (?, ?, ?, ?, ?)', vals)
        self.db.commit()
