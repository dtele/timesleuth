import sys
import time

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import QThread, pyqtSignal

from qtd_gui import Ui_MainWindow
from sql_commands import Writer
from tracker import Tracker


class StartToggle(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.enabled = True
        self.delay = 10
        # change file name later
        self.writer = Writer(r'dbname.sqlite')
        self.tracker = Tracker(callback_function=self.writer.write)

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
        self.ui = Ui_MainWindow()
        self.Form = QMainWindow()
        self.ui.setupUi(self.Form)

        self.fig = plt.figure()
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.ui.graph_layout.addWidget(self.canvas)

        self.ui.toggle_button.clicked.connect(self.on_click)

        self.thread = StartToggle()
        self.stop_signal.connect(self.thread.stop)

    def on_click(self):
        self.started = not self.started
        if self.started:
            self.ui.toggle_button.setText('Stop')
            self.thread.reset()
            self.thread.start()
        else:
            self.ui.toggle_button.setText('Start')
            self.stop_signal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    app.setPalette(palette)
    window = MainWindow()
    window.Form.show()

    sys.exit(app.exec_())
