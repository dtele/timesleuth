import pandas as pd
import sqlite3

from datetime import datetime
from typing import Tuple

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

    def read_rows(self, date: datetime.date) -> List[ProcessDetails]:
        """
        Reads data from the database.

        :param date: lower range of timeframe to read entries from
        :returns: pandas dataframe object of data converted from sql table
        """
        self.cursor.execute('select title, exe_path, process_start, process_end from activity where process_start > (?)', (date,))
        output = [Reader.to_process_details(i) for i in self.cursor.fetchall()]

        self.db.commit()

        output_dir={}
        for i in output:
            if i.exe_name not in output_dir:
                output_dir[i.exe_name]=i.runtime
            else:
                output_dir[i.exe_name]+=i.runtime
        
        data=[[i.exe_name[:-4],
               i.runtime.total_seconds(),
               output_dir[i.exe_name].total_seconds()] for i in output]
        
        if max(data,key=lambda i:i[1])[1] > 3600:
            data=[[i,j,k/60] for i,j,k in data]

        df=pd.DataFrame(data,columns=['Processes','Runtime','Total_time'])
        
        return df
