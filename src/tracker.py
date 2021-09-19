import os
import subprocess
from datetime import datetime
from typing import Any, Callable

from listener import Listener, ProcessDetails


class Icon:
    """
    A class to manage icons.
    """
    def __init__(self):
        try:
            os.mkdir(os.path.join(os.getcwd(), 'icons'))
        except FileExistsError:
            pass

    @staticmethod
    def create(exe_path) -> None:
        """
        Calls a PowerShell script which extracts icon from the specified executable and saves it as bitmap.

        :param exe_path: path of executable
        """
        try:
            exe_path = '"' + exe_path + '"'
            process_name = exe_path[exe_path.rfind('\\') + 1:-1].replace('.exe', '.bmp')
            save_path = os.path.join(os.getcwd(), 'icons', process_name)

            if not os.path.isdir(save_path):
                subprocess.call(['powershell', '-executionpolicy', 'bypass', './icons.ps1', '-ExePath', exe_path, '-SavePath', save_path])
        except AttributeError:
            pass


class Tracker:
    """
    A class to track time spent on processes.
    """
    def __init__(self, callback_function: Callable[[ProcessDetails], Any] = print, delay: int = 1_000):
        """
        :param callback_function: function to be called when process is switched
        :param delay: delay between calls to get process in milliseconds
        """
        self.callback_function = callback_function
        self.icon_manager = Icon()

        self.process_details_prev = ProcessDetails()
        self.process_start = self.process_end = datetime.now()

        self.process_listener = Listener(callback_function=self.check_window, delay=delay)
        self.process_listener.start()

    def check_window(self, process_details: ProcessDetails):
        """
        Checks if the active process is the same as the one in last tick.
        Populates process_start and process_end for process_details_prev and calls the callback function if not.

        :param process_details: ProcessDetails object of the current active process
        """
        try:
            if not process_details.isnone():
                if not self.process_details_prev.isnone() and self.process_details_prev != process_details:
                    self.icon_manager.create(process_details.exe_path)

                    self.process_end = datetime.now()
                    self.process_details_prev.process_end, self.process_details_prev.process_start = self.process_end, self.process_start
                    self.process_details_prev.runtime = self.process_end - self.process_start
                    self.process_start = datetime.now()

                    self.callback_function(self.process_details_prev)

                self.process_details_prev = process_details
        except AttributeError:
            self.process_start = datetime.now()
