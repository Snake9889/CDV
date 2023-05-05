#
#
from PyQt5.QtCore import pyqtSignal, QObject, QTimer, QSettings
import numpy as np
import pycx4.qcda as cda
import os
from playsound import playsound
from BPM_template import BPMTemplate
from datasources_bpm import BPMData
import datasources

class BPMDataAll(BPMTemplate):
    """   """

    """Default time for timer in ms"""
    DEFAULT_TIME = 5*1000
    """Control for hash"""
    control = (1, 1, 1, 1)
    """BPM name"""
    bpm = "bpm_all"
    """istart type"""
    istart_work = (0, 0, 0, 0)

    def __init__(self, bpm_name='', parent=None):
        super(BPMDataAll, self).__init__("bpm_all", parent)

        self.data_bpm = None
        self.istart = None
        self.bpm_name_local = None

        self.timer_1 = QTimer()
        self.timer_2 = QTimer()
        self.timer_3 = QTimer()
        self.timer_4 = QTimer()

        self.sound_path = os.path.dirname(os.path.abspath(__file__))
        self.music_win = {"bpm01": 'etc\sound\BPM01_stopped.mp3',
                          "bpm02": 'etc\sound\BPM02_stopped.mp3',
                          "bpm03": 'etc\sound\BPM03_stopped.mp3',
                          "bpm04": 'etc\sound\BPM04_stopped.mp3',
                          "model_1": 'etc\sound\Model_stopped.mp3',
                          "model_2": 'etc\sound\Model_stopped.mp3',
                          "model_3": 'etc\sound\Model_stopped.mp3',
                          "model_4": 'etc\sound\Model_stopped.mp3'}
        self.music_lin = {"bpm01": 'etc/sound/BPM01_stopped.mp3',
                          "bpm02": 'etc/sound/BPM02_stopped.mp3',
                          "bpm03": 'etc/sound/BPM03_stopped.mp3',
                          "bpm04": 'etc/sound/BPM04_stopped.mp3',
                          "model_1": 'etc/sound/Model_stopped.mp3',
                          "model_2": 'etc/sound/Model_stopped.mp3',
                          "model_3": 'etc/sound/Model_stopped.mp3',
                          "model_4": 'etc/sound/Model_stopped.mp3'}
        self.timers = {"bpm01": self.timer_1,
                       "model_1": self.timer_1,
                       "bpm02": self.timer_2,
                       "model_2": self.timer_2,
                       "bpm03": self.timer_3,
                       "model_3": self.timer_3,
                       "bpm04": self.timer_4,
                       "model_4": self.timer_4}

        self.def_time = 5000#10000
        self.timer_1.timeout.connect(self.on_sound_played)
        self.timer_2.timeout.connect(self.on_sound_played)
        self.timer_3.timeout.connect(self.on_sound_played)
        self.timer_4.timeout.connect(self.on_sound_played)

        if bpm_name == 'bpm_all':
            self.BPM1 = BPMData("bpm01")
            self.BPM2 = BPMData("bpm02")
            self.BPM3 = BPMData("bpm03")
            self.BPM4 = BPMData("bpm04")
        elif bpm_name == 'model_all':
            self.BPM1 = datasources.BPMData("model_1")
            self.BPM2 = datasources.BPMData("model_2")
            self.BPM3 = datasources.BPMData("model_3")
            self.BPM4 = datasources.BPMData("model_4")
        else:
            self.BPM1 = datasources.BPMData("model_1")
            self.BPM2 = datasources.BPMData("model_2")
            self.BPM3 = datasources.BPMData("model_3")
            self.BPM4 = datasources.BPMData("model_4")

        self.BPM1.data_ready.connect(self.on_data_ready)
        self.BPM2.data_ready.connect(self.on_data_ready)
        self.BPM3.data_ready.connect(self.on_data_ready)
        self.BPM4.data_ready.connect(self.on_data_ready)

    def on_data_ready(self, BPM):
        """   """
        print(BPM.bpm_name)
        self.bpm_name_local = BPM.bpm_name
        self.istart = BPM.istart
        self.timers[self.bpm_name_local].start(self.def_time)
        if self.istart == 0:
            self.timers[self.bpm_name_local].stop()
        self.reshaping_data(BPM)

    def reshaping_data(self, BPM):
        """   """
        # self.bpm_name_local = BPM.bpm_name
        data_len = len(BPM.dataT)
        data_bpm = self.reshaping_arrays(BPM.dataT, BPM.dataX, BPM.dataZ, BPM.dataI)
        self.data_bpm = data_bpm
        self.data_ready.emit(self)

    def reshaping_arrays(self, M1, M2, M3, M4):
        """   """
        newMass = np.zeros((len(M1),4))
        for i in range(len(M1)):
            newMass[:, 0] = M1
            newMass[:, 1] = M2
            newMass[:, 2] = M3
            newMass[:, 3] = M4

        return(newMass)

    def on_sound_played(self):
        """   """
        sound_path = None
        sound_path = os.path.join(self.sound_path, self.music_lin[self.bpm_name_local])
        print(sound_path)
        playsound(sound_path)
