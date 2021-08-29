import sqlite3

from datetime import datetime, timedelta


class Reader:
    def __init__(self, db_name):
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()

    @staticmethod
    def get_runtime(data: list):
        distinct = set(map(lambda k: k[0], data))

        for elem in distinct:
            total = timedelta()
            for i in data:
                if i[0] == elem:
                    total += datetime.strptime(i[2], '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(i[1],
                                                                                                 '%Y-%m-%d %H:%M:%S.%f')

            yield elem, total

    def get_info(self, date):
        self.cursor.execute('select exe_name, process_start, process_end from activity where process_start > (?)', (date,))
        output = [i for i in self.cursor.fetchall()]
        f_output = list(self.get_runtime(output))
        f_output.sort(key=lambda x: x[1], reverse=True)
        if len(f_output) == 0:
            print('No Data available.')

        else:
            print(f_output)

        self.db.commit()
