from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 515)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 515))
        MainWindow.setMaximumSize(QtCore.QSize(1000, 515))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("projectlogo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QMainWindow{\n"
"      background:  #1F242A;\n"
"}\n"
"QPushButton{\n"
"background-color:rgb(55,62,65);\n"
"color:rgb(201,201,201);\n"
"border: 1px solid;\n"
"}\n"
"QPushButton:hover{\n"
"border:2px solid rgb(255,255,255);\n"
"color:rgb(255,255,255);\n"
"}\n"
"QLabel{\n"
"color:rgb(201,201,201);\n"
"}\n"
"QSlider:hover{\n"
"border: 1px solid rgb(255,255,255);\n"
"}\n"
"QCheckBox{\n"
"color:rgb(201,201,201);\n"
"}\n"
"QCheckBox:hover{\n"
"border: 1px solid rgb(255,255,255);\n"
"color:rgb(255,255,255);\n"
"}\n"
"QCheckBox:checked{\n"
"color:rgb(255,255,255);\n"
"}\n"
"QGridLayout.settings_layout{\n"
"background-color:rgb(55,62,65);\n"
"border: 2px solid;\n"
"}\n"
"QVBoxLayout#graph_layout{\n"
"border: 1px solid;\n"
"}\n"
"QDateEdit{\n"
"color:rgb(201,201,201);\n"
"}\n"
"QDateEdit:hover{\n"
"color:rgb(255,255,255);\n"
"}\n"                                
"QDateEdit:focus{\n"
"color:rgb(255,255,255);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 7, 291, 161))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.buttons_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setObjectName("buttons_layout")
        self.toggle_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.toggle_button.setMinimumSize(QtCore.QSize(50, 75))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.toggle_button.setFont(font)
        self.toggle_button.setObjectName("toggle_button")
        self.buttons_layout.addWidget(self.toggle_button, 1, 0, 1, 1)
        self.graph_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.graph_button.setMinimumSize(QtCore.QSize(50, 75))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.graph_button.setFont(font)
        self.graph_button.setObjectName("graph_button")
        self.buttons_layout.addWidget(self.graph_button, 2, 0, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 170, 291, 322))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.settings_layout = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.settings_layout.setContentsMargins(0, 0, 0, 0)
        self.settings_layout.setObjectName("settings_layout")
        self.from_date = QtWidgets.QDateEdit(self.gridLayoutWidget_2)
        self.from_date.setObjectName("from_date")
        self.settings_layout.addWidget(self.from_date, 3, 0, 1, 1)
        self.delay_slider = QtWidgets.QSlider(self.gridLayoutWidget_2)
        palette = QtGui.QPalette()
        self.delay_slider.setPalette(palette)
        self.delay_slider.setOrientation(QtCore.Qt.Horizontal)
        self.delay_slider.setObjectName("delay_slider")
        self.settings_layout.addWidget(self.delay_slider, 6, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.settings_layout.addItem(spacerItem, 18, 0, 1, 1)
        self.icons_checkbox = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.icons_checkbox.setObjectName("icons_checkbox")
        self.settings_layout.addWidget(self.icons_checkbox, 13, 0, 1, 1, QtCore.Qt.AlignHCenter)
        spacerItem1 = QtWidgets.QSpacerItem(20, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.settings_layout.addItem(spacerItem1, 18, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 12, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.settings_layout.addItem(spacerItem2, 12, 1, 1, 1)
        self.processes_slider = QtWidgets.QSlider(self.gridLayoutWidget_2)
        self.processes_slider.setOrientation(QtCore.Qt.Horizontal)
        self.processes_slider.setObjectName("processes_slider")
        self.settings_layout.addWidget(self.processes_slider, 10, 0, 1, 2)
        self.instances_checkbox = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.instances_checkbox.setObjectName("instances_checkbox")
        self.settings_layout.addWidget(self.instances_checkbox, 13, 1, 1, 1, QtCore.Qt.AlignHCenter)
        spacerItem3 = QtWidgets.QSpacerItem(20, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.settings_layout.addItem(spacerItem3, 8, 1, 1, 1)
        self.processes_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.processes_label.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setUnderline(False)
        self.processes_label.setFont(font)
        self.processes_label.setAlignment(QtCore.Qt.AlignCenter)
        self.processes_label.setObjectName("processes_label")
        self.settings_layout.addWidget(self.processes_label, 11, 0, 1, 2)
        spacerItem4 = QtWidgets.QSpacerItem(20, 12, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.settings_layout.addItem(spacerItem4, 12, 0, 1, 1)
        self.settings_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.settings_label.setFont(font)
        self.settings_label.setAlignment(QtCore.Qt.AlignCenter)
        self.settings_label.setObjectName("settings_label")
        self.settings_layout.addWidget(self.settings_label, 0, 0, 2, 2)
        spacerItem5 = QtWidgets.QSpacerItem(20, 8, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.settings_layout.addItem(spacerItem5, 5, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.settings_layout.addItem(spacerItem6, 14, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.settings_layout.addItem(spacerItem7, 14, 1, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(20, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.settings_layout.addItem(spacerItem8, 8, 0, 1, 1)
        self.delay_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.delay_label.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setUnderline(False)
        self.delay_label.setFont(font)
        self.delay_label.setAlignment(QtCore.Qt.AlignCenter)
        self.delay_label.setObjectName("delay_label")
        self.settings_layout.addWidget(self.delay_label, 7, 0, 1, 2)
        self.to_date = QtWidgets.QDateEdit(self.gridLayoutWidget_2)
        self.to_date.setObjectName("to_date")
        self.settings_layout.addWidget(self.to_date, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.settings_layout.addWidget(self.label, 4, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.settings_layout.addWidget(self.label_2, 4, 1, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(20, 8, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.settings_layout.addItem(spacerItem9, 2, 0, 1, 1)
        self.names_checkbox = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.names_checkbox.setObjectName("names_checkbox")
        self.settings_layout.addWidget(self.names_checkbox, 16, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.legend_checkbox = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.legend_checkbox.setObjectName("legend_checkbox")
        self.settings_layout.addWidget(self.legend_checkbox, 16, 0, 1, 1, QtCore.Qt.AlignHCenter)
        spacerItem10 = QtWidgets.QSpacerItem(20, 8, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.settings_layout.addItem(spacerItem10, 5, 1, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(20, 8, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.settings_layout.addItem(spacerItem11, 2, 1, 1, 1)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(309, 9, 681, 471))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.graph_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.graph_layout.setContentsMargins(0, 0, 0, 0)
        self.graph_layout.setObjectName("graph_layout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "TimeSleuth"))
            self.toggle_button.setText(_translate("MainWindow", "Start Tracking"))
            self.graph_button.setText(_translate("MainWindow", "Start Generating Graph"))
            self.icons_checkbox.setText(_translate("MainWindow", "Show Icons   "))
            self.instances_checkbox.setText(_translate("MainWindow", "Show Instances"))
            self.processes_label.setText(_translate("MainWindow", "Processes"))
            self.settings_label.setText(_translate("MainWindow", "Graph Settings"))
            self.delay_label.setText(_translate("MainWindow", "Delay"))
            self.label.setText(_translate("MainWindow", "From"))
            self.label_2.setText(_translate("MainWindow", "To"))
            self.names_checkbox.setText(_translate("MainWindow", "Show Names    "))
            self.legend_checkbox.setText(_translate("MainWindow", "Show Legend"))
            
