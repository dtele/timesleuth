import os
import subprocess

from listener import Listener


class Icon:
    def __init__(self):
        pass

    @staticmethod
    def create(path):
        path = '"' + path + '"'
        process_name = path[path.rfind('\\') + 1:-1].replace('.exe', '.bmp')
        save_path = os.path.join(os.getcwd(), 'icons', process_name)

        if not os.path.isdir(save_path):
            subprocess.call(['powershell', '-executionpolicy', 'bypass', './icons.ps1', '-ExePath', path, '-SavePath', save_path])


class Tracker:
    def __init__(self):
        self.listen = Listener(callback_function=self.on_activity, delay=300)
        self.listen.start()
        self.icon_maker = Icon()

    def on_activity(self, process_details):
        Icon.create(process_details[3])


try:
    os.mkdir(os.path.join(os.getcwd(), 'icons'))
except FileExistsError:
    pass

tracker = Tracker()
