import os
import subprocess
from datetime import datetime, timedelta
from typing import Any, Callable

from process_listener import Listener, ProcessDetails


class Icon:
    def __init__(self):
        try:
            os.mkdir(os.path.join(os.getcwd(), 'icons'))
        except FileExistsError:
            pass

    @staticmethod
    def create(exe_path):
        try:
            exe_path = '"' + exe_path + '"'
            process_name = exe_path[exe_path.rfind('\\') + 1:-1].replace('.exe', '.bmp')
            save_path = os.path.join(os.getcwd(), 'icons', process_name)

            if not os.path.isdir(os.path.join(os.getcwd(), 'icons', process_name)):
                subprocess.call(['powershell', '-executionpolicy', 'bypass', './icons.ps1', '-ExePath', exe_path, '-SavePath', save_path])
        except AttributeError:
            pass


class Tracker:
    def __init__(self, callback_function: Callable[[ProcessDetails], Any] = print):
        self.callback_function = callback_function
        self.icon_manager = Icon()

        self.process_details_prev = ProcessDetails(0, '', '', '')
        self.process_start = datetime.now()

        self.listener = Listener(callback_function=self.on_activity, delay=10)
        self.listener.start()

    def on_activity(self, process_details: ProcessDetails):
        try:
            if not process_details.isnone():
                self.icon_manager.create(process_details.exe_path)

                if not self.process_details_prev.isnone():
                    if process_details != self.process_details_prev:
                        self.process_end = datetime.now()
                        self.process_details_prev.process_end, self.process_details_prev.process_start= self.process_end, self.process_start
                        self.process_details_prev.runtime = self.process_end - self.process_start
                        self.process_start = datetime.now()

                        self.callback_function(self.process_details_prev)

                self.process_details_prev = process_details
        except AttributeError:
            self.process_start = datetime.now()
