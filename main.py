from PyQt5 import QtCore, QtGui, QtWidgets
from app.recordWindow import Ui_Form
from app.mainWindow import Ui_MainWindow
import sys, subprocess
from general import constants, serialConnection as sC, recording as rec


def make_analysis(ui):
    filename = ui.get_filename().split('.')[0]
    filepath = ui.get_filepath()
    file = open(r"{}\{}.py".format(filepath, filename), 'w')
    file.write('import pandas as pd\n')
    file.write('import seaborn as sns\n')
    file.write('import matplotlib.pyplot as plt\n')
    file.write('masseter_df = pd.DataFrame()\n')
    file.write('MAP = {}\n'.format(constants.MAP))
    file.write('for movement in list(MAP.values()):\n')
    file.write('\tdf = pd.read_excel( r"{}\{}.xlsx", index_col=0, sheet_name=movement)\n'.format(filepath, filename))
    file.write('\tmasseter_df.insert(0, movement, df[0])\n')
    file.write('display(masseter_df.describe(), masseter_df.info())\n')
    file.write('fig = plt.figure(figsize=(20,8))\n')
    file.write('ax = sns.scatterplot(data=masseter_df[:4000])\n')
    file.write('ax2 = ax.twinx()\n')
    file.write("ax2.set(xlabel='sample no.', ylabel='amplitude [V]', title='EMG Signal Sequence Masseter')\n")
    file.write('sns.scatterplot(data=masseter_df[:4000]*5/1023, ax=ax2)\n')
    file.write('plt.show()')
    file.close()

    subprocess.Popen('ipynb-py-convert {}/{}.py {}/{}.ipynb'.format(filepath, filename, filepath, filename))
    subprocess.Popen('runipy {}/{}.ipynb {}/{}.ipynb'.format(filepath, filename, filepath, filename)).communicate()
    QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://localhost:8888/notebooks/Desktop/{}.ipynb'.format(filename)))


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)

    # connect Widgets
    ui.fileBtn.clicked.connect(ui.select_loc)
    ui.filenameLE.textEdited.connect(ui.set_filename)
    ui.portDropdown.popupAboutToBeShown.connect(ui.get_ports)
    ui.portDropdown.activated.connect(ui.set_current_port)

    # Serial Connection 
    # port = ui.get_current_port
    # print(port)
    # serial = sC.SerialConnection(port=port)
    # ser = serial.get_serial()

    # Recording
    #recorder = rec.Recording(ser)
    #filename = ui.get_filename()
    #filepath = ui.get_filepath()

    # 2nd screen
    Form = QtWidgets.QWidget()
    rec_ui = Ui_Form()
    rec_ui.setupUi(Form)
    rec_ui.cancelBtn.clicked.connect(lambda: rec_ui.cancel(Form))
    # rec_ui.analysisBtn.clicked.connect(lambda:make_analysis(filename = ui.get_filename().split('.')[0], filepath = ui.get_filepath()))
    rec_ui.analysisBtn.clicked.connect(lambda: make_analysis())
    # ui.startRecBtn.clicked.connect(lambda: serial.connect(port=port))
    ui.startRecBtn.clicked.connect(lambda: rec_ui.record_screen(Form))
    #ui.startRecBtn.clicked.connect(lambda: recorder.start_recording(rec_ui, filename=filename, filepath=filepath))

    # self.startrecbtn.clicked.connect(self.ui.start_recording)
    # ui.startRecBtn.clicked.connect(lambda:start_serial_connection(ui))
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
