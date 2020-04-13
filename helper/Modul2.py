# recordWindow

    ser = ''
    def __init__(self):
    #def __init__(self, filename, filepath):
        #self.timer = QtCore.QTimer()
        #self.timer.setInterval(3000)
        #self.timer.singleShot(0, self.start_recording)
        #self.timer.timeout.connect(self.start_recording)
        #self.timer.setSingleShot(True)
        #self.timer.start()
        self.MAP = {1: 'Zähneknirschen',
                    2: 'Zähne zusammenbeißen', 
                    3: 'Kauen', 
                    4: 'Gähnen',
                    5: 'Entspannen'}
        self.samples = []
        #self.filename = filename
        #self.filepath = filepath

    def start_recording(self):
        print('started')
        writer = pd.ExcelWriter(r"{}\{}".format(self.filepath, self.filename), engine = 'xlsxwriter') 
        for task_no in range(1,6):
            self.collect_data(writer, task_no, 15)
            QtWidgets.QApplication.processEvents()
            self.emg_df = pd.DataFrame(data = self.samples)
            self.emg_df.to_excel(writer, sheet_name=self.MAP[task_no])
        writer.save()
        writer.close()
        self.analysisBtn.setEnabled(True)

    def collect_data(self, writer, task_no, dt=60):
        self.samples = []
        QtWidgets.QApplication.processEvents()
        self.taskTxt.setText(self.MAP[task_no])
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



    def rec(self, dt=4):
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

    def read_serial_input(self, dt=4):
        end = time.time() + dt
        while time.time() < end:
            if not(self.ser.isOpen()):
                break
            QtWidgets.QApplication.processEvents()
            self.samples.append(self.ser.readline().decode('utf-8', 'ignore').rstrip())
            

    def red_light(self):
        self.r_led.setBrush(self.red)
        self.y_led.setBrush(self.yellow_faded)
        self.g_led.setBrush(self.green_faded)
        QtWidgets.QApplication.processEvents()
        self.scene.update()
        
    def cancel(self, Form):
        #Form.hide()      
        Form.close()


    def make_analysis(self):
        file = open(r"{}\{}.py".format(self.filepath,self.filename.split('.')[0], ), 'w')
        file.write('import pandas as pd\n')
        file.write('import seaborn as sns\n')
        file.write('import matplotlib.pyplot as plt\n')
        file.write('masseter_df = pd.DataFrame()\n')
        file.write('MAP = {}\n'.format(self.MAP))
        file.write('for movement in list(MAP.values()):\n')
        file.write('\tdf = pd.read_excel( r"{}\{}", index_col=0, sheet_name=movement)\n'.format(self.filepath,self.filename))
        file.write('\tmasseter_df.insert(0, movement, df[0])\n')
        file.write('display(masseter_df.describe(), masseter_df.info())\n')
        file.write('fig = plt.figure(figsize=(20,8))\n')
        file.write('ax = sns.scatterplot(data=masseter_df[:4000])\n')
        file.write('ax2 = ax.twinx()\n')
        file.write("ax2.set(xlabel='sample no.', ylabel='amplitude [V]', title='EMG Signal Sequence Masseter')\n")
        file.write('sns.scatterplot(data=masseter_df[:4000]*5/1023, ax=ax2)\n')
        file.write('plt.show()')
        file.close()

        subprocess.Popen('ipynb-py-convert {}/{}.py {}/{}.ipynb'.format(self.filepath, self.filename.split('.')[0], self.filepath, self.filename.split('.')[0]))
        subprocess.Popen('runipy {}/{}.ipynb {}/{}.ipynb'.format(self.filepath, self.filename.split('.')[0], self.filepath, self.filename.split('.')[0])).communicate()
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://localhost:8888/notebooks/Desktop/{}.ipynb'.format(self.filename.split('.')[0])))


  
# mainWindow
    def record_screen(self):
        self.Form = QtWidgets.QWidget()
        self.ui = Ui_Form(self.filename, self.filepath)
        self.ui.setupUi(self.Form)
        self.ui.cancelBtn.clicked.connect(self.update_status)
        #self.startRecBtn.clicked.connect(self.ui.start_recording)
        if self.serial_connection:
            setattr(self.ui, 'ser', self.ser)
            self.Form.show()
            self.ui.start_recording()
            
    def get_file_info(self):
        return self.filename, self.filepath

    def select_loc(self):
        self.filepath = QtWidgets.QFileDialog.getExistingDirectory(None, 'Speichern unter')
        self.filepathTB.setText(self.filepath)

    def get_filename(self):
        self.filename = self.filenameLE.text()

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

    def get_current_port(self):
        #self.current_port = str(self.portDropdown.currentText())
        return str(self.portDropdown.currentText())

    def start_serial_connection(self):
        self.get_current_port()
        try:
            # pySerial timeout=None:  wait forever / until requested number of bytes are received
            self.ser = serial.Serial(self.current_port, self.baudrate, timeout=None)  
        except Exception:
           self.serstatus.setText("Serial Status: Failed to open port {}".format(self.current_port))
        else:
            self.serstatus.setText("Serial Status: Port {} opened".format(self.current_port))
            self.serial_connection  = True
   
    def help():
        pass
            
 
    def update_status(self):
        try:
            self.ser.close()
        except Exception as e:
            print(e)
            pass
        else:
            self.serstatus.setText("Serial Status: Disconnected")
            self.serial_connection  = False
       

