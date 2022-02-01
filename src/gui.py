import os
import sys
import time
from datetime import datetime, timedelta

from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from graph import GraphGenerator
from qtd_gui import Ui_MainWindow
from sql_commands import Writer
from tracker import Tracker


class MplCanvas(FigureCanvasQTAgg):
    """
    A class to transfer the canvas between threads.
    """
    def __init__(self, parent=None):
        fig = Figure(facecolor='#373E41')
        fig.subplots_adjust(0.14, 0.08, 0.96, 0.92)
        self.axes = fig.add_subplot(111)
        self.axes.set_facecolor(color='#1F242A')
        super(MplCanvas, self).__init__(fig)


class StartToggle(QThread):
    """
    A class to toggle user activity tracking.
    """
    def __init__(self, path):
        QThread.__init__(self)
        self.enabled = True
        self.delay = 10
        self.writer = Writer(path)
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
    """
    A class to update the graph and transfer parameters from MainWindow to GraphGenerator.
    """
    def __init__(self, canvas, path):
        QThread.__init__(self)
        self.enabled = True
        self.icons = True
        self.instances = True
        self.legend = True
        self.names = True
        self.from_date = (datetime.now().date() - timedelta(days=7)).strftime('%Y-%m-%d')
        self.to_date = datetime.now().date().strftime('%Y-%m-%d')
        self.path = path
        self.canvas = canvas

    def change_states(self, icons, instances, legend, names):
        self.icons = icons
        self.instances = instances
        self.legend = legend
        self.names = names

    def change_dates(self, from_date, to_date):
        self.from_date = from_date
        self.to_date = to_date

    def __del__(self):
        self.wait()

    def run(self):
        while self.enabled:
            try:
                GraphGenerator(self.icons, self.instances, self.legend, self.names, 5, self.from_date, self.to_date, self.canvas.axes)
                self.canvas.draw()
                self.canvas.axes.clear()
            except Exception as e:
                print(f'{e}: Graph generation failed, sqlite file might be empty')
            time.sleep(1)

    def stop(self):
        self.enabled = False

    def reset(self):
        self.enabled = True


class MainWindow(QWidget):
    """
    A class for the parent window.
    """
    tracking_signal = pyqtSignal()
    generate_signal = pyqtSignal()
    states_signal = pyqtSignal(bool, bool, bool, bool)
    dates_signal = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.tracking = False
        self.generating = False
        self.ui = Ui_MainWindow()
        self.Form = QMainWindow()
        self.ui.setupUi(self.Form)

        self.ui.from_date.setDate(datetime.now().date() - timedelta(days=7))
        self.ui.to_date.setDate(datetime.now().date())
        self.ui.from_date.dateChanged.connect(self.on_change_dates)
        self.ui.to_date.dateChanged.connect(self.on_change_dates)

        self.checkboxes = [self.ui.icons_checkbox, self.ui.instances_checkbox, self.ui.legend_checkbox, self.ui.names_checkbox]

        for checkbox in self.checkboxes:
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(self.on_change_states)

        self.ui.toggle_button.clicked.connect(self.on_toggle)
        self.ui.graph_button.clicked.connect(self.on_generate)

        self.figure = plt.figure()
        self.canvas = MplCanvas(self.figure)
        self.ui.graph_layout.addWidget(self.canvas)
        self.path = os.getenv('UserProfile') + r'\Documents\TimeSleuth\activity.sqlite'

        try:
            GraphGenerator(*[i.checkState() for i in self.checkboxes], 5, self.ui.from_date.date().toString('yyyy-MM-dd'), self.ui.to_date.date().toString('yyyy-MM-dd'), self.canvas.axes)
            self.canvas.draw()
        except Exception as e:
            print(f'{e}: Graph generation failed, sqlite file might be empty')

        self.toggle_thread = StartToggle()
        self.graph_thread = GraphManager(self.canvas)

        self.generate_signal.connect(self.graph_thread.stop)
        self.states_signal.connect(self.graph_thread.change_states)
        self.dates_signal.connect(self.graph_thread.change_dates)
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

    def on_change_states(self):
        states = [i.checkState() for i in self.checkboxes]

        self.states_signal.emit(*states)

    def on_change_dates(self):
        dates = (self.ui.from_date.date().toString('yyyy-MM-dd'), self.ui.to_date.date().toString('yyyy-MM-dd'))

        self.dates_signal.emit(*dates)


if __name__ == "__main__":
    path = os.getenv('UserProfile') + '\\Documents\\'
    try:
        os.mkdir(path + r'\TimeSleuth')
    except FileExistsError:
        pass
    
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
   
