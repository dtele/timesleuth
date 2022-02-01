import sys
import time
from datetime import datetime, timedelta
from os import getenv, mkdir

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
        # change file name later
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
        self.date_start = (datetime.now().date() - timedelta(days=7)).strftime('%Y-%m-%d')
        self.date_end = datetime.now().date().strftime('%Y-%m-%d')
        self.delay = 1
        self.processes_num = 3
        self.path = path
        self.canvas = canvas

    def change_states(self, icons, instances, legend, names):
        self.icons = icons
        self.instances = instances
        self.legend = legend
        self.names = names

    def change_dates(self, date_start, date_end):
        self.date_start = date_start
        self.date_end = date_end

    def change_sliders(self, delay, processes_num):
        self.delay = delay
        self.processes_num = processes_num

    def __del__(self):
        self.wait()

    def run(self):
        while self.enabled:
            try:
                GraphGenerator(icons=self.icons, instances=self.instances, legend=self.legend, names=self.names,
                               num_bars=self.processes_num, date_start=self.date_start, date_end=self.date_end,
                               path=self.path, ax=self.canvas.axes)
                self.canvas.draw()
                self.canvas.axes.clear()
            except Exception as e:
                self.canvas.axes.clear()
                self.canvas.draw()
                print(f'{e}: Graph generation failed, sqlite file might be empty')
            time.sleep(self.delay)

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
    sliders_signal = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.tracking = False
        self.generating = False
        self.ui = Ui_MainWindow()
        self.Form = QMainWindow()
        self.ui.setupUi(self.Form)

        # Date selection
        self.ui.date_start.setDate(datetime.now().date() - timedelta(days=7))
        self.ui.date_end.setDate(datetime.now().date())
        self.ui.date_start.dateChanged.connect(self.on_change_dates)
        self.ui.date_end.dateChanged.connect(self.on_change_dates)

        # Sliders
        self.ui.delay_slider.setValue(1)
        self.ui.processes_slider.setValue(3)
        self.ui.delay_slider.valueChanged.connect(self.on_change_sliders)
        self.ui.processes_slider.valueChanged.connect(self.on_change_sliders)

        # Checkboxes
        self.checkboxes = [self.ui.icons_checkbox, self.ui.instances_checkbox, self.ui.legend_checkbox, self.ui.names_checkbox]

        for checkbox in self.checkboxes:
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(self.on_change_states)

        # Buttons
        self.ui.toggle_button.clicked.connect(self.on_toggle)
        self.ui.graph_button.clicked.connect(self.on_generate)

        # Graph
        self.figure = plt.figure()
        self.canvas = MplCanvas(self.figure)
        self.ui.graph_layout.addWidget(self.canvas)

        self.path = fr'{getenv("UserProfile")}\Documents\TimeSleuth\activity.sqlite'

        try:
            GraphGenerator(*[checkbox.checkState() for checkbox in self.checkboxes],
                           num_bars=3, date_start=self.ui.date_start.date().toString('yyyy-MM-dd'),
                           date_end=self.ui.date_end.date().toString('yyyy-MM-dd'),
                           path=self.path, ax=self.canvas.axes)
            self.canvas.draw()
        except Exception as e:
            print(f'{e}: Graph generation failed, sqlite file might be empty')

        # Threads
        self.toggle_thread = StartToggle(self.path)
        self.graph_thread = GraphManager(self.canvas, self.path)

        self.tracking_signal.connect(self.toggle_thread.stop)
        self.generate_signal.connect(self.graph_thread.stop)
        self.states_signal.connect(self.graph_thread.change_states)
        self.dates_signal.connect(self.graph_thread.change_dates)
        self.sliders_signal.connect(self.graph_thread.change_sliders)

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
        dates = (self.ui.date_start.date().toString('yyyy-MM-dd'), self.ui.date_end.date().toString('yyyy-MM-dd'))

        self.dates_signal.emit(*dates)

    def on_change_sliders(self):
        values = (self.ui.delay_slider.value(), self.ui.processes_slider.value())

        self.ui.delay_label.setText(f'Delay - {values[0]}s')
        self.ui.processes_label.setText(f'Processes - {values[1]}')

        self.sliders_signal.emit(*values)


if __name__ == "__main__":
    try:
        mkdir(fr'{getenv("UserProfile")}\Documents\TimeSleuth')
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
