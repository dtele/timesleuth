import time
from ctypes import byref, c_ulong, create_unicode_buffer, windll
from typing import Any, Callable, Tuple

from psutil import Process, AccessDenied


class ProcessDetails:
    def __init__(self, pid, exe_name, title, exe_path):
        self.pid = pid
        self.exe_name = exe_name
        self.title = title
        self.exe_path = exe_path
        self.process_start = None
        self.process_end = None
        self.runtime = None

    def __eq__(self, other):
        unique_self = {k: v for k, v in self.__dict__.items() if k not in ['pid', 'process_start', 'process_end', 'runtime']}
        unique_other = {k: v for k, v in other.__dict__.items() if k not in ['pid', 'process_start', 'process_end', 'runtime']}

        return unique_self == unique_other

    def __getitem__(self, item):
        return getattr(self, item)

    def __repr__(self):
        return f'<ProcessDetails pid={self.pid} exe_name=_{self.exe_name}_ title=_{self.title}_ runtime={self.runtime}>'

    def isnone(self):
        return self.pid == 0


class Listener:
    # TODO: Add stop method
    def __init__(self, callback_function: Callable[[ProcessDetails], Any], delay: int = 1_000):
        self.user32 = windll.user32
        self.callback_function = callback_function
        self.delay = delay / 1_000

    def get_window(self) -> ProcessDetails:
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
            pass

    def start(self) -> None:
        while True:
            self.callback_function(self.get_window())
            time.sleep(self.delay)