# main
ser = None
baudrate = 115200

def start_serial_connection(mainUi):
    current_port = mainUi.get_current_port()
    try:
        # pySerial timeout=None:  wait forever / until requested number of bytes are received
        ser = serial.Serial(current_port, baudrate, timeout=None)  
    except Exception:
        mainUi.serstatus.setText("Serial Status: Failed to open port {}".format(current_port))
    else:
        mainUi.serstatus.setText("Serial Status: Port {} opened".format(current_port))
        #mainUi.serial_connection  = True

def update_status(mainUi):
    if ser.isOpen():
        ser.close()
        mainUi.serstatus.setText("Serial Status: Disconnected")
        #mainUi.serial_connection  = False

def make_analysis(mainUi):
    filename, filepath = mainUi.get_file_info()
    file = open(r"{}\{}.py".format(filepath, filename.split('.')[0], ), 'w')
    file.write('import pandas as pd\n')
    file.write('import seaborn as sns\n')
    file.write('import matplotlib.pyplot as plt\n')
    file.write('masseter_df = pd.DataFrame()\n')
    file.write('MAP = {}\n'.format(self.MAP))
    file.write('for movement in list(MAP.values()):\n')
    file.write('\tdf = pd.read_excel( r"{}\{}", index_col=0, sheet_name=movement)\n'.format(filepath, filename))
    file.write('\tmasseter_df.insert(0, movement, df[0])\n')
    file.write('display(masseter_df.describe(), masseter_df.info())\n')
    file.write('fig = plt.figure(figsize=(20,8))\n')
    file.write('ax = sns.scatterplot(data=masseter_df[:4000])\n')
    file.write('ax2 = ax.twinx()\n')
    file.write("ax2.set(xlabel='sample no.', ylabel='amplitude [V]', title='EMG Signal Sequence Masseter')\n")
    file.write('sns.scatterplot(data=masseter_df[:4000]*5/1023, ax=ax2)\n')
    file.write('plt.show()')
    file.close()

    subprocess.Popen('ipynb-py-convert {}/{}.py {}/{}.ipynb'.format(filepath, filename.split('.')[0], filepath, filename.split('.')[0]))
    subprocess.Popen('runipy {}/{}.ipynb {}/{}.ipynb'.format(filepath, filename.split('.')[0], filepath, filename.split('.')[0])).communicate()
    QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://localhost:8888/notebooks/Desktop/{}.ipynb'.format(filename.split('.')[0])))


def record_screen(mainUi):
    Form = QtWidgets.QWidget()
    #ui = Ui_Form(self.filename, self.filepath)
    ui = Ui_Form()
    ui.setupUi(Form)
    ui.cancelBtn.clicked.connect(lambda:update_status())
    start_serial_connection(mainUi)
    #self.startRecBtn.clicked.connect(self.ui.start_recording)
    if ser.isOpen():
        setattr(ui, 'ser', ser)
        ui.cancelBtn.clicked.connect(lambda: self.cancel(Form))
        ui.analysisBtn.clicked.connect(lambda:make_analysis(ui))
        Form.show()
        ui.start_recording()