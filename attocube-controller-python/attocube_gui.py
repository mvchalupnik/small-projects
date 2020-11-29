

import datetime
import numpy as np
import os
import pyqtgraph as pg
import pyqtgraph.exporters
import time

from qtpy import QtWidgets
from qtpy import QtGui
from qtpy import uic
import attocube_logic



class AttocubeWindow(QtWidgets.QWidget):
    def __init__(self):
        """ Create the attocube control window.
        """
        # Get the path to the *.ui file
        this_dir = os.path.dirname(__file__)
        ui_file = os.path.join(this_dir, 'uis/attocubeGUI_6axes_mod.ui')

        # Load it
        super().__init__()
        uic.loadUi(ui_file, self)
        self.show()


class AttocubeGUI():
    _modclass = 'AttocubeGui'
    _modtype = 'gui'

    ## declare connectors
    attocubelogic1= attocube_logic.AttocubeLogic


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_activate()

    def on_activate(self):
        """ Definition and initialisation of the GUI.
        """

        #=============
        #Connect buttons
        #=============


        self._attocube_logic = self.attocubelogic1()

        # setting up the window
        self._mw = AttocubeWindow()

        # initialize arrays
      
        self.comboBox_setMode_arr = [self._mw.comboBox_setMode, self._mw.comboBox_setMode_3, self._mw.comboBox_setMode_4,
                                self._mw.comboBox_setMode_5, self._mw.comboBox_setMode_6, self._mw.comboBox_setMode_7]

        self.pushButton_submitFreq_arr= [self._mw.pushButton_submitFreq, self._mw.pushButton_submitFreq_3, self._mw.pushButton_submitFreq_4,
                                self._mw.pushButton_submitFreq_5, self._mw.pushButton_submitFreq_6, self._mw.pushButton_submitFreq_7]
        self.pushButton_left_arr = [self._mw.pushButton_left, self._mw.pushButton_left_3, self._mw.pushButton_left_4,
                                self._mw.pushButton_left_5, self._mw.pushButton_left_6, self._mw.pushButton_left_7]
        self.pushButton_right_arr = [self._mw.pushButton_right, self._mw.pushButton_right_3, self._mw.pushButton_right_4,
                                self._mw.pushButton_right_5, self._mw.pushButton_right_6, self._mw.pushButton_right_7]
        self.lineEdit_freq_arr = [self._mw.lineEdit_currentFreq_1, self._mw.lineEdit_currentFreq_2, self._mw.lineEdit_currentFreq_3,
                                self._mw.lineEdit_currentFreq_4, self._mw.lineEdit_currentFreq_5, self._mw.lineEdit_currentFreq_6]
        self.lineEdit_volt_arr = [self._mw.lineEdit_setVolt_1, self._mw.lineEdit_setVolt_2, self._mw.lineEdit_setVolt_3,
                                self._mw.lineEdit_setVolt_4, self._mw.lineEdit_setVolt_5, self._mw.lineEdit_setVolt_6]
        self.label_freq_arr = [self._mw.label_currentFreq_1, self._mw.label_currentFreq_2, self._mw.label_currentFreq_3,
                               self._mw.label_currentFreq_4, self._mw.label_currentFreq_5, self._mw.label_currentFreq_6]
        self.label_volt_arr = [self._mw.label_currentVolt_1, self._mw.label_currentVolt_2, self._mw.label_currentVolt_3,
                               self._mw.label_currentVolt_4, self._mw.label_currentVolt_5, self._mw.label_currentVolt_6]

        self.radioButton_continuous_arr = [self._mw.radioButton_continous, self._mw.radioButton_continous_3, self._mw.radioButton_continous_4,
                                self._mw.radioButton_continous_5, self._mw.radioButton_continous_6, self._mw.radioButton_continous_7]
        self.radioButton_step_arr = [self._mw.radioButton_step, self._mw.radioButton_step_3, self._mw.radioButton_step_4,
                                self._mw.radioButton_step_5, self._mw.radioButton_step_6, self._mw.radioButton_step_7]

        self.dsOffsetV_arr = [self._mw.doubleSpinBox_offsetV_1, self._mw.doubleSpinBox_offsetV_2, self._mw.doubleSpinBox_offsetV_3,
                              self._mw.doubleSpinBox_offsetV_4, self._mw.doubleSpinBox_offsetV_5, self._mw.doubleSpinBox_offsetV_6,]



        for x in range(6):
            self.pushButton_submitFreq_arr[x].clicked.connect(lambda state, i=x: self.gui_update_stp_params(i))
            self.radioButton_continuous_arr[x].toggled.connect(lambda state, i=x: self.setContSignals(i))
            self.radioButton_step_arr[x].toggled.connect(lambda state, i=x: self.setStepSignals(i))
            self.comboBox_setMode_arr[x].currentIndexChanged.connect(lambda state, i=x: self.set_mode(i))
            self.dsOffsetV_arr[x].valueChanged.connect(lambda state, i=x: self.gui_set_offset_voltage(i))

            # Disable this comboBox for now since we have to be in stp mode anyway for uis moving
            self.comboBox_setMode_arr[x].addItem("stp+")
            self.comboBox_setMode_arr[x].addItem("stpgit")
            self.comboBox_setMode_arr[x].addItem("gnd")
            # self.comboBox_setMode_arr[x].addItem("cap")
            self.comboBox_setMode_arr[x].addItem("off")

            self.radioButton_step_arr[x].toggle()

            self.gui_get_freq(x)
            self.gui_get_volt(x)



        self._mw.pushButton_stop.clicked.connect(self.gui_stop)
        self._mw.show()

    def on_deactivate(self):
        pass

    def set_mode(self, i):
        md = self.comboBox_setMode_arr[i].currentText()
        self._attocube_logic.set_mode(1+i, md)

    def gui_set_offset_voltage(self,i):
        mode = self.comboBox_setMode_arr[i].currentText()
        if mode == 'off' or mode == 'stp+' or mode == 'stp-':
            ov = self.dsOffsetV_arr[i].value()
            self._attocube_logic.set_offset(i+1, ov) #axis number specific
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Please switch to \'off\' mode first')
            msg.exec_()

    def gui_set_freq(self,i):
        fq = self.lineEdit_freq_arr[i].text()
        self._attocube_logic.set_freq(1+i, fq)
        self.gui_get_freq(i)

    def gui_get_freq(self,i):
        response = self._attocube_logic.get_freq(i+1)
        #print(response)
        res = response.split('= ')
        self.label_freq_arr[i].setText(res[1])

    def gui_set_volt(self,i):
        v = self.lineEdit_volt_arr[i].text()
        self._attocube_logic.set_volt(1+i, v)
        self.gui_get_volt(i)

    def gui_get_volt(self,i):
        response = self._attocube_logic.get_volt(i+1)
        res = response.split('= ')
        self.label_volt_arr[i].setText(res[1])

    def gui_update_stp_params(self, i):
        try:
            val = float(self.lineEdit_freq_arr[i].text())
            self.gui_set_freq(i)
        except ValueError:
            print('  ')

        try:
            val = float(self.lineEdit_volt_arr[i].text())
            self.gui_set_volt(i)
        except ValueError:
            print('   ')


    def gui_movePiezoUp(self, i):
        mode = self.comboBox_setMode_arr[i].currentText()
        if mode == 'stp' or mode == 'stp+' or mode == 'stp-':
            self._attocube_logic.stepu(mode, i+1) #axis number specific
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Please switch to \'stp\' mode first')
            msg.exec_()

    def gui_movePiezoUpContinuous(self, i):
        mode = self.comboBox_setMode_arr[i].currentText()
        if mode == 'stp' or mode == 'stp+' or mode == 'stp-':
            self._attocube_logic.stepu(mode, i+1, 'c')
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Please switch to \'stp\' mode first')
            msg.exec_()

    def gui_movePiezoDown(self,i):
        mode = self.comboBox_setMode_arr[i].currentText()
        if mode == 'stp' or mode == 'stp+' or mode == 'stp-':
            self._attocube_logic.stepd(mode, i+1) #axis number specific
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Please switch to \'stp\' mode first')
            msg.exec_()


    def gui_movePiezoDownContinuous(self,i):
        mode = self.comboBox_setMode_arr[i].currentText()
        if mode == 'stp' or mode == 'stp+' or mode == 'stp-':
            self._attocube_logic.stepd(mode, i+1, 'c') #axis number specific
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Please switch to \'stp\' mode first')
            msg.exec_()

    def gui_stop(self):
        self._attocube_logic.stop()

    def setStepSignals(self,i):
        self.pushButton_left_arr[i].disconnect()
        self.pushButton_right_arr[i].disconnect()

        self.pushButton_left_arr[i].clicked.connect(lambda state, n=i: self.gui_movePiezoDown(n))
        self.pushButton_right_arr[i].clicked.connect(lambda state, n=i: self.gui_movePiezoUp(n))

  
    def setContSignals(self,i):
        self.pushButton_left_arr[i].disconnect()
        self.pushButton_right_arr[i].disconnect()


        self.pushButton_left_arr[i].pressed.connect(lambda: self.gui_movePiezoDownContinuous(i))
        self.pushButton_left_arr[i].released.connect(self.gui_stop)

        self.pushButton_right_arr[i].pressed.connect(lambda: self.gui_movePiezoUpContinuous(i))
        self.pushButton_right_arr[i].released.connect(self.gui_stop)



if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = AttocubeGUI()
    app.exec_()