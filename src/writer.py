import sqlite3

from listener import ProcessDetails
from tracker import Tracker


class Writer:
    """
    A class to create a database and input process details.
    """
    def __init__(self, db_name: str):
        """
        :param db_name: relative path of database
        """
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()

        try:
            self.cursor.execute('create table activity(title varchar(256), exe_path varchar(512), process_start datetime, process_end datetime)')
        except sqlite3.OperationalError:
            pass

    def write(self, process_details: ProcessDetails) -> None:
        """
        Inputs process details in the table.
        
        :param process_details: ProcessDetails oject of active process
        """
        vals = (process_details.title,
                process_details.exe_path,
                process_details.process_start,
                process_details.process_end)
        self.cursor.execute('insert into activity(title, exe_path, process_start, process_end) values (?, ?, ?, ?)', vals)
        self.db.commit()
