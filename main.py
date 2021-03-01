from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtWidgets, QtGui, sip, uic
import sys
import os
import json
import tempfile
import time
import webbrowser
import smtplib
import socket
import platform
import re
import math
import qdarkgraystyle
import trianglesolver
# from functools import partial
# from shutil import copyfile
# from PyQt5.QtGui import QPainterPath
# from email.mime.text import MIMEText

canvas_height = 300
canvas_width = 460

ChiploadRole = QtCore.Qt.UserRole + 1000
FeedrateRole = QtCore.Qt.UserRole + 1001

file_dir = os.path.dirname(os.path.realpath(__file__)) + '\Bits/'
if not os.path.exists(file_dir):
    os.makedirs(file_dir)

if os.path.exists(file_dir + 'run_time_settings.json'):
    with open(file_dir + 'run_time_settings.json') as file:
        run_time_settings_loaded = json.load(file)
else:
    file = open(file_dir + 'run_time_settings.json', 'w+')
    file.write('''{
}''')
    run_time_settings_current_settings = {
        'last_selected_bit': '{}'.format(0),
        'last_selected_mat': '{}'.format(0),
        'last_rpm': '{}'.format(18000),
        'last_flute': '{}'.format(2)
    }
    file.close()

    with open(file_dir + 'run_time_settings.json', mode='w+', encoding='utf-8') as file:
        json.dump(run_time_settings_current_settings,
                  file, ensure_ascii=False, indent=4)
    with open(file_dir + 'run_time_settings.json') as file:
        run_time_settings_loaded = json.load(file)

if os.path.exists(file_dir + 'settings.json'):
    with open(file_dir + 'settings.json') as file:
        settings = json.load(file)
else:
    file = open(file_dir + 'settings.json', 'w+')
    file.write('''{
}''')
    current_settings = {
        'imperial': '{}'.format('True'),
        'metric': '{}'.format('False'),
        'minute': '{}'.format('True'),
        'second': '{}'.format('False'),
        'millimeter': '{}'.format('True'),
        'meter': '{}'.format('False'),
        'inch': '{}'.format('False'),
        'feet': '{}'.format('False')
    }
    file.close()

    with open(file_dir + 'settings.json', mode='w+', encoding='utf-8') as file:
        json.dump(current_settings, file, ensure_ascii=False, indent=4)
    with open(file_dir + 'settings.json') as file:
        settings = json.load(file)

if not os.path.exists(file_dir + 'configure.json'):
    file = open(file_dir + 'configure.json', 'w+')
    file.write('''{
    \"bits\": [
        {
            \"material\": [
                \"Hard Wood\"
            ],
            \"chipload\": [
                \"0.003 - 0.004 - 0.005\",
                \"0.009 - 0.010 - 0.011\",
                \"0.015 - 0.016 - 0.017 - 0.018\",
                \"0.019 - 0.020 - 0.021\"
            ]
        },
        {
            \"material": [
                "Softwood & Plywood"
            ],
            \"chipload\": [
                \"0.003 - 0.004 - 0.005\",
                \"0.009 - 0.010 - 0.011\",
                \"0.015 - 0.016 - 0.017 - 0.018\",
                \"0.019 - 0.020 - 0.021\"
            ]
        },
        {
            \"material\": [
                \"MDF/Particle Board\"
            ],
            "chipload": [
                \"0.004 - 0.005 - 0.006 - 0.007\",
                \"0.013 - 0.014 - 0.015 - 0.016\",
                \"0.020 - 0.021 - 0.022 - 0.023\",
                \"0.025 - 0.026 - 0.027\"
            ]
        },
        {
            \"material\": [
                \"High Pressure Laminate\"
            ],
            \"chipload\": [
                \"0.003 - 0.004 - 0.005\",
                \"0.009 - 0.010 - 0.011 - 0.012\",
                \"0.015 - 0.016 - 0.017 - 0.018\",
                \"0.023 - 0.024 - 0.025\"
            ]
        },
        {
            \"material\": [
                \"Phenolic\"
            ],
            "chipload": [
                \"0.001 - 0.002 - 0.003\",
                \"0.004 - 0.005 - 0.006\",
                \"0.006 - 0.007 - 0.008\",
                \"0.010 - 0.011 - 0.012\"
            ]
        },
        {
            \"material\": [
                \"Hard Plastic\"
            ],
            \"chipload\": [
                \"0.002 - 0.003 - 0.004\",
                \"0.006 - 0.007 - 0.008 - 0.009\",
                \"0.008 - 0.009 - 0.010\",
                \"0.010 - 0.011 - 0.012\"
            ]
        },
        {
            \"material\": [
                \"Soft Plastic\"
            ],
            \"chipload\": [
                \"0.003 - 0.004 - 0.005 - 0.006\",
                \"0.007 - 0.008 - 0.009 - 0.010\",
                \"0.010 - 0.011 - 0.012\",
                \"0.012 - 0.013 - 0.014 - 0.015 - 0.016\"
            ]
        },
        {
            \"material\": [
                \"Solid Surface\"
            ],
            \"chipload\": [
                \"0.002 - 0.003 - 0.004\",
                \"0.006 - 0.007 - 0.008 - 0.009\",
                \"0.008 - 0.009 - 0.010\",
                \"0.010 - 0.011 - 0.012\"
            ]
        },
        {
            \"material\": [
                \"Acrylic\"
            ],
            \"chipload\": [
                \"0.003 - 0.004 - 0.005\",
                \"0.008 - 0.009 - 0.010\",
                \"0.010 - 0.011 - 0.012\",
                \"0.012 - 0.013 - 0.014 - 0.015\"
            ]
        },
        {
            \"material\": [
                \"Aluminium\"
            ],
            \"chipload\": [
                \"0.003 - 0.004",
                \"0.005 - 0.006 - 0.007\",
                \"0.006 - 0.007 - 0.008\",
                \"0.008 - 0.009 - 0.010\"
            ]
        }
    ]
}''')
    file.close()

file = open(file_dir + 'configure.json', 'r+')
first_char = file.read(1)
if not first_char:
    file.write('''{
    \"bits\": [

    ]
}''')
    file.close()
file = open(file_dir + 'settings.json', 'r+')
first_char = file.read(1)
if not first_char:
    file.write('')
    file.close()
if os.path.exists(file_dir + 'configure.json'):
    with open(file_dir + 'configure.json') as file:
        data = json.load(file)
else:
    file = open(file_dir + 'configure.json', 'w+')
    file.write('''{
    \"bits\": [
    ]
}''')
    file.close()
    with open(file_dir + 'configure.json') as file:
        data = json.load(file)

current_data = data
current_settings = settings
run_time_settings = run_time_settings_loaded
# minute = True
# second = False
# millimeters = True
# meters = False
# inches = False
# feet = False
if settings['imperial'] == 'True':
    bit_widths = ['1/8\"', '1/4\"', '3/8\"', '1/2\"']
    imperial = True
else:
    imperial = False
if settings['metric'] == 'True':
    bit_widths = ['3.175mm', '6.35mm"', '9.525mm"', '12.7mm"']
    metric = True
else:
    metric = False
if settings['minute'] == 'True':
    minute = True
else:
    minute = False
if settings['second'] == 'True':
    second = True
else:
    second = False
if settings['millimeter'] == 'True':
    millimeters = True
else:
    millimeters = False
if settings['meter'] == 'True':
    meters = True
else:
    meters = False
if settings['inch'] == 'True':
    inches = True
else:
    inches = False
if settings['feet'] == 'True':
    feet = True
else:
    feet = False
# print(data)
materials = []
bit_widths = []
chiploads = []
feedrates = []

if not materials:
    for bits in data['bits']:
        for material in bits['material']:
            materials.append(material)
        for chipload in bits['chipload']:
            chiploads.append(chipload)
        # for feedrate in bits['feedrate']:
        #     feedrates.append(feedrate)
has_started = False

last_selected_bit = int(run_time_settings['last_selected_bit'])
last_selected_mat = int(run_time_settings['last_selected_mat'])
last_rpm = int(run_time_settings['last_rpm'])
last_flute = int(run_time_settings['last_flute'])
title = 'CNC Bit Config'
version = 'v1.2'


