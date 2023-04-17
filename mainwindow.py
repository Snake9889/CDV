# This Python file uses the following encoding: utf-8

import os.path
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel
from PyQt5.QtCore import pyqtSignal, QRectF, Qt, QSettings, QSize, QPoint
from PyQt5 import uic
import pyqtgraph as pg
from helpwidget import HelpWidget


class MainWindow(QMainWindow):
    """   """
    region_changed = pyqtSignal(object)

    def __init__(self, data_source, data_proc, settings_control, bpm_name):
        super(MainWindow, self).__init__()

        ui_path = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(ui_path, 'MainWindow_1.ui'), self)

        self.bpm = bpm_name

        self.images_list = []
        self.I_rect = None

        self.data_source = data_source
        self.data_proc = data_proc
        self.settingsControl = settings_control

        self.data_proc.data_processed.connect(self.on_current_status)

        self.actionSave.triggered.connect(self.on_save_button)
        self.actionRead.triggered.connect(self.on_read_button)

        self.actionExit.triggered.connect(self.on_exit_button)
        self.actionExit.triggered.connect(QApplication.instance().quit)

        self.help_widget = HelpWidget(os.path.join(ui_path, 'etc/icons/Help_1.png'))
        self.actionHelp.triggered.connect(self.help_widget.show)

        # self.ui.nu_x_label.setText('\u03BD<sub>x</sub> = ')
        # self.ui.nu_z_label.setText('\u03BD<sub>z</sub> = ')
        # self.ui.delta_I_label.setText('\u0394I = ')

        self.plots_customization()

        self.data_curve1 = self.ui.plotI.plot(pen='r', title='Current_plot_BPM1')
        self.data_curve2 = self.ui.plotI.plot(pen='b', title='Current_plot_BPM2')
        self.data_curve3 = self.ui.plotI.plot(pen='k', title='Current_plot_BPM3')
        self.data_curve4 = self.ui.plotI.plot(pen='y', title='Current_plot_BPM4')

    @staticmethod
    def customise_label(plot, text_item, html_str):
        """   """
        plot_vb = plot.getViewBox()
        text_item.setHtml(html_str)
        text_item.setParentItem(plot_vb)

    def plots_customization(self):
        """   """
        label_str_i = "<span style=\"color:black;font-size:16px\">{}</span>"

        plot = self.ui.plotI
        self.customize_plot(plot)
        self.customise_label(plot, pg.TextItem(), label_str_i.format("I"))

    @staticmethod
    def customize_plot(plot):
        """   """
        plot.setBackground('w')
        plot.showAxis('top')
        plot.showAxis('right')
        plot.getAxis('top').setStyle(showValues=False)
        plot.getAxis('right').setStyle(showValues=False)
        plot.showGrid(x=True, y=True)

    def on_exit_button(self):
        """   """
        print(self, ' Exiting... Bye...')

    def on_read_button(self):
        """   """
        self.settingsControl.read_settings()

    def on_save_button(self):
        """   """
        self.settingsControl.save_settings()

    def on_current_ready(self, data_source):
        """   """
        self.data_curve4.setData(data_source.data_bpm[:,0], data_source.data_bpm[:, 3])
        self.current_rect = self.ui.plotI.viewRange()

    def on_current_status(self, data_processor):
        """   """
        if data_processor.warning == 0:
            self.ui.delta_I_1.setText('{:.5f}'.format(data_processor.delta_I))
            self.ui.pos_1.setText('{:.5f}'.format(data_processor.t_zero))
        elif data_processor.warning == 1:
            self.ui.delta_I_1.setText(data_processor.warningText)
            self.ui.pos_1.setText(data_processor.warningText)
        else:
            self.ui.delta_I_1.setText('Unexpected value!')
            self.ui.pos_1.setText('Unexpected value!')


    def save_settings(self):
        """   """
        settings = QSettings()
        settings.beginGroup(self.bpm)
        settings.beginGroup("Plots")
        settings.setValue("current_zoom", self.current_rect)
        settings.setValue('size', self.size())
        settings.setValue('pos', self.pos())
        settings.endGroup()
        settings.endGroup()
        settings.sync()

    def read_settings(self):
        """   """
        rect_def = [[0, 1], [0, 1]]
        rect_def_phase = [[-1, 1], [-1, 1]]
        settings = QSettings()
        settings.beginGroup(self.bpm)
        settings.beginGroup("Plots")
        self.current_rect = settings.value("current_zoom", rect_def)
        self.resize(settings.value('size', QSize(500, 500)))
        self.move(settings.value('pos', QPoint(60, 60)))
        settings.endGroup()
        settings.endGroup()

        self.ui.plotI.setRange(xRange=self.current_rect[0], yRange=self.current_rect[1])

