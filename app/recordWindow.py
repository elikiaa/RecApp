# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\recordingRecApp.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sys, serial, time, os, subprocess
import pandas as pd
import numpy as np
import seaborn as sns

from general import constants


class Ui_Form(object):
    def __init__(self):
        self.samples = []
        #self.ser = None

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(866, 575)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.horLayout = QtWidgets.QHBoxLayout()
        self.horLayout.setObjectName("horLayout")

        #self.vertLayout = QtWidgets.QVBoxLayout()
        #self.vertLayout.setObjectName("vertLayout")
        #self.taskLbl = QtWidgets.QLabel(Form)
        #self.taskLbl.setFixedWidth(160)
        #self.taskLbl.setFixedHeight(30)
        #font = QtGui.QFont()
        #font.setFamily("Verdana Pro")
        #font.setPointSize(16)
        #self.taskLbl.setFont(font)
        #self.taskLbl.setObjectName("taskLbl")
        #self.vertLayout.addWidget(self.taskLbl, 0, QtCore.Qt.AlignHCenter)
        self.taskTxt = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Verdana Pro")
        font.setPointSize(22)
        self.taskTxt.setFont(font)
        self.taskTxt.setObjectName("taskTxt")
        self.taskTxt.setFixedHeight(30)
        self.taskTxt.setFixedWidth(400)
        #self.vertLayout.addWidget(self.taskTxt, 0, QtCore.Qt.AlignHCenter)
        
        #self.gridLayout.addLayout(self.vertLayout, 0, 0, 1, 1)

    # Ampel
        
        self.scene = QtWidgets.QGraphicsScene()
        #self.showStatus(self.scene, self)
        self.red = QtCore.Qt.red
        self.red_faded = QtGui.QColor(255, 0, 0, 50)
        self.yellow = QtCore.Qt.yellow
        self.yellow_faded = QtGui.QColor(255, 255, 0, 50)
        self.green = QtCore.Qt.green
        self.green_faded = QtGui.QColor(0, 255, 0, 50)

        self.r_led = self.scene.addEllipse(0,0,90,90, QtGui.QPen(self.red_faded), QtGui.QBrush(self.red))
        self.y_led = self.scene.addEllipse(0,120,90,90, QtGui.QPen(self.yellow_faded), QtGui.QBrush(self.yellow_faded))
        self.g_led = self.scene.addEllipse(0,240,90,90, QtGui.QPen(self.green_faded), QtGui.QBrush(self.green_faded))

        self.showStatus = QtWidgets.QGraphicsView(self.scene)
        self.showStatus.setBackgroundBrush(QtGui.QColor(0, 0, 0,200))
        self.showStatus.setFixedWidth(160)
        self.showStatus.setFixedHeight(400)
        self.showStatus.setObjectName("showStatus")
        self.horLayout.addStretch()
        self.horLayout.addWidget(self.showStatus,1)
        self.horLayout.addStretch()
        self.horLayout.addWidget(self.taskTxt, 3)
        self.horLayout.addStretch()
        self.gridLayout.addLayout(self.horLayout, 0, 0, 1, 1, QtCore.Qt.AlignCenter)

    # Buttons
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.addStretch()
        self.analysisBtn = QtWidgets.QPushButton(Form)
        self.analysisBtn.setEnabled(False)
        self.analysisBtn.setFixedWidth(150)
        self.analysisBtn.setFixedHeight(50)
        font = QtGui.QFont()
        font.setFamily("Verdana Pro")
        font.setPointSize(10)
        self.analysisBtn.setFont(font)
        self.analysisBtn.setObjectName("analysisBtn")
        self.horizontalLayout_2.addWidget(self.analysisBtn)
        self.cancelBtn = QtWidgets.QPushButton(Form)
        self.cancelBtn.setMinimumSize(QtCore.QSize(150, 50))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro")
        font.setPointSize(10)
        self.cancelBtn.setFont(font)
        self.cancelBtn.setObjectName("cancelBtn")
        self.horizontalLayout_2.addWidget(self.cancelBtn)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
    def record_screen(self, Form):
        Form.show()

    def cancel(self, Form):
        #Form.hide()      
        Form.close()
    
    def _start_recording(self, ui, ser):
        print('started')
        print((ui))
        filename = ui.get_filename()
        filepath = ui.get_filepath()
        print('filename: {}, filepath: {}'.format(filename, filepath))
        self.ser = ser
        writer = pd.ExcelWriter(r"{}\{}".format(filepath, filename), engine = 'xlsxwriter') 
        for task_no in range(1,6):
            self.taskTxt.setText(constants.MAP[task_no])
            self.collect_data(writer, task_no, 5)
            QtWidgets.QApplication.processEvents()
            emg_df = pd.DataFrame(data = self.samples)
            emg_df.to_excel(writer, sheet_name=constants.MAP[task_no])
        writer.save()
        writer.close()
        self.analysisBtn.setEnabled(True)    

    def _collect_data(self, writer, task_no, dt=60):
        self.samples = []
        QtWidgets.QApplication.processEvents()
        #self.taskTxt.setText(cons.MAP[task_no])
        end = time.time() + dt
        if task_no < 5:
            while time.time() < end:
                self.rec(4)
        if task_no == 5:
            self.yellow_light()
            time.sleep(1)
            self.green_light()
            self.read_serial_input(dt)
            self.red_light()
        
        #self.samples = np.array(self.samples).reshape(len(self.samples), 1)

    def _rec(self, dt=4):
        time.sleep(2)
        self.yellow_light()
        time.sleep(2)
        self.green_light()
        self.read_serial_input(dt)
        self.red_light()
        time.sleep(1)

    def green_light(self):
        self.r_led.setBrush(self.red_faded)
        self.y_led.setBrush(self.yellow_faded)
        self.g_led.setBrush(self.green)
        QtWidgets.QApplication.processEvents()
        self.scene.update()

    def yellow_light(self):
        self.r_led.setBrush(self.red_faded)
        self.y_led.setBrush(self.yellow)
        self.g_led.setBrush(self.green_faded) 
        QtWidgets.QApplication.processEvents()
        self.scene.update()

    def red_light(self):
        self.r_led.setBrush(self.red)
        self.y_led.setBrush(self.yellow_faded)
        self.g_led.setBrush(self.green_faded)
        QtWidgets.QApplication.processEvents()
        self.scene.update()

    def _read_serial_input(self, dt=4):
        end = time.time() + dt
        while time.time() < end:
            if self.ser is None:
                break
            QtWidgets.QApplication.processEvents()
            self.samples.append(self.ser.readline().decode('utf-8', 'ignore').rstrip())

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Collect Data"))
        #self.taskLbl.setText(_translate("Form", "Bewegung:"))
        self.taskTxt.setText(_translate("Form", ""))
        self.analysisBtn.setText(_translate("Form", "Analyse"))
        self.cancelBtn.setText(_translate("Form", "Abbrechen"))


