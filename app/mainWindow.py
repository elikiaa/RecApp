# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mainRecApp.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


import os, serial
from serial.tools.list_ports import comports

from PyQt5 import QtCore, QtGui, QtWidgets
from app.recordWindow import Ui_Form


# create ComboBox from QComboBox to update item list on click 
class ComboBox(QtWidgets.QComboBox):
    popupAboutToBeShown = QtCore.pyqtSignal()

    def showPopup(self):
        self.popupAboutToBeShown.emit()
        super(ComboBox, self).showPopup()

class Ui_MainWindow(object):
    def __init__(self):
        self.portDropdown = ComboBox()
        #self.portDropdown.popupAboutToBeShown.connect(self.get_ports)
        self.current_port = ''
        self.filepath=r'C:\Users\hella\Desktop'
        self.filename='sig_out.xlsx'
        self.ports = []

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(663, 333)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

    # Part 1: Choose Port (Label, ComboBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.portLbl = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Verdana Pro")
        font.setPointSize(10)
        self.portLbl.setFont(font)
        self.portLbl.setObjectName("portLbl")
        self.portLbl.setFixedWidth(125)
        self.portLbl.setFixedHeight(30)
        self.horizontalLayout.addWidget(self.portLbl, QtCore.Qt.AlignLeft)
        self.portDropdown.setMaximumSize(QtCore.QSize(100, 30))
        self.portDropdown.setEditable(True)
        self.portDropdown.setIconSize(QtCore.QSize(16, 16))
        self.portDropdown.setObjectName("portDropdown")
        # list of available ports
        self.get_ports()
        self.horizontalLayout.addWidget(self.portDropdown)
        self.portStat = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Verdana Pro")
        font.setPointSize(8)
        self.portStat.setFont(font)
        self.portStat.setObjectName("portStat")
        self.portStat.setFixedHeight(30)
        self.horizontalLayout.addWidget(self.portStat, QtCore.Qt.AlignLeft)
        self.horizontalLayout.addStretch()
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

    # Part 2: Dateiname
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.filenameLbl = QtWidgets.QLabel(self.centralwidget)        
        font = QtGui.QFont()
        font.setFamily("Verdana Pro")
        font.setPointSize(10)
        self.filenameLbl.setFont(font)
        self.filenameLbl.setObjectName("filenameLbl")
        self.filenameLbl.setFixedWidth(130)
        self.horizontalLayout_4.addWidget(self.filenameLbl, QtCore.Qt.AlignLeft)
        self.filenameLE = QtWidgets.QLineEdit(self.centralwidget)
        self.filenameLE.setFixedHeight(30)
        self.filenameLE.setFixedWidth(350)
        self.filenameLE.setObjectName("filenameLE")
        self.horizontalLayout_4.addWidget(self.filenameLE, QtCore.Qt.AlignLeft)
        self.horizontalLayout_4.addStretch()
        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)

    # Part 3: Speicherort
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.fileLbl = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Verdana Pro")
        font.setPointSize(10)
        self.fileLbl.setFont(font)
        self.fileLbl.setObjectName("fileLbl")
        self.fileLbl.setFixedWidth(124)
        self.horizontalLayout_2.addWidget(self.fileLbl, QtCore.Qt.AlignLeft)
        self.filepathTB = QtWidgets.QTextBrowser(self.centralwidget)
        self.filepathTB.setFixedHeight(30)
        self.filepathTB.setFixedWidth(480)
        self.filepathTB.setObjectName("filepathTB")
        self.horizontalLayout_2.addWidget(self.filepathTB, QtCore.Qt.AlignLeft)
        self.fileBtn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Verdana Pro")
        font.setPointSize(10)
        self.fileBtn.setFont(font)
        self.fileBtn.setObjectName("fileBtn")
        self.horizontalLayout_2.addWidget(self.fileBtn)
        self.horizontalLayout_2.addStretch()
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

    # Part 4: Messungen starten
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.startRecBtn = QtWidgets.QPushButton(self.centralwidget)
        self.startRecBtn.setFixedWidth(250)
        self.startRecBtn.setFixedHeight(70)
        font = QtGui.QFont()
        font.setFamily("Verdana Pro")
        font.setPointSize(12)
        self.startRecBtn.setFont(font)
        self.startRecBtn.setObjectName("startRecBtn")
        self.horizontalLayout_3.addWidget(self.startRecBtn, QtCore.Qt.AlignCenter)
        self.horizontalLayout_3.addStretch()
        self.gridLayout.addLayout(self.horizontalLayout_3, 4, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.serstatus = QtWidgets.QLabel("Serial Status: Disconnected")
        self.statusbar.addWidget(self.serstatus)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #self.startRecBtn.clicked.connect(self.start_serial_connection)
        #self.startRecBtn.clicked.connect(self.record_screen)
        #self.startRecBtn.clicked.connect(self.ui.start_recording)
        #self.fileBtn.clicked.connect(self.select_loc)
        #self.filenameLE.textEdited.connect(self.get_filename)
        #self.portDropdown.popupAboutToBeShown.connect(self.get_ports)
        #self.portDropdown.activated.connect(self.get_current_port)
        
    def get_ports(self):
        self.ports = list(comports())
        self.portDropdown.clear()
        self.portDropdown.addItems([p[0] for p in self.ports])
        if len(self.ports) == 0:
            try:
                self.portStat.setText('No ports available.')
            except Exception:
                pass
        else:
            self.portDropdown.setCurrentIndex(0)
            self.current_port = self.portDropdown.currentText()
            try:
                self.portStat.setText('')
                
            except Exception:
                pass    

    def select_loc(self):
        self.filepath = QtWidgets.QFileDialog.getExistingDirectory(None, 'Speichern unter')
        self.filepathTB.setText(self.filepath)

    def get_filename(self):
        if self.filenameLE.text() == '':
            return self.filename
        return self.filenameLE.text()

    def get_filepath(self):
        if self.filepathTB.toPlainText() == '':
            return self.filepath
        return str(self.filepathTB.toPlainText())

    def set_filename(self):
        self.filename = self.filenameLE.text()

    def get_current_port(self):
        return str(self.portDropdown.currentText())
    
    def set_current_port(self):
        self.current_port = str(self.portDropdown.currentText())

    def _get_serial(self):
        return self.ser

    def _start_serial_connection(self, baudrate):
        try:
            # pySerial timeout=None:  wait forever / until requested number of bytes are received
            self.ser = serial.Serial(self.get_current_port(), baudrate, timeout=None)  
        except Exception:
           self.serstatus.setText("Serial Status: Failed to open port {}".format(self.get_current_port()))
        else:
            self.serstatus.setText("Serial Status: Port {} opened".format(self.get_current_port()))
            self.serial_connection  = True



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EMG Signal Acquisition"))
        self.portLbl.setText(_translate("MainWindow", "Port"))
        self.portStat.setText(_translate("MainWindow", ""))
        self.fileLbl.setText(_translate("MainWindow", "Speicherort"))
        self.fileBtn.setText(_translate("MainWindow", "Durchsuchen"))
        self.filenameLbl.setText(_translate("MainWindow", "Dateiname"))
        self.startRecBtn.setText(_translate("MainWindow", "Messungen starten"))


#if __name__ == "__main__":
#    import sys
#    app = QtWidgets.QApplication(sys.argv)
#    MainWindow = QtWidgets.QMainWindow()
#    ui = Ui_MainWindow()
#    ui.setupUi(MainWindow)
#    MainWindow.show()
#    sys.exit(app.exec_())
