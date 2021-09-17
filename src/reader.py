import sqlite3

from datetime import datetime,timedelta
from typing import List, Tuple

from listener import ProcessDetails


class Reader:
    """
    A class to read data from the database.
    """
    def __init__(self, db_name):
        """
        :param db_name: relative path of database
        """
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()

    @staticmethod
    def to_process_details(row: Tuple[str, str, str, str]) -> ProcessDetails:
        """
        Converts SQL entries to ProcessDetails objects.

        :param row: individual row read from sql table
        :returns: converted ProcessDetails object
        """
        process = ProcessDetails(title=row[0], exe_name=row[1][row[1].rfind('\\') + 1:], exe_path=row[1])
        process.process_start = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f')
        process.process_end = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S.%f')
        process.runtime = process.process_end - process.process_start

        return process

    @staticmethod
    def get_runtime(data: List[ProcessDetails]) -> List[Tuple[str, timedelta]]:
        """
        Calculates total runtime of each unique process.

        :param data: list of ProcessDetails objects converted from sql entries
        :returns: list of unique processes and their total runtime
        """
        process_runtimes = {}

        for elem in data:
            if elem.exe_path in process_runtimes:
                process_runtimes[elem.exe_path] += elem.runtime
            else:
                process_runtimes[elem.exe_path] = elem.runtime

        return sorted(process_runtimes.items(), key=lambda i: i[1], reverse=True)

    def read_rows(self, date: datetime.date) -> List[ProcessDetails]:
        """
        Reads data from the database.

        :param date: lower range of timeframe to read entries from
        :returns: list of ProcessDetails objects converted from sql table
        """
        self.cursor.execute('select title, exe_path, process_start, process_end from activity where process_start > (?)', (date,))
        output = [Reader.to_process_details(i) for i in self.cursor.fetchall()]

        self.db.commit()

        return output
