import time
import pandas as pd

from general import constants


class Recording(object):
    def __init__(self, ser = None):
        self.ser = ser
        self.samples = []

    def start_recording(self, rec_ui, filename='', filepath=''):
        # filename = ui.get_filename()
        # filepath = ui.get_filepath()
        # print('filename: {}, filepath: {}'.format(filename, filepath))
        writer = pd.ExcelWriter(r"{}\{}".format(filepath, filename), engine='xlsxwriter')
        for task_no in range(1, len(constants.MAP)):
            rec_ui.taskTxt.setText(constants.MAP[task_no])
            samples = self.get_samples(writer, rec_ui, task_no, 18)
            print(samples)
            # QtWidgets.QApplication.processEvents()
            emg_df = pd.DataFrame(data=samples)
            emg_df.to_excel(writer, sheet_name=constants.MAP[task_no])
            self.samples = []
        writer.save()
        writer.close()
        rec_ui.analysisBtn.setEnabled(True)

    def get_samples(self, writer, rec_ui, task_no, dt=60):
        # QtWidgets.QApplication.processEvents()
        rec_ui.taskTxt.setText(constants.MAP[task_no])
        end = time.time() + dt
        if task_no < 5:
            while time.time() < end:
                self.rec(rec_ui, 4)
        if task_no == 5:
            rec_ui.yellow_light()
            time.sleep(1)
            rec_ui.green_light()
            self.read_serial_input(dt)
            rec_ui.red_light()

        # self.samples = np.array(self.samples).reshape(len(self.samples), 1)
        return self.samples

    def rec(self, rec_ui, dt=4):
        time.sleep(2)
        rec_ui.yellow_light()
        time.sleep(2)
        rec_ui.green_light()
        self.read_serial_input(dt)
        rec_ui.red_light()
        time.sleep(1)

    def read_serial_input(self, dt=4):
        end = time.time() + dt
        while time.time() < end:
            if self.ser is None:
                print(None)
                break
            # QtWidgets.QApplication.processEvents()
            self.samples.append(self.ser.readline().decode('utf-8', 'ignore').rstrip())
