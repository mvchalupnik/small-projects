from qtpy import QtCore
from collections import OrderedDict
import numpy as np
import time
import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import pyvisa
import attocube_hardware

class AttocubeLogic():

    """This logic module gathers data from wavemeter and the counter logic.
    """

  
    _modclass = 'attocubelogic'
    _modtype = 'logic'

    # declare connectors
    attocube1 = attocube_hardware.ANC300


    def __init__(self, **kwargs):
        """ Create WavemeterLoggerLogic object with connectors.

          @param dict config: module configuration
          @param dict kwargs: optional parameters
        """
        super().__init__(**kwargs)
        self.on_activate()

    def on_activate(self):
        self._attocube = self.attocube1()

    def on_deactivate(self):
        pass

    def stepu(self, mode, axisnum, stepsize=1):
        self._attocube.write('setm ' + str(axisnum) + ' ' + mode) #step only works in 'stp' mode!
        self._attocube.write('stepu ' + str(axisnum) + ' ' + str(stepsize)) #stepsize = 'c' for continous mode

    def stepd(self, mode, axisnum, stepsize=1):
        self._attocube.write('setm ' + str(axisnum) + ' ' + mode)
        self._attocube.write('stepd ' + str(axisnum) + ' ' + str(stepsize))

    def stop(self):
        #stop along ALL axes
        self._attocube.write('stop 1')
        self._attocube.write('stop 2')
        self._attocube.write('stop 3')
        self._attocube.write('stop 4')
        self._attocube.write('stop 5')
        self._attocube.write('stop 6')
        self._attocube.write('stop 7')

    def set_freq(self, axisnum, fn):
        self._attocube.write('setf ' + str(axisnum) + ' ' + str(fn))
        self._attocube.read() #clear buffer

    def get_freq(self, axisnum):
        return self._attocube.getf(axisnum)

    def set_volt(self, axisnum, vn):
        self._attocube.write('setv ' + str(axisnum) + ' ' + str(vn))
        self._attocube.read() #clear buffer

    def get_volt(self, axisnum):
        return self._attocube.getv(axisnum)

    def set_mode(self, axisnum, mode):
        self._attocube.setm(axisnum, mode)

    def set_offset(self, axisnum, ov):
        self._attocube.seta(axisnum, str(ov))