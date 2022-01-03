from ctypes import byref, c_ulong, create_unicode_buffer, windll
from datetime import datetime
from typing import Any, Callable

from psutil import Process, AccessDenied


class ProcessDetails:
    """
    A class to represent a process.
    """
    def __init__(self, pid: int = 0, exe_name: str = '', title: str = '', exe_path: str = ''):
        """
        :param pid: process id
        :param exe_name: executable name
        :param title: title of window
        :param exe_path: absolute path of executable
        """
        self.pid = pid
        self.exe_name = exe_name
        self.title = title
        self.exe_path = exe_path
        self.process_start = None
        self.process_end = None
        self.runtime = None

    def __eq__(self, other) -> bool:
        """
        Checks if two ProcessDetails objects are the same.

        :param other: the other object
        :returns: boolean value of the check
        """
        return (self.title, self.exe_path) == (other.title, other.exe_path)

    def __repr__(self) -> str:
        """
        Represents self as string for debugging.

        :returns: string representation
        """
        return f'<ProcessDetails pid={self.pid} exe_name=_{self.exe_name}_ title=_{self.title}_>'

    def isnone(self) -> bool:
        """
        Checks if self is empty or invalid (PID 0 is reserved for System Idle Process).

        :returns: boolean value of the check
        """
        return self.pid == 0


class Tracker:
    """
    A class to track time spent on processes.
    """
    def __init__(self, callback_function: Callable[[ProcessDetails], Any] = print):
        """
        :param callback_function: function to be called when process is switched
        """
        self.user32 = windll.user32

        self.callback_function = callback_function

        self.process_details_prev = ProcessDetails()
        self.process_start = self.process_end = datetime.now()

    def get_window(self) -> ProcessDetails:
        """
        Gets process id, executable name, window title and executable path of the currently active process.

        :returns: ProcessDetails object of the active process
        """
        try:
            hwnd = self.user32.GetForegroundWindow()
            pid = c_ulong()
            self.user32.GetWindowThreadProcessId(hwnd, byref(pid))

            process = Process(pid.value)

            buff_size = self.user32.GetWindowTextLengthW(hwnd) + 1
            title = create_unicode_buffer(buff_size)
            self.user32.GetWindowTextW(hwnd, title, buff_size)

            return ProcessDetails(pid.value, process.name(), ''.join(map(str, title))[:-1], process.exe())
        except AccessDenied:
            return ProcessDetails()

    def check_window(self, process_details: ProcessDetails) -> None:
        """
        Checks if the active process is the same as the one in last tick.
        Populates process_start and process_end for process_details_prev and calls the callback function if not.

        :param process_details: ProcessDetails object of the current active process
        """
        try:
            if not process_details.isnone():
                if not self.process_details_prev.isnone() and self.process_details_prev != process_details:

                    self.process_end = datetime.now()
                    self.process_details_prev.process_end, self.process_details_prev.process_start = self.process_end, self.process_start
                    self.process_details_prev.runtime = self.process_end - self.process_start
                    self.process_start = datetime.now()

                    self.callback_function(self.process_details_prev)

                self.process_details_prev = process_details
        except AttributeError:
            self.process_start = datetime.now()