class App(QMainWindow):

    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        # app.setStyleSheet(qdarkgraystyle.load_stylesheet())
        # app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

        # self.txtMaterial = QLineEdit(self)
        # self.txtBitWidth = QLineEdit(self)
        self.materialType = QComboBox(self)
        self.bitWidthType = QComboBox(self)
        self.txtChipLoad = QLineEdit(self)
        self.txtFlute = QLineEdit(self)
        self.txtRPM = QLineEdit(self)
        self.txtFeedRate = QLineEdit(self)
        self.title = title
        self.version = version
        self.left = 100
        self.top = 100
        self.width = canvas_width
        self.height = canvas_height
        self.setWindowIcon(QtGui.QIcon('icons/icon5.png'))
        # self.setWindowFlags(QtCore.Qt.X11BypassWindowManagerHint)
        if materials:
            # self.messageBox("No bits added yet!")
            self.selected_material = materials[0]
            self.selected_chipload = chiploads[0]
            self.selected_feedrate = None
        else:
            self.selected_material = None
            self.selected_chipload = None
            self.selected_feedrate = None
        self.initUI()

    def initUI(self):
        global has_started
        # self.update_text()
        self.setWindowTitle(self.title + ' ' + self.version)
        self.setFixedSize(self.width, self.height)
        # self.setMinimumSize(self.width, self.height)
        # TOOL BAR MENU
        global last_selected_bit
        global last_selected_mat
        global last_rpm
        global last_flute
        global bit_widths
        with open(file_dir + 'run_time_settings.json') as file:
            run_time_settings = json.load(file)

        last_selected_bit = int(run_time_settings['last_selected_bit'])
        last_selected_mat = int(run_time_settings['last_selected_mat'])
        last_rpm = int(run_time_settings['last_rpm'])
        last_flute = int(run_time_settings['last_flute'])

        mainMenu = self.menuBar()
        mainMenu.setFont(QtGui.QFont('Calibri', 14))
        fileMenu = mainMenu.addMenu('File')
        fileMenu.setFont(QtGui.QFont('Calibri', 14))
        exitButton = QAction(QIcon('icons/exit.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close_application)
        fileMenu.addAction(exitButton)

        addConfigButton = QAction(QIcon('icons/add.png'), 'Add Material', self)
        # addConfigButton.setShortcut('Ctrl+A')
        addConfigButton.setStatusTip('Add Bit to Configuration')
        addConfigButton.triggered.connect(self.add_configureationPopup)
        fileMenu.addAction(addConfigButton)

        Settings = QAction(QIcon('icons/settings.png'), 'Settings', self)
        Settings.setStatusTip('Change settings of program')
        Settings.triggered.connect(self.settingsPopup)
        fileMenu.addAction(Settings)

        # impMenu = QMenu('Config', self)
        impAction = QAction(QIcon('icons/import.png'), 'Import File', self)
        impAction.setStatusTip('Import file')
        impAction.triggered.connect(self.import_config)
        fileMenu.addAction(impAction)

        expAction = QAction(QIcon('icons/export.png'), 'Export File', self)
        expAction.setStatusTip('Save/Export File')
        expAction.setShortcut('Ctrl+S')
        expAction.triggered.connect(self.export_config)
        fileMenu.addAction(expAction)
        # fileMenu.addMenu(impMenu)

        helpMenu = mainMenu.addMenu('Help')
        helpMenu.setFont(QtGui.QFont('Calibri', 14))

        helpButton = QAction(QIcon('icons/help.png'), 'About', self)
        helpButton.setStatusTip('About the app')
        helpButton.triggered.connect(self.about_message_box)

        contactButton = QAction(QIcon('icons/contact.png'), 'Contact', self)
        calculateChipLoadButton = QAction(
            QIcon('icons/play.png'), 'Calculate Chipload', self)
        calculateChipLoadButton.triggered.connect(
            self.calculate_chipload_Popup)
        # contactButton.triggered.connect(self.contactPopup)

        tipMenu = mainMenu.addMenu('Tips')
        tipMenu.setFont(QtGui.QFont('Calibri', 14))
        tipButton = QAction(QIcon('icons/tip.png'), 'Tip', self)
        tipButton.setStatusTip('Gives tips on how you should run your CNC')
        tipButton.triggered.connect(self.tipsPopup)
        tipMenu.addAction(tipButton)

        helpMenu.addAction(helpButton)
        # helpMenu.addAction(contactButton)

        progMenu = mainMenu.addMenu('Programs')
        progMenu.setFont(QtGui.QFont('Calibri', 14))
        progButton = QAction(QIcon('icons/play.png'), 'Bit Depth Calc', self)
        progButton.setStatusTip('Run a custom program to calculate bit depth')
        progButton.triggered.connect(self.drawPopup)
        progMenu.addAction(progButton)
        progMenu.addAction(calculateChipLoadButton)

        lblBitwidth = QLabel(self)
        lblBitwidth.setText('Bit width:')
        lblBitwidth.move(5, 60)
        lblBitwidth.setFont(QtGui.QFont('Calibri', 16))

        lblChipload = QLabel(self)
        lblChipload.setText('Chipload:')
        lblChipload.move(5, 110)
        lblChipload.setFont(QtGui.QFont('Calibri', 16))

        lblFlute = QLabel(self)
        lblFlute.setText('Flute:')
        lblFlute.move(5, 160)
        lblFlute.setFont(QtGui.QFont('Calibri', 16))

        lblRPM = QLabel(self)
        lblRPM.setText('RPM:')
        lblRPM.move(175, 160)
        lblRPM.setFont(QtGui.QFont('Calibri', 16))

        lblFeedrate = QLabel(self)
        lblFeedrate.setText('Feedrate:')
        lblFeedrate.move(5, 210)
        lblFeedrate.setFont(QtGui.QFont('Calibri', 16))

        self.lblchiploadSetting = QLabel(self)
        self.lblchiploadSetting.move(390, 120)
        self.lblchiploadSetting.setFont(QtGui.QFont('Calibri', 10))
        self.lblchiploadSetting.setText('(inches)')

        self.lblcurrentSettings = QLabel(self)
        self.lblcurrentSettings.move(390, 220)
        self.lblcurrentSettings.setFont(QtGui.QFont('Calibri', 10))

        if millimeters == True:
            if second == True:
                self.lblcurrentSettings.setText('(mm/sec)')
            elif minute == True:
                self.lblcurrentSettings.setText('(mm/min)')
        elif meters == True:
            if second == True:
                self.lblcurrentSettings.setText('(m/sec)')
            elif minute == True:
                self.lblcurrentSettings.setText('(m/min)')
        elif inches == True:
            if second == True:
                self.lblcurrentSettings.setText('(in/sec)')
            elif minute == True:
                self.lblcurrentSettings.setText('(in/min)')
        elif feet == True:
            if second == True:
                self.lblcurrentSettings.setText('(ft/sec)')
            elif minute == True:
                self.lblcurrentSettings.setText('(ft/min)')
        else:
            return

        f = self.txtFeedRate.font()
        f.setPointSize(10)
        self.txtChipLoad.setFont(f)
        self.txtChipLoad.setText(self.selected_chipload)
        self.txtChipLoad.setAlignment(Qt.AlignCenter)
        self.txtChipLoad.textChanged.connect(self.calculate)
        self.txtChipLoad.move(120, 100)
        self.txtChipLoad.resize(270, 50)
        self.txtChipLoad.setValidator(QtGui.QDoubleValidator(0, 100000, 3))
        self.txtChipLoad.setToolTip(
            'The chipload (inches) of that bits width (per RPM).')
        self.txtChipLoad.keyReleaseEvent = self.keyPressEvent

        f = self.txtFlute.font()
        f.setPointSize(10)
        self.txtFlute.setFont(f)
        self.txtFlute.setText(run_time_settings['last_flute'])
        self.txtFlute.setAlignment(Qt.AlignCenter)
        self.txtFlute.textChanged.connect(self.calculate)
        self.txtFlute.move(120, 150)
        self.txtFlute.resize(50, 50)
        self.txtFlute.setValidator(QtGui.QDoubleValidator(0, 100000, 3))
        self.txtFlute.setToolTip('How many edges the bit has.')
        self.txtFlute.keyReleaseEvent = self.keyPressEvent

        f = self.txtRPM.font()
        f.setPointSize(10)
        self.txtRPM.setFont(f)
        self.txtRPM.setText(run_time_settings['last_rpm'])
        self.txtRPM.setAlignment(Qt.AlignCenter)
        self.txtRPM.textChanged.connect(self.calculate)
        self.txtRPM.move(280, 150)
        self.txtRPM.resize(110, 50)
        self.txtRPM.setValidator(QtGui.QDoubleValidator(0, 100000, 3))
        self.txtRPM.setToolTip('The RPM of the bit.')
        self.txtRPM.keyReleaseEvent = self.keyPressEvent

        f = self.txtFeedRate.font()
        f.setPointSize(10)
        self.txtFeedRate.setFont(f)
        self.txtFeedRate.setText(self.selected_feedrate)
        self.txtFeedRate.setAlignment(Qt.AlignCenter)
        self.txtFeedRate.textChanged.connect(self.calculate)
        self.txtFeedRate.move(120, 200)
        self.txtFeedRate.resize(270, 50)
        self.txtFeedRate.setValidator(QtGui.QDoubleValidator(0, 100000, 3))
        self.txtFeedRate.keyReleaseEvent = self.keyPressEvent
        # BUTTONS
        # btnCalculate = QPushButton('Calculate', self)
        # btnCalculate.move(120, 300)
        # btnCalculate.resize(220,40)
        # btnCalculate.setFont(QtGui.QFont('Calibri', 15))
        # btnCalculate.clicked.connect(self.calculate)
        # btnCalculate.setToolTip('Calculate for Chipload/Feed rate.')

        # btnRefresh = QPushButton('Refresh', self)
        # btnRefresh.move(230, 300)
        # btnRefresh.resize(110,40)
        # btnRefresh.setFont(QtGui.QFont('Calibri', 15))
        # btnRefresh.clicked.connect(self.refresh)
        # btnRefresh.setToolTip('Refresh the program')

        # materialType BOX
        self.m_model = QtGui.QStandardItemModel(self)
        self.materialType.setModel(self.m_model)
        self.materialType.currentIndexChanged.connect(
            self._on_material_selection_changed
        )
        # for i in materials:
        #     self.materialType.addItem(i)
        self.materialType.setToolTip('Selection of materials')
        self.materialType.move(200, 50)
        self.materialType.resize(190, 50)
        self.materialType.setFont(QtGui.QFont('Calibri', 11))
        self._on_material_selection_changed(self.materialType.currentIndex())
        # Bit Width BOX
        self.bitWidthType.setModel(self.m_model)
        # self.bitWidthType.currentIndexChanged.connect(partial(self._on_bitwidth_selection_changed, last_selected_bit))
        self.bitWidthType.currentIndexChanged.connect(
            self._on_bitwidth_selection_changed)
        # for i in bit_widths:
        #     self.bitWidthType.addItem(i + '"')
        if imperial == True:
            self.bitWidthType.setFont(QtGui.QFont('Calibri', 12))
        else:
            self.bitWidthType.setFont(QtGui.QFont('Calibri', 10))
        self.bitWidthType.setToolTip('Selection of bit widths')
        self.bitWidthType.resize(80, 50)
        self.bitWidthType.move(120, 50)
        self.fill_model()
        if settings['imperial'] == 'True' or imperial == True:
            bit_widths = ['1/8\"', '1/4\"', '3/8\"', '1/2\"']
        elif settings['metric'] == 'True' or metric == True:
            bit_widths = ['3.175mm', '6.35mm', '9.525mm', '12.7mm']
        # Now use a palette to switch to dark colors:
        # app.setStyle("Windows Vista")
        # app.setStyle("Windows")
        # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        # app.setStyle('Fusion')
        # palette = QPalette()
        # palette.setColor(QPalette.Window, QColor(53, 53, 53))
        # palette.setColor(QPalette.WindowText, Qt.white)
        # palette.setColor(QPalette.Base, QColor(25, 25, 25))
        # palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        # palette.setColor(QPalette.ToolTipBase, Qt.white)
        # palette.setColor(QPalette.ToolTipText, Qt.white)
        # palette.setColor(QPalette.Text, Qt.white)
        # palette.setColor(QPalette.Button, QColor(53, 53, 53))
        # palette.setColor(QPalette.ButtonText, Qt.white)
        # palette.setColor(QPalette.BrightText, Qt.red)
        # palette.setColor(QPalette.Link, QColor(42, 130, 218))
        # palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        # palette.setColor(QPalette.HighlightedText, Qt.black)
        # app.setPalette(palette)

        self.fill_model()
        self.calculate()
        # if has_started == False:
        # has_started = True
        self.materialType.setCurrentIndex(last_selected_mat)
        self.bitWidthType.setCurrentIndex(last_selected_bit)
        self.show()

    def refresh(self):
        global has_started
        has_started = False
        App()
        self.close()

    def add_configureationPopup(self):
        self.close()
        self.add_configPopup = add_configuration('Add Config')
        self.add_configPopup.setFixedSize(300, 310)
        self.add_configPopup.setWindowTitle('Add Configuration')
        self.add_configPopup.setWindowIcon(QtGui.QIcon('icons/add.png'))
        # self.add_configPopup.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.add_configPopup.show()

    def settingsPopup(self):
        self.close()
        self.settingsPopup = options_menu('Settings')
        self.settingsPopup.setWindowIcon(QtGui.QIcon('icons/settings.png'))
        self.settingsPopup.setFixedSize(300, 250)
        # self.settingsPopup.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.settingsPopup.setWindowTitle('Settings')
        self.settingsPopup.show()

    def tipsPopup(self):
        # self.close()
        self.tipsPopup = tips_menu('Tips')
        self.tipsPopup.setWindowIcon(QtGui.QIcon('icons/tip.png'))
        self.tipsPopup.setFixedSize(300, 250)
        self.tipsPopup.setWindowTitle('Tips')
        # self.tipsPopup.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.tipsPopup.show()

    def drawPopup(self):
        # self.close()
        self.drawPopup = drawProg()
        # self.tipsPopup.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.drawPopup.show()
    # def contactPopup(self):
    # self.close()
    # self.contactPopup = calculate_chipload_menu('Email')
    # self.contactPopup.setWindowIcon(QtGui.QIcon('contact.png'))
    # self.contactPopup.setFixedSize(300, 250)
    # self.contactPopup.setWindowTitle('Email')
    # # self.tipsPopup.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
    # self.contactPopup.show()

    def calculate_chipload_Popup(self):
        # self.close()
        self.calculateChipload = calculate_chipload_menu('Calculate Chipload')
        # self.calculateChipload.setWindowIcon(QtGui.QIcon('contact.png'))
        self.calculateChipload.setFixedSize(215, 250)
        self.calculateChipload.setWindowTitle('Calculate Chipload')
        # self.calculateChipload.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.calculateChipload.show()

    def messageBox(self, text):
        buttonReply = QMessageBox.critical(
            self, 'Error!', text, QMessageBox.Ok, QMessageBox.Ok)
        return
        # buttonReply = QMessageBox.information(self, 'Contact!', "<a href=\"http://stackoverflow.com/\">Stackoverflow/</a", QMessageBox.Ok, QMessageBox.Ok)

    def about_message_box(self):
        buttonReply = QMessageBox.information(self, 'About!',
                                              "{}\nVersion: {}\n16/10/2019\nBy: Jared Gross".format(self.title,
                                                                                                    self.version),
                                              QMessageBox.Ok)

    def close_application(self):
        choice = QMessageBox.question(self, 'Exit!',
                                      "Are you sure you want to exit?",
                                      QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.No)
        if choice == QMessageBox.Yes:
            os._exit(1)
        else:
            pass

    @pyqtSlot(int)
    def _on_material_selection_changed(self, index):
        global last_selected_mat
        root_index = self.m_model.index(index, 0)
        self.bitWidthType.setRootModelIndex(root_index)
        self.bitWidthType.setCurrentIndex(last_selected_bit)
        last_selected_mat = index
        self.calculate()
        self.save_runtime_settings()

    @pyqtSlot(int)
    def _on_bitwidth_selection_changed(self, index):
        global last_selected_bit
        material = self.materialType.currentText()
        chipload = self.bitWidthType.itemData(index, ChiploadRole)
        feedrate = self.bitWidthType.itemData(index, FeedrateRole)
        if not chipload == None:
            chipload = chipload.replace(' , ', ', ')
        self.selected_material = material
        self.selected_chipload = chipload
        self.selected_feedrate = feedrate
        last_selected_bit = index
        self.save_runtime_settings()
        self.update_text()
        self.calculate()
        # print(index)

    def save_runtime_settings(self):
        run_time_settings_current_settings = {
            'last_selected_bit': '{}'.format(last_selected_bit),
            'last_selected_mat': '{}'.format(last_selected_mat),
            'last_rpm': '{}'.format(self.txtRPM.text()),
            'last_flute': '{}'.format(self.txtFlute.text())
        }
        with open(file_dir + 'run_time_settings.json', mode='w+', encoding='utf-8') as file:
            json.dump(run_time_settings_current_settings,
                      file, ensure_ascii=False, indent=4)
        with open(file_dir + 'run_time_settings.json') as file:
            run_time_settings = json.load(file)

    @pyqtSlot()
    def fill_model(self):
        # global last_selected_mat
        # global last_selected_bit
        global imperial
        global metric
        with open(file_dir + 'settings.json') as file:
            settings = json.load(file)
        with open(file_dir + 'run_time_settings.json') as file:
            run_time_settings = json.load(file)
        self.bitWidthType.clear()
        self.materialType.clear()
        # self.bitWidthType.setCurrentIndex(last_selected_bit)
        # time.sleep(0.1)
        with open(file_dir + 'configure.json') as file:
            data = json.load(file)
            bits = data["bits"]
            for e in bits:
                material_text = e["material"][0]
                root_item = QtGui.QStandardItem(material_text)
                self.m_model.appendRow(root_item)
                chipload_elements = e["chipload"]
                # feedrate_elements = e["feedrate"]
                # for text, chipload, feedrate in zip(bit_widths, chipload_elements, feedrate_elements):
                # , feedrate_elements):
                for text, chipload in zip(bit_widths, chipload_elements):
                    it = QtGui.QStandardItem(text)
                    it.setData(chipload, ChiploadRole)
                    # it.setData(feedrate, FeedrateRole)
                    root_item.appendRow(it)

        self.update_text()

    def hasNumbers(self, text):
        try:
            allowed = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-']
            if any(text in s for s in allowed):
                return False
            else:
                return True
        except ValueError:
            return False
        return False

    def import_config(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Import config file", '', "json Files (*.json)",
                                                  options=options)
        if not fileName:
            return
        with open(fileName) as file:
            data = json.load(file)
        with open(file_dir + 'configure.json', mode='w+') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        del materials[:]

        for bits in data['bits']:
            for material in bits['material']:
                materials.append(material)

        self.selected_material = materials[0]
        self.fill_model()
        self.update_text()

    def export_config(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save config file", "", "json Files (*.json)",
                                                  options=options)
        if not fileName:
            return
        if fileName.endswith('.json'):
            fileName = fileName.replace('.json', '')
        file = open(fileName + '.json', 'w+')
        file.close()
        with open(fileName + '.json', mode='w+', encoding='utf-8') as file:
            json.dump(current_data, file, ensure_ascii=False, indent=4)

    def update_text(self):
        # self.txtMaterial.setText(self.selected_material)
        # self.txtBitWidth.setText(self.selected_bit_width)
        self.txtChipLoad.setText(self.selected_chipload)
        self.txtFeedRate.setText(self.selected_feedrate)

    @pyqtSlot()
    def calculate(self):
        self.save_runtime_settings()
        # if second == True:
        #     if millimeters == True:
        #     elif meters == True:
        #     if inches == True:
        #     elif feet == True:
        # else:
        #     if millimeters == True:
        #     elif meters == True:
        #     if inches == True:
        #     elif feet == True:
        if self.txtRPM.text() == '' or self.txtFlute.text() == '':
            # buttonReply = QMessageBox.critical(self, 'Error!', 'Not inputs!', QMessageBox.Ok, QMessageBox.Ok)
            return
        try:
            split_chiploads = self.txtChipLoad.text().split('-')
            split_feedrates = self.txtFeedRate.text().split('-')
            # split_chiploads = self.txtChipLoad.text().split(',')
            # split_feedrates = self.txtFeedRate.text().split(',')

            temp = []
            for i, n in enumerate(split_chiploads):
                # split_feedrates = split_feedrates.replace(' ', '')
                # split_chiploads = split_chiploads.replace(' ', '')
                if not n == '':
                    # if imperial == True:
                    if millimeters == True:
                        if second == True:
                            result = float(n) * float(self.txtRPM.text()) * \
                                float(self.txtFlute.text()) * 25.4 / 60
                            self.txtFeedRate.setToolTip(
                                'Feed rate with that bit width and chipload. (mm/sec)')
                            self.lblcurrentSettings.setText('(mm/sec)')
                        elif minute == True:
                            result = float(n) * float(self.txtRPM.text()) * \
                                float(self.txtFlute.text()) * 25.4
                            self.txtFeedRate.setToolTip(
                                'Feed rate with that bit width and chipload. (mm/min)')
                            self.lblcurrentSettings.setText('(mm/min)')
                    elif meters == True:
                        if second == True:
                            result = float(n) * float(self.txtRPM.text()) * \
                                float(self.txtFlute.text()) * 0.0254 / 60
                            self.txtFeedRate.setToolTip(
                                'Feed rate with that bit width and chipload. (m/sec)')
                            self.lblcurrentSettings.setText('(m/sec)')
                        elif minute == True:
                            result = float(n) * float(self.txtRPM.text()) * \
                                float(self.txtFlute.text()) * 0.0254
                            self.txtFeedRate.setToolTip(
                                'Feed rate with that bit width and chipload. (m/min)')
                            self.lblcurrentSettings.setText('(m/min)')
                    elif inches == True:
                        if second == True:
                            result = float(
                                n) * float(self.txtRPM.text()) * float(self.txtFlute.text()) / 60
                            self.txtFeedRate.setToolTip(
                                'Feed rate with that bit width and chipload. (in/sec)')
                            self.lblcurrentSettings.setText('(in/sec)')
                        elif minute == True:
                            result = float(
                                n) * float(self.txtRPM.text()) * float(self.txtFlute.text())
                            self.txtFeedRate.setToolTip(
                                'Feed rate with that bit width and chipload. (in/min)')
                            self.lblcurrentSettings.setText('(in/min)')
                    elif feet == True:
                        if second == True:
                            result = float(n) * float(self.txtRPM.text()) * float(
                                self.txtFlute.text()) * 0.08333333 / 60
                            self.txtFeedRate.setToolTip(
                                'Feed rate with that bit width and chipload. (ft/sec)')
                            self.lblcurrentSettings.setText('(ft/sec)')
                        elif minute == True:
                            result = float(n) * float(self.txtRPM.text()) * \
                                float(self.txtFlute.text()) * 0.08333333
                            self.txtFeedRate.setToolTip(
                                'Feed rate with that bit width and chipload. (ft/min)')
                            self.lblcurrentSettings.setText('(ft/min)')
                    else:
                        # self.messageBox("No selections!")
                        return
                    # elif metric == True:
                    #     if millimeters == True:
                    #         if second == True:
                    #             result = float(n) * float(self.txtRPM.text()) * float(self.txtFlute.text()) / 60
                    #             self.txtFeedRate.setToolTip('Feed rate with that bit width and chipload. (mm/sec)')
                    #         elif minute == True:
                    #             result = float(n) * float(self.txtRPM.text()) * float(self.txtFlute.text())
                    #             self.txtFeedRate.setToolTip('Feed rate with that bit width and chipload. (mm/min)')
                    #     elif meters == True:
                    #         if second == True:
                    #             result = float(n) * float(self.txtRPM.text()) * float(self.txtFlute.text()) * 0.001 / 60
                    #             self.txtFeedRate.setToolTip('Feed rate with that bit width and chipload. (m/sec)')
                    #         elif minute == True:
                    #             result = float(n) * float(self.txtRPM.text()) * float(self.txtFlute.text()) * 0.001
                    #             self.txtFeedRate.setToolTip('Feed rate with that bit width and chipload. (m/min)')
                    #     elif inches == True:
                    #         if second == True:
                    #             result = float(n) * float(self.txtRPM.text()) * float(self.txtFlute.text()) * 0.03937008 / 60
                    #             self.txtFeedRate.setToolTip('Feed rate with that bit width and chipload. (in/sec)')
                    #         elif minute == True:
                    #             result = float(n) * float(self.txtRPM.text()) * float(self.txtFlute.text()) * 0.03937008
                    #             self.txtFeedRate.setToolTip('Feed rate with that bit width and chipload. (in/min)')
                    #     elif feet == True:
                    #         if second == True:
                    #             result = float(n) * float(self.txtRPM.text()) * float(self.txtFlute.text()) * 0.00328084 / 60
                    #             self.txtFeedRate.setToolTip('Feed rate with that bit width and chipload. (ft/sec)')
                    #         elif minute == True:
                    #             result = float(n) * float(self.txtRPM.text()) * float(self.txtFlute.text()) * 0.00328084
                    #             self.txtFeedRate.setToolTip('Feed rate with that bit width and chipload. (ft/min)')
                    #     else:
                    #         # self.messageBox("No selections!")
                    #         return
                    result = round(result, 3)
                    temp.append(str(result))

            r = ' - '.join(temp)
            self.selected_feedrate = str(temp)
            r = r.replace('[', '')
            r = r.replace(']', '')
            self.txtFeedRate.setText(r)
        except ValueError as e:
            self.messageBox("Invalid number!")


class drawProg(QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi('Bit_Config_Draw_GUI/mainwindow.ui', self)
        self.title = "CNC Bit Depth"
        # self.setMouseTracking(True)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon('icons/icon5.png'))

        # self.top= 150

        # self.left= 150

        # self.width = 500

        # self.height = 500

        # inches
        self.canvasSizeX = 800
        self.canvasSizeY = 600

        self.startPosX = 0
        self.startPosY = 1
        self.offset = 0

        self.useHeight = False

        self.height = 45
        self.width = 1
        self.side = 0
        self.degree = 45
        self.degree1 = 45

        self.thickness = 100
        self.thickness_side = 0
        self.thickness_depth = 0
        self.thickness_width = 0
        self.thickness_startPosY = 0
        self.thickness_startPosX = 0
        self.thickness_rect = 0
        self.thickness_dept_offset = 0

        self.numOfLayers = 3
        self.layerGap = 10
        self.stringLayersList = ''
        self.str_thickness_rect = ''
        self.scaleFactor = 200

        self.InitWindow()
        self.show()

    def InitWindow(self):
        # self.setGeometry(self.top, self.left, self.width, self.height)
        self.lblDrawGUI = self.findChild(QLabel, 'lblDrawGUI')
        self.canvas = QtGui.QPixmap(self.canvasSizeX, self.canvasSizeY)
        # self.canvas = self.canvas.scaled(self.canvasSizeX * 2, self.canvasSizeY * 2, Qt.KeepAspectRatio)
        # self.canvas = QtGui.QPixmap("").scaled(self.canvasSizeX, self.canvasSizeY, Qt.KeepAspectRatio,
        #                                              Qt.SmoothTransformation)
        # self.lblDrawGUI.setStyleSheet("QLabel {background-color: white; border: 1px solid "
        #                                "#01DFD7; border-radius: 5px;}")

        # self.canvas = QtGui.QPixmap(CHECK_ICON).scaled(20, 20, Qt.KeepAspectRatio,
        #                                       Qt.SmoothTransformation)
        self.lblDrawGUI.setPixmap(self.canvas)
        # self.lblDrawGUI.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        self.textEdit = self.findChild(QTextEdit, 'textEdit')

        self.sliderdepth = self.findChild(QSlider, 'sliderDepth')
        # self.sliderdepth.valueChanged.connect(self.SliderMovePosY)
        # self.sliderdepth.setMaximum(self.canvasSizeY / self.scaleFactor)
        # self.sliderdepth.setValue(self.startPosY)
        self.sliderdepth.setHidden(True)

        self.sliderStartPosX = self.findChild(QSlider, 'sliderX')
        # self.sliderStartPosX.valueChanged.connect(self.SliderMovePosX)
        # self.sliderStartPosX.setMaximum(
        #     self.canvasSizeX - self.width / self.scaleFactor)
        # self.sliderStartPosX.setValue(self.startPosX)
        self.sliderStartPosX.setHidden(True)

        self.checkBoxAuto = self.findChild(QCheckBox, 'checkBoxAuto')
        self.checkBoxAuto.stateChanged.connect(self.draw)
        # self.sliderDegree = self.findChild(QSlider, 'sliderDegree')
        # # self.sliderDegree.valueChanged.connect(self.sliderDegreeMove)
        # # self.sliderDegree.setMaximum(90)
        # # self.sliderDegree.setMinimum(10)
        # # self.sliderDegree.setValue(self.degree)

        self.sliderWidth = self.findChild(QSlider, 'sliderWidth')
        # self.sliderWidth.valueChanged.connect(self.sliderWidthMove)
        # self.sliderWidth.setMaximum(self.canvasSizeY / self.scaleFactor)
        # self.sliderWidth.setMinimum(10)
        # self.sliderWidth.setValue(self.width)
        self.sliderWidth.setHidden(True)

        self.sliderHeight = self.findChild(QSlider, 'sliderHeight')
        # self.sliderHeight.valueChanged.connect(self.sliderHeightMove)
        # self.sliderHeight.setMaximum(self.canvasSizeY / self.scaleFactor)
        # self.sliderHeight.setMinimum(1)
        # self.sliderHeight.setValue(self.height)
        self.sliderHeight.setHidden(True)

        self.inputDepth = self.findChild(QDoubleSpinBox, 'inputDepth')
        self.inputDepth.valueChanged.connect(self.inputDepthMove)

        self.inputX = self.findChild(QDoubleSpinBox, 'inputX')
        # self.inputX.valueChanged.connect(self.inputXMove)
        self.inputX.setHidden(True)

        self.inputNumOfLayers = self.findChild(QSpinBox, 'inputNumOfLayers')
        self.inputNumOfLayers.valueChanged.connect(self.inputNumOfLayersMove)

        self.inputLayerGap = self.findChild(QDoubleSpinBox, 'inputLayerGap')
        self.inputLayerGap.valueChanged.connect(self.inputLayerGapMove)
        self.inputOffset = self.findChild(QDoubleSpinBox, 'inputOffset')
        self.inputOffset.valueChanged.connect(self.inputOffsetMove)

        self.inputHeight = self.findChild(QDoubleSpinBox, 'inputHeight')
        self.inputHeight.valueChanged.connect(self.inputHeightMove)
        if self.useHeight:
            self.inputHeight.setMaximum(self.canvasSizeY / self.scaleFactor)
            self.inputHeight.setMinimum(1 / self.scaleFactor)
            self.inputHeightMove(self.height)
        else:
            self.inputHeight.setValue(45)
        # self.sliderHeightMove(self.height)

        self.inputWidth = self.findChild(QDoubleSpinBox, 'inputWidth')
        self.inputWidth.valueChanged.connect(self.inputWidthMove)
        self.inputWidth.setMaximum(self.canvasSizeX / self.scaleFactor)
        self.inputWidth.setMinimum(1 / self.scaleFactor)
        self.inputWidthMove(self.width)

        self.inputThickness = self.findChild(QDoubleSpinBox, 'inputThickness')
        self.inputThickness.valueChanged.connect(self.inputThicknessMove)
        self.inputThickness.setMaximum(self.canvasSizeY / self.scaleFactor / 2.2)
        self.inputThickness.setMinimum(0)

        self.sliderThickness = self.findChild(QSlider, 'sliderThickness')
        # self.sliderThickness.valueChanged.connect(self.sliderThicknessMove)
        # self.sliderThickness.setMaximum(self.canvasSizeY / 2)
        self.sliderThickness.setHidden(True)
        # self.inputDepth.setValue(1)
        # self.inputHeight.setValue(self.height)
        # self.inputWidth.setValue(self.width)
        self.check_height()
        self.draw()

    def draw(self):
        # self.lblDrawGUI.clear()
        painter = QtGui.QPainter(self.lblDrawGUI.pixmap())
        # painter.drawPixmap(0, 0, self.canvasSizeX * 2, self.canvasSizeY * 2, self.canvas.scaled(self.canvasSizeX * 2, self.canvasSizeY * 2, transformMode=QtCore.Qt.SmoothTransformation))
        # self.lblDrawGUI.setScaledContents(Qt.KeepAspectRatioBy)
        # painter.setRenderHint(QPainter.Antialiasing)
        # painter.begin(self)
        painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))

        painter.drawRect(0, 0, self.canvasSizeX - 1, self.canvasSizeY - 1)
        painter.setBrush(QBrush(QColor(116, 78, 26), Qt.SolidPattern))

        painter.drawRect(0, self.canvasSizeY - self.thickness,
                         self.canvasSizeX, self.canvasSizeY)
        # self.canvas.clear()
        painter.setBrush(Qt.white)
        painter.setBrush(QBrush(QColor(193, 193, 255), Qt.SolidPattern))
        # painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.moveTo(self.startPosX, self.startPosY)
        path.lineTo(self.startPosX + self.width,
                    self.startPosY)  # left to right
        path.lineTo(self.startPosX + self.width / 2,
                    self.startPosY + self.height)  # right down left
        path.lineTo(self.startPosX, self.startPosY)
        painter.drawPath(path)
        # painter.setWidth(1)

        # top
        # painter.drawLine(self.startPosX, self.startPosY, self.startPosX+self.width, self.startPosY)
        # # left
        # painter.drawLine(self.startPosX, self.startPosY, self.startPosX + (self.width/2), self.startPosY+self.height)
        # # right
        # painter.drawLine(self.startPosX + self.width, self.startPosY, self.startPosX + (self.width/2), self.startPosY+self.height)

        # draw side length
        painter.setPen(Qt.blue)
        painter.drawLine(self.startPosX - 20, self.startPosY, self.startPosX + (self.width / 2) - 20,
                         self.startPosY + self.height)
        painter.drawText(self.startPosX + self.width / 10, self.startPosY + (self.height / 2) - 10,
                         self.startPosX + self.width / 10, self.startPosY +
                         (self.height / 2), Qt.AlignLeft,
                         'a')
        # painter.setPen(QPen(Qt.green, 3, Qt.DotLine))

        painter.drawLine(self.startPosX + (self.width / 2) - 20,
                         self.startPosY + self.height, self.startPosX - 20, self.startPosY + self.height)
        # Width of bit
        painter.setPen(Qt.blue)
        painter.drawText(self.startPosX + (self.width / 2) - 10, self.startPosY - 20, self.startPosX + (self.width / 2),
                         self.startPosY, Qt.AlignLeft, 'c')
        # height of bit
        painter.setPen(Qt.blue)
        painter.drawText(self.startPosX - 40, self.startPosY + (self.height / 2) - 10, self.startPosX - 20,
                         self.startPosY + (self.height / 2), Qt.AlignLeft, 'h')
        painter.drawLine(self.startPosX - 20, self.startPosY,
                         self.startPosX - 20, self.startPosY + self.height)

        painter.setPen(Qt.black)
        # degree of bit
        painter.drawText(self.startPosX + (self.width / 2) - 10, self.startPosY + (self.height / 1.3) - 10,
                         self.startPosX +
                         (self.width / 2), self.startPosY +
                         (self.height / 1.3), Qt.AlignLeft,
                         'C')
        # depth of bit in wood
        self.stringLayersList = ''
        self.str_thickness_rect = ''
        painter.setPen(Qt.red)
        if (self.canvasSizeY - self.thickness) < self.startPosY + self.height and abs(
                (self.canvasSizeY - self.thickness) - (self.startPosY + self.height)) > 0.5:
            # c = √b2 + a2 - 2ba·cos(C) = 0.68404
            # print(round(self.solve_for_side(self.width, self.height), 3) - self.thickness_depth)
            if (self.startPosY < (self.canvasSizeY - self.thickness)):
                self.thickness_depth = round(
                    abs((self.canvasSizeY - self.thickness) - (self.startPosY + self.height)), 3)
            else:
                self.thickness_depth = self.height
            self.thickness_width = (
                self.thickness_depth / self.height) * self.width
            self.thickness_side = self.solve_for_side(
                self.thickness_width, self.thickness_depth)
            self.thickness_startPosX = self.startPosX + \
                (self.width - self.thickness_width) / 2
            self.thickness_startPosY = self.startPosY - \
                (self.thickness_depth - self.height)

            # thickness depth
            painter.drawLine(self.thickness_startPosX + self.thickness_width + 20, self.thickness_startPosY,
                             self.thickness_startPosX + self.thickness_width + 20, self.startPosY + self.height)
            painter.drawText(self.thickness_startPosX + self.thickness_width + 30,
                             self.thickness_startPosY +
                             (self.thickness_depth / 2),
                             self.thickness_startPosX + self.thickness_width + 30,
                             self.thickness_startPosY +
                             (self.thickness_depth / 2), Qt.AlignLeft,
                             'h')

            # thickness top width
            painter.setPen(Qt.red)
            painter.drawText(self.thickness_startPosX + (self.thickness_width / 2) - 10, self.thickness_startPosY - 20,
                             self.thickness_startPosX +
                             (self.thickness_width / 2),
                             self.thickness_startPosY, Qt.AlignLeft, 'c')
            # draw thickness side length
            painter.drawLine(self.thickness_startPosX + self.thickness_width + 20, self.thickness_startPosY,
                             self.thickness_startPosX +
                             (self.thickness_width / 2) + 20,
                             self.startPosY + self.height)
            painter.drawText(self.thickness_startPosX + self.thickness_width,
                             self.thickness_startPosY +
                             (self.thickness_depth / 2),
                             self.thickness_startPosX + self.thickness_width,
                             self.thickness_startPosY +
                             (self.thickness_depth / 2), Qt.AlignLeft,
                             'b')
            # draw thickness bottom
            painter.drawLine(self.thickness_startPosX + (self.thickness_width / 2) + 20,
                             self.startPosY + self.height, self.thickness_startPosX + self.thickness_width + 20,
                             self.startPosY + self.height)

            painter.setPen(Qt.black)
            painter.setBrush(QBrush(QColor(255, 97, 97), Qt.SolidPattern))
            path = QPainterPath()
            path.moveTo(self.thickness_startPosX, self.thickness_startPosY)
            path.lineTo(self.thickness_startPosX + self.thickness_width,
                        self.thickness_startPosY)  # left to right
            path.lineTo(self.thickness_startPosX + self.thickness_width / 2,
                        self.thickness_startPosY + self.thickness_depth)  # right down left
            path.lineTo(self.thickness_startPosX, self.thickness_startPosY)
            painter.drawPath(path)
            if (self.startPosY > (self.canvasSizeY - self.thickness)):
                path = QPainterPath()
                path.moveTo(self.startPosX, self.startPosY + 1)
                path.lineTo(self.startPosX,
                            (self.canvasSizeY - self.thickness))
                path.lineTo(self.startPosX + self.width,
                            (self.canvasSizeY - self.thickness))
                path.lineTo(self.startPosX + self.width, self.startPosY + 1)
                painter.drawPath(path)

                painter.setPen(Qt.magenta)
                self.thickness_rect = round(
                    abs((self.canvasSizeY - self.thickness) - self.startPosY), 3)
                painter.drawLine(self.startPosX + self.width + 20, self.canvasSizeY - self.thickness,
                                 self.startPosX + self.width + 20, self.canvasSizeY - self.thickness + self.thickness_rect)
                painter.drawText(self.startPosX + self.width + 40,
                                 self.canvasSizeY - self.thickness + self.thickness_rect / 2,
                                 self.startPosX + self.width + 50,
                                 self.canvasSizeY - self.thickness + self.thickness_rect / 2,
                                 Qt.AlignLeft,
                                 'h')
                self.str_thickness_rect = '<p style="color:magenta">h: ' + str(round(abs(self.thickness_rect / self.scaleFactor), 3)) + '"<br></p>'
            else: self.str_thickness_rect = ''
            if (self.numOfLayers != 0):
                if (self.checkBoxAuto.isChecked()):
                    self.layerGap = round(abs((self.canvasSizeY - self.thickness) - (self.thickness_startPosY + (
                        (self.canvasSizeY - self.thickness) - (self.startPosY + self.height)))) / self.numOfLayers, 3)
                    # self.layerGap = (round(abs((self.canvasSizeY - self.thickness) - (self.startPosY + self.height)), 3) / self.numOfLayers)
                    self.inputLayerGap.setValue(self.layerGap / self.scaleFactor)
                y = self.thickness_startPosY
                # painter.drawLine(self.thickness_startPosX, y,
                #                 self.thickness_startPosX + self.thickness_width, y)

                self.stringLayersList = ''
                self.stringLayersList += 'Depth (in) &nbsp;&nbsp;&nbsp;&nbsp; Diameter (in) &nbsp;&nbsp;&nbsp;&nbsp; Offset<br>'
                for i in range(self.numOfLayers):
                    y += self.layerGap
                    height = abs(y - self.thickness_startPosY - (self.thickness_depth))
                    try:
                        width = abs((height / self.height) * self.width)
                    except ZeroDivisionError:
                        height = 0.01
                        width = abs((height / self.height) * self.width)
                    temp_thick = (width - self.thickness_dept_offset) / self.scaleFactor
                    if temp_thick / self.scaleFactor <= 0: temp_thick = 0
                    self.stringLayersList += '{}.  {:12.3f}" &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {:12.3f} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {:12.3f}"<br>'.format(i + 1, round(abs(self.canvasSizeY - y - self.thickness) / self.scaleFactor, 3), round(width / self.scaleFactor, 3), round(temp_thick, 3))
                    # self.stringLayersList += f'{i + 1}.  {round(abs(self.canvasSizeY - y - self.thickness) / self.scaleFactor, 3)}" &nbsp;-&nbsp; {round(width/self.scaleFactor,3)}"<br>'
                    painter.setPen(QPen(Qt.black))
                    painter.drawLine((self.thickness_startPosX + self.thickness_width / 2 - width / 2),
                                    y, self.thickness_startPosX + self.thickness_width / 2 + width / 2, y)
                    # width = width - self.thickness_dept_offset
                    painter.setPen(QPen(Qt.cyan))
                    painter.drawLine((self.thickness_startPosX + self.thickness_width / 2 - temp_thick * self.scaleFactor / 2),
                                    y, self.thickness_startPosX + self.thickness_width / 2 + temp_thick * self.scaleFactor / 2, y)

                    painter.drawText(self.thickness_startPosX + self.thickness_width / 2 - width / 2 - 20, y - 5,
                                    self.thickness_startPosX +
                                    width, y -
                                    7, Qt.AlignLeft,
                                    f'{i + 1}.')

                self.stringLayersList += '<br>Depth (mm) &nbsp;&nbsp;&nbsp;&nbsp; Diameter (mm) &nbsp;&nbsp;&nbsp;&nbsp; Offset<br>'
                y = self.thickness_startPosY

                for i in range(self.numOfLayers):
                    y += self.layerGap
                    height = abs(y - self.thickness_startPosY - (self.thickness_depth))
                    # height = abs(self.canvasSizeY - self.thickness + y - (round(abs((self.canvasSizeY - self.thickness) - (self.startPosY + self.height)), 3)) - self.startPosY - self.height - self.canvasSizeY - self.thickness - self.startPosY)
                    try:
                        width = abs((height / self.height) * self.width)
                    except ZeroDivisionError:
                        height = 0.0001
                        width = abs((height / self.height) * self.width)
                    temp_thick = (width - self.thickness_dept_offset) / self.scaleFactor * 25.4
                    if temp_thick / self.scaleFactor <= 0: temp_thick = 0
                    self.stringLayersList += '{}.  {:12.3f}" &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {:12.3f} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {:12.3f}"<br>'.format(i + 1, round(abs(self.canvasSizeY - y - self.thickness) / self.scaleFactor * 25.4, 3), round(width * 25.4 / self.scaleFactor, 3), round(temp_thick, 3))

        # drawArc(x_axis, y_axis, width, length, startAngle, spanAngle)
        # painter.drawArc(100, 70, 300, 300, -(self.degree-self.degree)*16, self.degree * 16)
        # painter.drawArc(self.startPosX - (self.width / 2), self.startPosY - (self.height / 2) + self.height, 50, 50, 0*16, self.degree*16)

        painter.end()
        # QtCore.QMetaObject.connectSlotsByName(self)
        self.updateTextEdit()
        self.update()

        # time.sleep(0.001)

    def updateTextEdit(self):
        self.textEdit.setText('')
        self.textEdit.insertHtml(f'''
<p
style="color:blue">
h: {round(self.height / self.scaleFactor, 3)}"<br>
Volume: {round(self.solve_for_volume(self.width / self.scaleFactor, self.height / self.scaleFactor), 3)} in³<br>
Perimeter: {round((self.solve_for_side(self.width / self.scaleFactor, self.height / self.scaleFactor) * 2) + self.width / self.scaleFactor, 3)}"<br>
Surface Area: {round(self.solve_for_SA(self.width / self.scaleFactor, self.height / self.scaleFactor), 3)}<br>
Lateral Surface Area: {round(self.solve_for_LSA(self.width / self.scaleFactor, self.height / self.scaleFactor), 3)}<br>
Side a: {round(self.solve_for_side(self.width / self.scaleFactor, self.height / self.scaleFactor), 3)}"<br>
Side b: {round(self.solve_for_side(self.width / self.scaleFactor, self.height / self.scaleFactor), 3)}"<br>
Side c: {round(self.width, 3) / self.scaleFactor}"<br>
</p>

<p
style="color:red">
h: {round(self.thickness_depth / self.scaleFactor, 3)}"<br>
Volume: {round(self.solve_for_volume(self.thickness_width / self.scaleFactor, self.thickness_depth / self.scaleFactor), 3)} in³<br>
Perimeter: {round((self.solve_for_side(self.thickness_width / self.scaleFactor, self.thickness_depth / self.scaleFactor) * 2) + self.thickness_depth / self.scaleFactor, 3)}"<br>
Surface Area: {round(self.solve_for_SA(self.thickness_width / self.scaleFactor, self.thickness_depth / self.scaleFactor), 3)}<br>
Lateral Surface Area: {round(self.solve_for_LSA(self.thickness_width / self.scaleFactor, self.thickness_depth / self.scaleFactor), 3)}<br>
Side a: {round(self.solve_for_side(self.thickness_width / self.scaleFactor, self.thickness_depth / self.scaleFactor), 3)}"<br>
Side b: {round(self.solve_for_side(self.thickness_width / self.scaleFactor, self.thickness_depth / self.scaleFactor), 3)}"<br>
Side c: {round(self.thickness_width / self.scaleFactor, 3)}"<br>
</p>

<p
style="color:green">
Depth: {round(abs((self.canvasSizeY - self.thickness) - (self.startPosY + self.height)), 3) / self.scaleFactor}"<br>
Thickness: {round(self.thickness / self.scaleFactor,3)}"<br>
Angle A: {round(self.degree1, 3)}°<br>
Angle B: {round(self.degree1, 3)}°<br>
Angle C: {round(self.degree, 3)}°<br>
</p>

{self.str_thickness_rect}

<p
style="color:cyan">
{self.stringLayersList}
</p>
''')

    def SliderMovePosY(self, value):
        # self.startPosY = value * self.scaleFactor + self.offset
        # self.sliderDepth.setValue(self.startPosY)
        # self.check_height()
        self.draw()

    def SliderMovePosX(self, value):
        # self.startPosX = value * self.scaleFactor
        # self.inputX.setMaximum(
        #     self.canvasSizeX - self.width / self.scaleFactor - 40)
        # self.sliderStartPosX.setValue(self.startPosX)
        self.draw()

    def sliderDegreeMove(self, value):
        # self.degree = value / self.scaleFactor
        # self.inputDegree.setValue(self.degree)
        self.draw()

    def sliderHeightMove(self, value):
        # self.height = value * self.scaleFactor
        # self.inputHeight.setValue(self.height)
        # self.sliderdepth.setMinimum((self.canvasSizeY - self.thickness) - self.height / self.scaleFactor)
        # self.inputDepth.setMinimum(((self.canvasSizeY - self.thickness) - self.height) /self.scaleFactor)
        # self.solve_for_degree(self.solve_for_side(
            # self.width, self.height), self.width)
        # self.check_height()
        self.draw()

    def sliderWidthMove(self, value):
        # self.width = value * self.scaleFactor
        # self.inputWidth.setValue(self.width)
        # self.sliderStartPosX.setMaximum(self.canvasSizeX - self.width / self.scaleFactor)
        # self.inputX.setMaximum(
        #     (self.canvasSizeX - self.width) / self.scaleFactor)
        # self.solve_for_degree(self.solve_for_side(
        #     self.width, self.height), self.width)
        # self.check_height()
        self.draw()

    def sliderThicknessMove(self, value):
        # self.thickness = value * self.scaleFactor
        # self.check_height()
        # self.sliderThickness.setValue(self.thickness)
        self.draw()

    def inputDepthMove(self, value):
        self.startPosY = value * self.scaleFactor + self.offset
        # self.sliderDepth.setValue(self.startPosY)
        self.check_height()
        self.draw()

    def inputThicknessMove(self, value):
        self.thickness = value * self.scaleFactor
        self.check_height()
        # self.sliderThickness.setValue(self.thickness)
        self.draw()

    def inputXMove(self, value):
        self.startPosX = value * self.scaleFactor
        self.inputX.setMaximum(
            self.canvasSizeX - self.width / self.scaleFactor - 40)
        # self.sliderStartPosX.setValue(self.startPosX)
        self.draw()

    def inputHeightMove(self, value):
        # self.inputHeight.setValue(self.height)
        # self.sliderdepth.setMinimum((self.canvasSizeY - self.thickness) - self.height / self.scaleFactor)
        # self.inputDepth.setMinimum(((self.canvasSizeY - self.thickness) - self.height) /self.scaleFactor)
        if self.useHeight:
            self.height = value * self.scaleFactor
        else:
            inputDegree = value + (value)
            width = self.inputWidth.value()
            angleA = (math.radians(180) - math.radians(inputDegree)) / 2
            a, b, c, A, B, C = trianglesolver.solve(a=width, A=(inputDegree) * trianglesolver.degree, C=angleA)
            self.side = b
            area = (pow(self.side, 2) * math.sin(A)) / 2
            self.height = ((2 * area) / width) * self.scaleFactor
            self.degree1 = C / trianglesolver.degree
            self.degree = A / trianglesolver.degree
        self.check_height()
        self.draw()

    def inputWidthMove(self, value):
        self.width = value * self.scaleFactor
        # self.inputWidth.setValue(self.width)
        # self.sliderStartPosX.setMaximum(self.canvasSizeX - self.width / self.scaleFactor)
        # self.solve_for_degree(self.side, self.width / self.scaleFactor)
        self.inputHeightMove(self.inputHeight.value())
        self.inputX.setMaximum(
            (self.canvasSizeX - self.width) / self.scaleFactor)
        self.check_height()
        self.draw()

    def inputNumOfLayersMove(self, value):
        self.numOfLayers = value
        self.draw()

    def inputLayerGapMove(self, value):
        self.layerGap = value * self.scaleFactor
        self.draw()

    def inputOffsetMove(self, value):
        self.thickness_dept_offset = value * self.scaleFactor
        self.draw()

    def check_height(self):
        self.offset = abs(self.canvasSizeY - self.thickness - self.height)
        self.startPosY = self.inputDepth.value() * self.scaleFactor + self.offset
    # self.sliderdepth.setMinimum((self.canvasSizeY - self.thickness) - self.height/self.scaleFactor)
        # self.inputDepth.setMinimum()
        self.inputDepth.setMinimum((self.canvasSizeY - self.thickness - self.height - self.offset) / self.scaleFactor)
        self.startPosX = ((self.canvasSizeX / 2) -
                          (self.width / 2)) / self.scaleFactor
        self.inputXMove(self.startPosX)
        # if (self.height + (self.canvasSizeY - self.thickness)) < self.canvasSizeY:
        #     self.sliderdepth.setMaximum((self.canvasSizeY - self.thickness))
        #     self.inputDepth.setMaximum((self.canvasSizeY - self.thickness))
        # else:
        # self.sliderdepth.setMaximum(self.canvasSizeY - self.height/self.scaleFactor)
        self.inputDepth.setMaximum(
            (self.canvasSizeY - self.height - self.offset) / self.scaleFactor)

    def solve_for_SA(self, w, h):
        # l = math.sqrt((w/2) * (w/2) + h * h)
        return math.pi * (w / 2) * ((w / 2) + math.sqrt((w / 2) * (w / 2) + h * h))

    def solve_for_LSA(self, w, h):
        return math.pi * (w / 2 * math.sqrt((w / 2) * (w / 2) + h * h))

    def solve_for_volume(self, w, h):
        return round((1.0 / 3) * math.pi * (w / 2) * (w / 2) * h, 3)

    def solve_for_side(self, w, h):
        return math.hypot(w, h)

    def solve_for_degree(self, A, C):
        try:
            self.degree = math.degrees(
                math.acos((A * A + A * A - C * C) / (2.0 * A * A)))
            self.degree1 = math.degrees(
                math.acos((A * A + C * C - A * A) / (2.0 * A * C)))
        except Exception:
            return
# def mouseMoveEvent(self, event):
#     print('Mouse coords: ( %d : %d )' % (event.x(), event.y()))


class add_configuration(QDialog):

    def __init__(self, name):
        super().__init__()
        self.title = name
        # self.rad_metric_button = QRadioButton("Metric", self)
        # self.rad_imperial_button = QRadioButton("Imperial", self)
        self.txtMaterialName = QLineEdit(self)
        self.txtChipload1 = QLineEdit(self)
        self.txtChipload2 = QLineEdit(self)
        self.txtChipload3 = QLineEdit(self)
        self.txtChipload4 = QLineEdit(self)

        lblTip = QLabel(self)
        lblTip.setText(
            '*Seperate with \",\" to add more then one number. (Cannot add more then 5)')
        lblTip.move(0, 5)
        font = (QtGui.QFont('Calibri', 7))
        font.setItalic(True)
        lblTip.setFont(font)

        if imperial == True:
            lblMaterialName = QLabel(self)
            lblMaterialName.setText('Material Name:')
            lblMaterialName.move(10, 30)
            lblMaterialName.setFont(QtGui.QFont('Calibri', 14))

            lblChipload = QLabel(self)
            lblChipload.setText('Chipload for 1/8 Bit:')
            lblChipload.move(10, 80)
            lblChipload.setFont(QtGui.QFont('Calibri', 11))

            lblChipload = QLabel(self)
            lblChipload.setText('Chipload for 1/4 Bit:')
            lblChipload.move(10, 130)
            lblChipload.setFont(QtGui.QFont('Calibri', 11))

            lblChipload = QLabel(self)
            lblChipload.setText('Chipload for 3/8 Bit:')
            lblChipload.move(10, 180)
            lblChipload.setFont(QtGui.QFont('Calibri', 11))

            lblChipload = QLabel(self)
            lblChipload.setText('Chipload for 1/2 Bit:')
            lblChipload.move(10, 230)
            lblChipload.setFont(QtGui.QFont('Calibri', 11))
        elif metric == True:
            lblMaterialName = QLabel(self)
            lblMaterialName.setText('Material Name:')
            lblMaterialName.move(10, 35)
            lblMaterialName.setFont(QtGui.QFont('Calibri', 14))

            lblChipload = QLabel(self)
            lblChipload.setText('Chipload for 3.175mm Bit:')
            lblChipload.move(10, 85)
            lblChipload.setFont(QtGui.QFont('Calibri', 9))

            lblChipload = QLabel(self)
            lblChipload.setText('Chipload for 6.35mm Bit:')
            lblChipload.move(10, 135)
            lblChipload.setFont(QtGui.QFont('Calibri', 9))

            lblChipload = QLabel(self)
            lblChipload.setText('Chipload for 9.525mm Bit:')
            lblChipload.move(10, 185)
            lblChipload.setFont(QtGui.QFont('Calibri', 9))

            lblChipload = QLabel(self)
            lblChipload.setText('Chipload for 12.7mm Bit:')
            lblChipload.move(10, 235)
            lblChipload.setFont(QtGui.QFont('Calibri', 9))
        f = self.txtChipload1.font()
        f.setPointSize(10)
        self.txtMaterialName.setFont(f)
        self.txtMaterialName.setText('')
        self.txtMaterialName.setAlignment(Qt.AlignCenter)
        self.txtMaterialName.move(150, 20)
        self.txtMaterialName.resize(150, 50)
        self.txtMaterialName.setToolTip(
            'The name of the material you want to add.')

        regexp = QtCore.QRegExp(
            '[0-9.9]{1,100}[,][0-9.9]{1,100}[,][0-9.9]{1,100}[,][0-9.9]{1,100}[,][0-9.9]{1,100}')
        validator = QtGui.QRegExpValidator(regexp)
        f = self.txtChipload1.font()
        f.setPointSize(10)
        self.txtChipload1.setFont(f)
        self.txtChipload1.setText('')
        self.txtChipload1.setAlignment(Qt.AlignCenter)
        # self.txtChipload1.textChanged.connect(self.calculate)
        self.txtChipload1.move(150, 70)
        self.txtChipload1.resize(150, 50)
        self.txtChipload1.setValidator(validator)
        if imperial == True:
            self.txtChipload1.setToolTip('Chipload for 1/8 bit')
        elif metric == True:
            self.txtChipload1.setToolTip('Chipload for 3.175mm bit')

        f = self.txtChipload2.font()
        f.setPointSize(10)
        self.txtChipload2.setFont(f)
        self.txtChipload2.setText('')
        self.txtChipload2.setAlignment(Qt.AlignCenter)
        # self.txtChipload2.textChanged.connect(self.calculate)
        self.txtChipload2.move(150, 120)
        self.txtChipload2.resize(150, 50)
        self.txtChipload2.setValidator(validator)
        if imperial == True:
            self.txtChipload2.setToolTip('Chipload for 1/4 bit')
        elif metric == True:
            self.txtChipload2.setToolTip('Chipload for 6.35mm bit')

        f = self.txtChipload3.font()
        f.setPointSize(10)
        self.txtChipload3.setFont(f)
        self.txtChipload3.setText('')
        self.txtChipload3.setAlignment(Qt.AlignCenter)
        # self.txtChipload3.textChanged.connect(self.calculate)
        self.txtChipload3.move(150, 170)
        self.txtChipload3.resize(150, 50)
        self.txtChipload3.setValidator(validator)
        if imperial == True:
            self.txtChipload3.setToolTip('Chipload for 3/8 bit')
        elif metric == True:
            self.txtChipload3.setToolTip('Chipload for 9.525mm bit')

        f = self.txtChipload4.font()
        f.setPointSize(10)
        self.txtChipload4.setFont(f)
        self.txtChipload4.setText('')
        self.txtChipload4.setAlignment(Qt.AlignCenter)
        # self.txtChipload4.textChanged.connect(self.calculate)
        self.txtChipload4.move(150, 220)
        self.txtChipload4.resize(150, 50)
        self.txtChipload4.setValidator(validator)
        if imperial == True:
            self.txtChipload4.setToolTip('Chipload for 1/2 bit')
        elif metric == True:
            self.txtChipload4.setToolTip('Chipload for 12.7mm bit')

        btnSave = QPushButton('Save', self)
        btnSave.move(0, 270)
        btnSave.resize(150, 40)
        btnSave.setFont(QtGui.QFont('Calibri', 15))
        btnSave.clicked.connect(self.save)
        btnSave.setToolTip('Add the material.')

        btnClose = QPushButton('Close', self)
        btnClose.move(150, 270)
        btnClose.resize(150, 40)
        btnClose.setFont(QtGui.QFont('Calibri', 15))
        btnClose.clicked.connect(self.closeWindow)
        btnClose.setToolTip('Close')

    def save(self):
        if self.txtMaterialName.text() == '' or self.txtChipload1.text() == '' or self.txtChipload2.text() == '' or self.txtChipload3.text() == '' or self.txtChipload4.text() == '':
            buttonReply = QMessageBox.critical(
                self, 'Error!', 'No inputs!', QMessageBox.Ok, QMessageBox.Ok)
            return
        feedrateArr = []
        chiploadArr = []
        # choice = QMessageBox.question(self, 'Exit!',
        #                                 "Are you sure you want to exit?",
        #                                 QMessageBox.Yes | QMessageBox.No,
        #                                 QMessageBox.No)
        # if choice == QMessageBox.No:
        #     self.close
        input_material = self.txtMaterialName.text()
        input_chip_load1 = self.txtChipload1.text()
        input_chip_load2 = self.txtChipload2.text()
        input_chip_load3 = self.txtChipload3.text()
        input_chip_load4 = self.txtChipload4.text()

        input_chip_load1 = input_chip_load1.replace(' ', '')
        input_chip_load1 = input_chip_load1.replace(',', ' - ')
        input_chip_load2 = input_chip_load2.replace(' ', '')
        input_chip_load2 = input_chip_load2.replace(',', ' - ')
        input_chip_load3 = input_chip_load3.replace(' ', '')
        input_chip_load3 = input_chip_load3.replace(',', ' - ')
        input_chip_load4 = input_chip_load4.replace(' ', '')
        input_chip_load4 = input_chip_load4.replace(',', ' - ')

        # if not self.hasNumbers(input_chip_load):
        #     i = i - 1
        chiploadArr.append(str(input_chip_load1))
        chiploadArr.append(str(input_chip_load2))
        chiploadArr.append(str(input_chip_load3))
        chiploadArr.append(str(input_chip_load4))
        r = ', '.join(feedrateArr)
        r1 = ', '.join(chiploadArr)
        if imperial == True:
            buttonReply = QMessageBox.question(self,
                                               'Are you sure you want to save {}?'.format(
                                                   input_material),
                                               "Material: {}\nChipload: \n1/8\" bit: {}\n1/4\" bit: {}\n3/8\" bit: {}\n1/2\" bit: {}".format(
                                                   input_material, input_chip_load1, input_chip_load2, input_chip_load3,
                                                   input_chip_load4),
                                               QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.No)
            if buttonReply == QMessageBox.No:
                return
        elif metric == True:
            buttonReply = QMessageBox.question(self,
                                               'Are you sure you want to save {}?'.format(
                                                   input_material),
                                               "Material: {}\nChipload: \n3.175mm bit: {}\n6.35mm bit: {}\n9.525mm bit: {}\n12.7mm bit: {}".format(
                                                   input_material, input_chip_load1, input_chip_load2, input_chip_load3,
                                                   input_chip_load4),
                                               QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.No)
            if buttonReply == QMessageBox.No:
                return
        current_data['bits'].append(
            {
                'material': ['{}'.format(input_material)],
                'chipload': chiploadArr,
                # 'feedrate': feedrateArr
            })
        with open(file_dir + 'configure.json', mode='w+', encoding='utf-8') as file:
            json.dump(current_data, file, ensure_ascii=False, indent=4)
        with open(file_dir + 'configure.json') as file:
            data = json.load(file)

        del materials[:]

        for bits in data['bits']:
            for material in bits['material']:
                materials.append(material)

        App()
        self.close()

    def closeWindow(self):
        App().calculate()
        self.close()


class options_menu(QDialog):

    def __init__(self, name):
        super().__init__()
        self.title = name
        self.rad_metric_button = QRadioButton("Metric", self)
        self.rad_imperial_button = QRadioButton("Imperial", self)

        self.rad_inches_button = QRadioButton("Inches", self)
        self.rad_feet_button = QRadioButton("Feet", self)
        self.rad_millimeters_button = QRadioButton("Millimeters", self)
        self.rad_meters_button = QRadioButton("Meters", self)

        self.rad_minute_button = QRadioButton("per minute", self)
        self.rad_second_button = QRadioButton("per second", self)

        self.createTopLeftGroupBox()
        self.createBotRightGroupBox()
        self.createTopRightGroupBox()
        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.botRightGroupBox, 0, 1)
        mainLayout.addWidget(self.topRightGroupBox, 0, 0)

        btnApplySave = QPushButton('Apply && Save', self)
        btnApplySave.move(150, 160)
        btnApplySave.resize(145, 40)
        btnApplySave.setFont(QtGui.QFont('Calibri', 15))
        btnApplySave.clicked.connect(self.apply_and_save)
        btnApplySave.setToolTip('Apply the current settings and save them.')

        btnClose = QPushButton('Close', self)
        btnClose.move(150, 200)
        btnClose.resize(145, 40)
        btnClose.setFont(QtGui.QFont('Calibri', 15))
        btnClose.clicked.connect(self.Close)
        btnClose.setToolTip('Close')

    def Close(self):
        App()
        self.close()

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Measurements")

        # self.rad_millimeters_button.toggled.connect(self.btnstate)
        self.rad_millimeters_button.setChecked(millimeters)
        # self.rad_inches_button.toggled.connect(self.btnstate)
        self.rad_inches_button.setChecked(inches)
        # self.rad_meters_button.toggled.connect(self.btnstate)
        self.rad_meters_button.setChecked(meters)
        # self.rad_feet_button.toggled.connect(self.btnstate)
        self.rad_feet_button.setChecked(feet)

        layout = QVBoxLayout()
        layout.addWidget(self.rad_millimeters_button)
        layout.addWidget(self.rad_meters_button)
        layout.addWidget(self.rad_inches_button)
        layout.addWidget(self.rad_feet_button)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def createBotRightGroupBox(self):
        self.botRightGroupBox = QGroupBox("Time")
        self.rad_minute_button.setChecked(minute)
        # self.rad_minute_button.toggled.connect(self.btnstate)
        self.rad_second_button.setChecked(second)
        # self.rad_second_button.toggled.connect(self.btnstate)
        # if self.rad_minute_button.isChecked() == False and self.rad_second_button.isChecked() == False:
        #     self.rad_second_button.setChecked(second)
        #     self.rad_minute_button.setChecked(minute)
        layout = QVBoxLayout()
        layout.addWidget(self.rad_minute_button)
        layout.addWidget(self.rad_second_button)
        layout.addStretch(1)
        self.botRightGroupBox.setLayout(layout)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Display numbers in")
        self.rad_imperial_button.setChecked(imperial)
        # self.rad_minute_button.toggled.connect(self.btnstate)
        self.rad_metric_button.setChecked(metric)
        # self.rad_second_button.toggled.connect(self.btnstate)
        # if self.rad_minute_button.isChecked() == False and self.rad_second_button.isChecked() == False:
        #     self.rad_second_button.setChecked(second)
        #     self.rad_minute_button.setChecked(minute)
        layout = QVBoxLayout()
        layout.addWidget(self.rad_imperial_button)
        layout.addWidget(self.rad_metric_button)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def apply_and_save(self):
        if self.rad_feet_button.isChecked() == False and self.rad_inches_button.isChecked() == False and self.rad_meters_button.isChecked() == False and self.rad_millimeters_button.isChecked() == False:
            buttonReply = QMessageBox.critical(
                self, 'Error!', 'No inputs!', QMessageBox.Ok, QMessageBox.Ok)
            return
        self.btnstate()
        App().calculate()
        self.save_settings()
        self.close()

    def save_settings(self):
        current_settings = {
            'imperial': '{}'.format(imperial),
            'metric': '{}'.format(metric),
            'minute': '{}'.format(minute),
            'second': '{}'.format(second),
            'millimeter': '{}'.format(millimeters),
            'meter': '{}'.format(meters),
            'inch': '{}'.format(inches),
            'feet': '{}'.format(feet)
        }
        with open(file_dir + 'settings.json', mode='w+', encoding='utf-8') as file:
            json.dump(current_settings, file, ensure_ascii=False, indent=4)
        with open(file_dir + 'settings.json') as file:
            settings = json.load(file)

    def btnstate(self):
        global imperial
        global metric
        global minute
        global second
        global millimeters
        global meters
        global inches
        global feet
        if self.rad_imperial_button.isChecked() == True:
            imperial = True
        else:
            imperial = False

        if self.rad_metric_button.isChecked() == True:
            metric = True
        else:
            metric = False

        if self.rad_minute_button.isChecked() == True:
            minute = True
        else:
            minute = False

        if self.rad_second_button.isChecked() == True:
            second = True
        else:
            second = False
        if self.rad_millimeters_button.isChecked() == True:
            millimeters = True
        else:
            millimeters = False
        if self.rad_meters_button.isChecked() == True:
            meters = True
        else:
            meters = False
        if self.rad_inches_button.isChecked() == True:
            inches = True
        else:
            inches = False
        if self.rad_feet_button.isChecked() == True:
            feet = True
        else:
            feet = False


