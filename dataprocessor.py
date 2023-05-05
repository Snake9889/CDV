# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, Qt, QObject, QTimer
import numpy as np
import math
from command_parser import TerminalParser


class DataProcessor(QObject):
    """   """
    data_processed = pyqtSignal(object)

    def __init__(self, data_len=1024, parent=None):
        super(DataProcessor, self).__init__(parent)

        self.data_len = data_len

        self.dataT = None
        self.dataX = None
        self.dataZ = None
        self.dataI = None
        self.current_to_process = None

        self.t_zero = 0
        self.delta_I = 0.0
        self.max_I = 0.0
        self.pos_X = 0
        self.pos_Z = 0
        self.istart = None
        self.bpm_name = None

        self.warning = 0
        self.warning_text = ""

    def on_data_recv(self, data_source):
        """   """
        self.data_len = data_source.data_len
        self.istart = data_source.istart
        self.bpm_name = data_source.bpm_name_local

        self.dataT = data_source.data_bpm[:, 0]
        self.dataX = data_source.data_bpm[:, 1]
        self.dataZ = data_source.data_bpm[:, 2]
        self.dataI = data_source.data_bpm[:, 3]
        self.current_to_process = self.dataI

        self.delta_I, self.t_zero, self.max_I = self.current_calc(self.current_to_process)
        self.pos_X, self.pos_Z = self.osc_data_obt()

        self.data_processed.emit(self)

    def current_calc(self, current):
        """   """
        max_pos = 0
        max_diff = 0
        diff = np.zeros(len(current))
        for i in range(len(current)-1):
            diff[i] = current[i+1] - current[i]
        max_pos = np.argmax(abs(diff)) + 1
        print(max_pos)
        cur_max = current[max_pos]
        max_diff = current[max_pos] - np.mean(current[0:(max_pos-2)])
        return(max_diff, max_pos, cur_max)

    def osc_data_obt(self):
        """   """
        pos_X = self.dataX[self.t_zero]
        pos_Z = self.dataZ[self.t_zero]
        return(pos_X, pos_Z)



