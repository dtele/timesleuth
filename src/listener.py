import time
from ctypes import byref, c_ulong, create_unicode_buffer, windll
from typing import Any, Callable, Tuple

from psutil import Process


class Listener:
    # TODO: Add stop method
    def __init__(self, callback_function: Callable[[Tuple], Any], delay: int = 1_000):
        self.user32 = windll.user32
        self.callback_function = callback_function
        self.delay = delay / 1_000

    def get_window(self) -> Tuple[int, str, str, str]:
        hwnd = self.user32.GetForegroundWindow()
        pid = c_ulong()
        self.user32.GetWindowThreadProcessId(hwnd, byref(pid))

        process = Process(pid.value)

        buff_size = self.user32.GetWindowTextLengthW(hwnd) + 1
        title = create_unicode_buffer(buff_size)
        self.user32.GetWindowTextW(hwnd, title, buff_size)

        return pid.value, process.name(), ''.join(map(str, title))[:-1], process.exe()

    def start(self) -> None:
        while True:
            self.callback_function(self.get_window())
            time.sleep(self.delay)