class contact_menu(QDialog):

    def __init__(self, name):
        super().__init__()
        self.title = name
        regexp = QtCore.QRegExp(
            '^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$')
        validator = QtGui.QRegExpValidator(regexp)
        self.lblContactEmail = QLabel("Name*", self)
        self.lblContactEmail.move(5, 0)

        self.txtName = QLineEdit(self)
        self.txtName.move(0, 15)
        self.txtName.resize(100, 20)

        self.lblContactEmail = QLabel("Your Email*", self)
        self.lblContactEmail.move(5, 40)

        self.txtContactEmail = QLineEdit(self)
        self.txtContactEmail.move(0, 55)
        self.txtContactEmail.resize(150, 20)
        # self.txtContactEmail.setValidator(validator)

        self.lblText = QLabel('Text*', self)
        self.lblText.move(5, 80)

        self.txtText = QPlainTextEdit(self)
        self.txtText.move(0, 100)
        self.txtText.resize(300, 150)
        # self.txtText.insertPlainText("You can write text here.\n")

        self.btnSend = QPushButton('Send', self)
        self.btnSend.setFont(QtGui.QFont('Calibri', 15))
        self.btnSend.clicked.connect(self.send_email)
        self.btnSend.setToolTip('Sends email.')
        self.btnSend.resize(120, 40)
        self.btnSend.move(180, 20)

        btnClose = QPushButton('Close', self)
        btnClose.move(180, 60)
        btnClose.resize(120, 40)
        btnClose.setFont(QtGui.QFont('Calibri', 15))
        btnClose.clicked.connect(self.Close)
        btnClose.setToolTip('Close')

    def isValidEmail(self, email):
        if len(email) > 7:
            lst = re.findall('\S+@\S+', email)
            if len(lst) == 1:
                return True
        return False

    def Close(self):
        App()
        self.close()

    def send_email(self):
        if self.txtName.text() == '' or self.txtContactEmail.text() == '' or self.txtText.document().toPlainText() == '':
            buttonReply = QMessageBox.critical(
                self, 'Oh oh! :(', 'Invalid Entry.', QMessageBox.Ok, QMessageBox.Ok)
            return

        if not self.isValidEmail(self.txtContactEmail.text()) == True:
            buttonReply = QMessageBox.critical(self, 'Oh oh! :(',
                                               '{} is not a valid Email!'.format(
                                                   self.txtContactEmail.text()),
                                               QMessageBox.Ok, QMessageBox.Ok)
            return

        gmail_user = 'jaredgrozz@gmail.com'
        gmail_password = 'ffvprugomuuywemq'
        sent_from = gmail_user
        text = self.txtText.document().toPlainText()
        to = ['jaredgrozz@gmail.com']
        subject = '{} from: {}'.format(
            self.txtName.text(), self.txtContactEmail.text())
        text += '\n\nContact Email: {}\nProgram name: {} {}\nHardware Specs:\nMachine:{}\nVersion:{}\nPlatform:{}\nname:{}\nSystem:{}\nProcesser:{}'.format(
            self.txtContactEmail.text(), title, version, platform.machine(
            ), platform.version(), platform.platform(),
            platform.uname(), platform.system(), platform.processor())

        body = text

        email_text = "From: {0}\nTo: {1}\nSubject: {2}\n{3}".format(
            sent_from, self.txtName.text(), subject, body)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, email_text)
            server.close()
            buttonReply = QMessageBox.information(self, 'Email Sent! :)', 'We will respond to the email:\n{}'.format(
                self.txtContactEmail.text()), QMessageBox.Ok, QMessageBox.Ok)
            App()
            self.close()
        except Exception as e:
            buttonReply = QMessageBox.critical(
                self, 'Oh no! :(', '{}'.format(e), QMessageBox.Ok, QMessageBox.Ok)
            App()
            self.close()


