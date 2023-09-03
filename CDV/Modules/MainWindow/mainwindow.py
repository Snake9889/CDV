# This Python file uses the following encoding: utf-8

import os.path
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel
from PyQt5.QtCore import pyqtSignal, QRectF, Qt, QSettings, QSize, QPoint
from PyQt5 import uic
import pyqtgraph as pg
from CDV.Modules.MainWindow.helpwidget import HelpWidget


class MainWindow(QMainWindow):
    """   """
    region_changed = pyqtSignal(object)

    def __init__(self, data_source, data_proc, settings_control, bpm_name, parent=None):
        super().__init__(parent)

        ui_path = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(ui_path, 'MainWindow.ui'), self)

        self.bpm = bpm_name

        self.images_list = []
        self.I_rect = None

        self.bpm01_dict = {'plot': self.ui.plotI, 'pos': self.ui.pos_1, 'status': self.ui.status_1,
                        'I_label': self.ui.i_label_1, 'I_value': self.ui.value_I_1,
                        'X_label': self.ui.x_label_1, 'X_value': self.ui.value_x_1,
                        'Z_label': self.ui.z_label_1, 'Z_value': self.ui.value_z_1,
                        'delta_label': self.ui.delta_label_1, 'delta_value': self.ui.delta_1}
        self.bpm02_dict = {'plot': self.ui.plotI, 'pos': self.ui.pos_2, 'status': self.ui.status_2,
                        'I_label': self.ui.i_label_2, 'I_value': self.ui.value_I_2,
                        'X_label': self.ui.x_label_2, 'X_value': self.ui.value_x_2,
                        'Z_label': self.ui.z_label_2, 'Z_value': self.ui.value_z_2,
                        'delta_label': self.ui.delta_label_2, 'delta_value': self.ui.delta_2}
        self.bpm03_dict = {'plot': self.ui.plotI, 'pos': self.ui.pos_3, 'status': self.ui.status_3,
                        'I_label': self.ui.i_label_3, 'I_value': self.ui.value_I_3,
                        'X_label': self.ui.x_label_3, 'X_value': self.ui.value_x_3,
                        'Z_label': self.ui.z_label_3, 'Z_value': self.ui.value_z_3,
                        'delta_label': self.ui.delta_label_3, 'delta_value': self.ui.delta_3}
        self.bpm04_dict = {'plot': self.ui.plotI, 'pos': self.ui.pos_4, 'status': self.ui.status_4,
                        'I_label': self.ui.i_label_4, 'I_value': self.ui.value_I_4,
                        'X_label': self.ui.x_label_4, 'X_value': self.ui.value_x_4,
                        'Z_label': self.ui.z_label_4, 'Z_value': self.ui.value_z_4,
                        'delta_label': self.ui.delta_label_4, 'delta_value': self.ui.delta_4}

        self.data_source = data_source
        self.data_proc = data_proc
        self.settingsControl = settings_control

        self.data_proc.data_processed.connect(self.on_widgets_choice)

        self.actionSave.triggered.connect(self.on_save_button)
        self.actionRead.triggered.connect(self.on_read_button)

        self.actionExit.triggered.connect(self.on_exit_button)
        self.actionExit.triggered.connect(QApplication.instance().quit)

        self.help_widget = HelpWidget(os.path.join(ui_path, 'etc/icons/Help_1.png'))
        self.actionHelp.triggered.connect(self.help_widget.show)

        self.plots_customization()

        self.data_curve1 = self.ui.plotI.plot(pen='r', title='Current_plot_BPM1')
        self.data_curve2 = self.ui.plotI.plot(pen='b', title='Current_plot_BPM2')
        self.data_curve3 = self.ui.plotI.plot(pen='k', title='Current_plot_BPM3')
        self.data_curve4 = self.ui.plotI.plot(pen='g', title='Current_plot_BPM4')

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

    def on_current_choice(self, data_source):
        """   """
        if data_source.bpm_name_local in ('model_1', 'bpm01'):
            self.on_current_ready(data_source.data_bpm, self.data_curve1)
        elif data_source.bpm_name_local in ('model_2', 'bpm02'):
            self.on_current_ready(data_source.data_bpm, self.data_curve2)
        elif data_source.bpm_name_local in ('model_3', 'bpm03'):
            self.on_current_ready(data_source.data_bpm, self.data_curve3)
        elif data_source.bpm_name_local in ('model_4', 'bpm04'):
            self.on_current_ready(data_source.data_bpm, self.data_curve4)
        else: pass

    def on_current_ready(self, data, curve):
        """   """
        curve.setData(data[:,0], data[:, 3])
        self.current_rect = self.ui.plotI.viewRange()

    def on_widgets_choice(self, data_processor):
        """   """
        if data_processor.bpm_name in ('model_1', 'bpm01'):
            self.on_current_status(data_processor.t_zero, data_processor.warning, data_processor.warning_text,
            data_processor.pos_X, data_processor.pos_Z, data_processor.delta_I, data_processor.max_I, self.bpm01_dict, data_processor.istart)
        elif data_processor.bpm_name in ('model_2', 'bpm02'):
            self.on_current_status(data_processor.t_zero, data_processor.warning, data_processor.warning_text,
            data_processor.pos_X, data_processor.pos_Z, data_processor.delta_I, data_processor.max_I, self.bpm02_dict, data_processor.istart)
        elif data_processor.bpm_name in ('model_3', 'bpm03'):
            self.on_current_status(data_processor.t_zero, data_processor.warning, data_processor.warning_text,
            data_processor.pos_X, data_processor.pos_Z, data_processor.delta_I, data_processor.max_I, self.bpm03_dict, data_processor.istart)
        elif data_processor.bpm_name in ('model_4', 'bpm04'):
            self.on_current_status(data_processor.t_zero, data_processor.warning, data_processor.warning_text,
            data_processor.pos_X, data_processor.pos_Z, data_processor.delta_I, data_processor.max_I, self.bpm04_dict, data_processor.istart)
        else: pass

    def on_current_status(self, pos, warning, text, x_amp, z_amp, delta, i_amp, w_dict, status):
        """   """
        if warning == 0:
            if status == 1:
                w_dict['status'].setStyleSheet("QLabel{background-color: red; border: 1px solid black; border-radius: 10px;}")
                w_dict['status'].setToolTip("Run regime")
            else:
                w_dict['status'].setStyleSheet("QLabel{background-color: green; border: 1px solid black; border-radius: 10px;}")
                w_dict['status'].setToolTip("Everything OK")
            w_dict['pos'].setText(f'{pos}')
            w_dict['I_label'].setText(f'I<sub>{pos:04}</sub> = ')
            w_dict['I_value'].setText(f'{i_amp:.3f}')
            w_dict['X_label'].setText(f'X<sub>{pos:04}</sub> = ')
            w_dict['X_value'].setText(f'{x_amp:.3f}')
            w_dict['Z_label'].setText(f'Z<sub>{pos:04}</sub> = ')
            w_dict['Z_value'].setText(f'{z_amp:.3f}')
            w_dict['delta_label'].setText(f'\u0394 I = ')
            w_dict['delta_label'].setToolTip(f'I<sub>{pos:04}</sub> - <span style="text-decoration:overline">I</span><sub>{(pos-2):04}</sub> = ')
            w_dict['delta_value'].setText(f'{delta:.3f}')
        elif warning == 1:
            w_dict['pos'].setText(text)
            w_dict['status'].setStyleSheet("QLabel{background-color: red; border: 1px solid black; border-radius: 10px;}")
        else:
            w_dict['pos'].setText('Unexpected value!')
            w_dict['status'].setStyleSheet("QLabel{background-color: red; border: 1px solid black; border-radius: 10px;}")


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

