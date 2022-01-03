import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import pyqtSignal, QThread

from qtd_gui import Ui_Form
from tracker import Tracker
from sql_commands import Writer


class StartToggle(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.enabled = True
        self.delay = 10
        # change file name later
        self.tracker = Tracker(callback_function=Writer(r'haskelldudes-main/src/dbname.sqlite').write)

    def __del__(self):
        self.wait()

    def run(self):
        while self.enabled:
            self.tracker.check_window(self.tracker.get_window())
            time.sleep(self.delay / 1_000)

    def stop(self):
        self.enabled = False

    def reset(self):
        self.enabled = True


class MainWindow(QWidget):
    stop_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.started = False
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.btnstart.clicked.connect(self.on_click)

        self.thread = StartToggle()
        self.stop_signal.connect(self.thread.stop)

    def on_click(self):
        self.started = not self.started
        if self.started:
            self.ui.btnstart.setText('Stop')
            self.thread.reset()
            self.thread.start()
        else:
            self.ui.btnstart.setText('Start')
            self.stop_signal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