class tips_menu(QDialog):

    def __init__(self, name):
        super().__init__()
        self.title = name
        self.txtText = QPlainTextEdit(self)
        self.txtText.move(0, 0)
        self.txtText.resize(300, 250)
        self.txtText.document().setPlainText(
            'Tip #1 Want to improve your bit life? The key for a long lasting bit life is giving it a cool life, use infared digital thermometer and keep an eye on its temperature, typically beyween 23 to 35 degrees celsius but can varry between types of materials.\n\nTip #2 Higher chipload = cooler bit life, but also can cause ripping, chipping and whipping.\n\nTip #3 lower chipload = finner and hotter cuts, hotter? Yes heat destroys bit life... be carful now. Running large nested files/sheets will heat your bit up and damage its cutting edge.')
        self.txtText.setReadOnly(True)


class calculate_chipload_menu(QDialog):

    def __init__(self, name):
        super().__init__()
        self.title = name

        self.lblFeedrate = QLabel(self)
        self.lblFeedrate.setText('Feedrate:')
        self.lblFeedrate.move(5, 5)
        self.lblFeedrate.setFont(QtGui.QFont('Calibri', 16))

        self.lblRPM = QLabel(self)
        self.lblRPM.setText('RPM:')
        self.lblRPM.move(5, 45)
        self.lblRPM.setFont(QtGui.QFont('Calibri', 16))

        self.lblFlute = QLabel(self)
        self.lblFlute.setText('Flute:')
        self.lblFlute.move(5, 85)
        self.lblFlute.setFont(QtGui.QFont('Calibri', 16))

        # self.lblFBitDiameter = QLabel(self)
        # self.lblFBitDiameter.setText('Bit Diameter:')
        # self.lblFBitDiameter.move(5,133)
        # self.lblFBitDiameter.setFont(QtGui.QFont('Calibri', 12))

        self.lblChipload = QLabel(self)
        self.lblChipload.setText('Chipload:')
        self.lblChipload.move(5, 210)
        self.lblChipload.setFont(QtGui.QFont('Calibri', 16))

        self.txtFeedrate = QLineEdit(self)
        self.txtFeedrate.setText('600')
        self.txtFeedrate.move(110, 5)
        self.txtFeedrate.resize(100, 40)
        self.txtFeedrate.setAlignment(Qt.AlignCenter)
        self.txtFeedrate.setValidator(QtGui.QDoubleValidator(0, 100000, 3))
        self.txtFeedrate.textChanged.connect(self.calculate)
        self.txtFeedrate.setToolTip('The feed rate')

        self.txtRPM = QLineEdit(self)
        self.txtRPM.setText('18000')
        self.txtRPM.move(110, 45)
        self.txtRPM.resize(100, 40)
        self.txtRPM.setAlignment(Qt.AlignCenter)
        self.txtRPM.setValidator(QtGui.QDoubleValidator(0, 100000, 3))
        self.txtRPM.textChanged.connect(self.calculate)
        self.txtRPM.setToolTip('The bits Revolutions Per Minute')

        self.txtFlute = QLineEdit(self)
        self.txtFlute.setText('2')
        self.txtFlute.move(110, 85)
        self.txtFlute.resize(100, 40)
        self.txtFlute.setAlignment(Qt.AlignCenter)
        self.txtFlute.setValidator(QtGui.QDoubleValidator(0, 100000, 3))
        self.txtFlute.textChanged.connect(self.calculate)
        self.txtFlute.setToolTip('How many edges the bit has count.')

        # self.txtBitDiameter = QLineEdit(self)
        # self.txtBitDiameter.setText('0.375')
        # self.txtBitDiameter.move(110,125)
        # self.txtBitDiameter.resize(100,40)
        # self.txtBitDiameter.setAlignment(Qt.AlignCenter)
        # self.txtBitDiameter.setValidator(QtGui.QDoubleValidator(0,100000,3))
        # self.txtBitDiameter.textChanged.connect(self.calculate)
        # self.txtBitDiameter.setToolTip('The bit diameter in inches.')

        self.txtChipload = QLineEdit(self)
        self.txtChipload.move(110, 205)
        self.txtChipload.resize(100, 40)
        self.txtChipload.setAlignment(Qt.AlignCenter)
        self.txtChipload.setValidator(QtGui.QDoubleValidator(0, 100000, 3))
        self.txtChipload.setReadOnly(True)
        self.txtChipload.setToolTip('(inches) the calculated chipload.')

        self.calculate()

    def calculate(self):
        try:
            flute = self.txtFlute.text()
            rpm = self.txtRPM.text()
            feedrate = self.txtFeedrate.text()
            # or self.txtBitDiameter.text() == '':
            if self.txtFlute.text() == '' or self.txtRPM.text() == '' or self.txtFeedrate == '':
                return
            result = float(self.txtFeedrate.text()) / \
                float(self.txtRPM.text()) / float(self.txtFlute.text())
            # result = float(self.txtFeedrate.text()) / float(1200 * 3.82 / float(self.txtBitDiameter.text())) / float(self.txtFlute.text())
            result = round(result, 3)
            self.txtChipload.setText(str(result))
        except:
            buttonReply = QMessageBox.critical(
                self, 'Oh oh! :(', 'Not a number.', QMessageBox.Ok, QMessageBox.Ok)

            flute = flute.replace(',', '')
            rpm = rpm.replace(',', '')
            feedrate = feedrate.replace(',', '')

            flute = flute.replace('e', '')
            rpm = rpm.replace('e', '')
            feedrate = feedrate.replace('e', '')

            flute = flute.replace('E', '')
            rpm = rpm.replace('E', '')
            feedrate = feedrate.replace('E', '')

            self.txtFlute.setText(flute)
            self.txtRPM.setText(rpm)
            self.txtFeedrate.setText(feedrate)
            self.calculate()
            return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = App()
    # QApplication.setPalette(QApplication.style().standardPalette())
    # app.setStyle('Windows Vista')
    main_window.show()
    sys.exit(app.exec_())
