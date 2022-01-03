import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import pyqtSignal, QThread

from qtd_gui import Ui_Form
from listener import Listener


class StartToggle(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.enabled = True
        self.listener = Listener(print, 10)

    def __del__(self):
        self.wait()

    def run(self):
        while self.enabled:
            # add sql Writer stuff here
            self.listener.listen()
            time.sleep(self.listener.delay / 1_000)

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
