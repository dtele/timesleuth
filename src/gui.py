import sys
import time
from datetime import datetime, timedelta

from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

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


class GraphManager(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.enabled = True
        self.icons = False
        self.instances = False
        self.legend = False
        self.names = False

    def change_settings(self, icons, instances, legend, names):
        self.icons = icons
        self.instances = instances
        self.legend = legend
        self.names = names

    def __del__(self):
        self.wait()

    def run(self):
        while self.enabled:
            # Graph generation and embedding into gui here
            ...

    def stop(self):
        self.enabled = False

    def reset(self):
        self.enabled = True


class MainWindow(QWidget):
    tracking_signal = pyqtSignal()
    generate_signal = pyqtSignal()
    states_signal = pyqtSignal(bool, bool, bool, bool)

    def __init__(self):
        super().__init__()
        self.tracking = False
        self.generating = False
        self.ui = Ui_MainWindow()
        self.Form = QMainWindow()
        self.ui.setupUi(self.Form)

        self.ui.from_date.setDate(datetime.now().date() - timedelta(days=7))
        self.ui.to_date.setDate(datetime.now().date())

        self.ui.toggle_button.clicked.connect(self.on_toggle)
        self.ui.graph_button.clicked.connect(self.on_generate)
        self.ui.icons_checkbox.stateChanged.connect(self.on_change)
        self.ui.instances_checkbox.stateChanged.connect(self.on_change)
        self.ui.legend_checkbox.stateChanged.connect(self.on_change)
        self.ui.names_checkbox.stateChanged.connect(self.on_change)

        self.toggle_thread = StartToggle()
        self.graph_thread = GraphManager()

        self.generate_signal.connect(self.graph_thread.stop)
        self.states_signal.connect(self.graph_thread.change_settings)
        self.tracking_signal.connect(self.toggle_thread.stop)

    def on_toggle(self):
        self.tracking = not self.tracking
        if self.tracking:
            self.ui.toggle_button.setText('Stop Tracking')
            self.toggle_thread.reset()
            self.toggle_thread.start()
        else:
            self.ui.toggle_button.setText('Start Tracking')
            self.tracking_signal.emit()

    def on_generate(self):
        self.generating = not self.generating
        if self.generating:
            self.ui.graph_button.setText('Stop Generating Graph')
            self.graph_thread.reset()
            self.graph_thread.start()
        else:
            self.ui.graph_button.setText('Start Generating Graph')
            self.generate_signal.emit()

    def on_change(self):
        states = (self.ui.icons_checkbox.isChecked(),
                  self.ui.instances_checkbox.isChecked(),
                  self.ui.legend_checkbox.isChecked(),
                  self.ui.names_checkbox.isChecked())

        self.states_signal.emit(*states)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
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
