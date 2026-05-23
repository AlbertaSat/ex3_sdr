#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: [EX3-CM] S Band Receiver
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from datetime import datetime
from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from os import name
from pathlib import Path
import sip
import threading
import time



class OQPSK_Quarter_HSTXC(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "[EX3-CM] S Band Receiver", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("[EX3-CM] S Band Receiver")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "OQPSK_Quarter_HSTXC")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.record_toggle = record_toggle = 0
        self.qt_raw_rec_toggle = qt_raw_rec_toggle = True
        self.qt_dec_rec_toggle = qt_dec_rec_toggle = True
        self.platform = platform = name
        self.timestamp = timestamp = str(datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H.%M.%S"))
        self.samp_rate = samp_rate = 32000
        self.recording_path = recording_path = f"{Path.cwd()}\\rec\\"
        self.rec_note = rec_note = "recording"
        self.raw_rec = raw_rec = qt_raw_rec_toggle and record_toggle
        self.null_path = null_path = "NUL:" if platform == "nt" else "/dev/null"
        self.gain = gain = 40
        self.frequency = frequency = 2200000000
        self.dec_rec = dec_rec = qt_dec_rec_toggle and record_toggle
        self.antenna = antenna = 'RX2'
        self.agc = agc = 'Disabled'

        ##################################################
        # Blocks
        ##################################################

        self.settings = Qt.QTabWidget()
        self.settings_widget_0 = Qt.QWidget()
        self.settings_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.settings_widget_0)
        self.settings_grid_layout_0 = Qt.QGridLayout()
        self.settings_layout_0.addLayout(self.settings_grid_layout_0)
        self.settings.addTab(self.settings_widget_0, 'RF Settings')
        self.settings_widget_1 = Qt.QWidget()
        self.settings_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.settings_widget_1)
        self.settings_grid_layout_1 = Qt.QGridLayout()
        self.settings_layout_1.addLayout(self.settings_grid_layout_1)
        self.settings.addTab(self.settings_widget_1, 'Recording Settings')
        self.top_grid_layout.addWidget(self.settings, 20, 0, 1, 11)
        for r in range(20, 21):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 11):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._recording_path_tool_bar = Qt.QToolBar(self)
        self._recording_path_tool_bar.addWidget(Qt.QLabel("Recording Location" + ": "))
        self._recording_path_line_edit = Qt.QLineEdit(str(self.recording_path))
        self._recording_path_tool_bar.addWidget(self._recording_path_line_edit)
        self._recording_path_line_edit.editingFinished.connect(
            lambda: self.set_recording_path(str(str(self._recording_path_line_edit.text()))))
        self.settings_grid_layout_1.addWidget(self._recording_path_tool_bar, 0, 0, 1, 1)
        for r in range(0, 1):
            self.settings_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.settings_grid_layout_1.setColumnStretch(c, 1)
        self._record_toggle_choices = {'Pressed': bool(1), 'Released': bool(0)}

        _record_toggle_toggle_button = qtgui.ToggleButton(self.set_record_toggle, 'Record', self._record_toggle_choices, False, 'value')
        _record_toggle_toggle_button.setColors("default", "default", "default", "default")
        self.record_toggle = _record_toggle_toggle_button

        self.top_grid_layout.addWidget(_record_toggle_toggle_button, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rec_note_tool_bar = Qt.QToolBar(self)
        self._rec_note_tool_bar.addWidget(Qt.QLabel("Recording Note" + ": "))
        self._rec_note_line_edit = Qt.QLineEdit(str(self.rec_note))
        self._rec_note_tool_bar.addWidget(self._rec_note_line_edit)
        self._rec_note_line_edit.editingFinished.connect(
            lambda: self.set_rec_note(str(str(self._rec_note_line_edit.text()))))
        self.settings_grid_layout_1.addWidget(self._rec_note_tool_bar, 1, 0, 1, 1)
        for r in range(1, 2):
            self.settings_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.settings_grid_layout_1.setColumnStretch(c, 1)
        self._frequency_range = qtgui.Range(2200000000, 2300000000, 100000, 2200000000, 200)
        self._frequency_win = qtgui.RangeWidget(self._frequency_range, self.set_frequency, "Receive Frequency", "eng_slider", float, QtCore.Qt.Horizontal)
        self.settings_grid_layout_0.addWidget(self._frequency_win, 10, 0, 1, 10)
        for r in range(10, 11):
            self.settings_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 10):
            self.settings_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            frequency, #fc
            samp_rate, #bw
            'Waterfall', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 5, 1, 5, 10)
        for r in range(5, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 11):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_ledindicator_0 = self._qtgui_ledindicator_0_win = qtgui.GrLEDIndicator('', "red", "black", record_toggle, 40, 2, 1, 1, self)
        self.qtgui_ledindicator_0 = self._qtgui_ledindicator_0_win
        self.top_grid_layout.addWidget(self._qtgui_ledindicator_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            frequency, #fc
            samp_rate, #bw
            'Frequency', #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)

        self.qtgui_freq_sink_x_0.disable_legend()


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 0, 6, 5, 5)
        for r in range(0, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 11):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "Constellation", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(True)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)

        self.qtgui_const_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_win, 0, 1, 5, 5)
        for r in range(0, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        _qt_raw_rec_toggle_check_box = Qt.QCheckBox("Raw data recording")
        self._qt_raw_rec_toggle_choices = {True: True, False: False}
        self._qt_raw_rec_toggle_choices_inv = dict((v,k) for k,v in self._qt_raw_rec_toggle_choices.items())
        self._qt_raw_rec_toggle_callback = lambda i: Qt.QMetaObject.invokeMethod(_qt_raw_rec_toggle_check_box, "setChecked", Qt.Q_ARG("bool", self._qt_raw_rec_toggle_choices_inv[i]))
        self._qt_raw_rec_toggle_callback(self.qt_raw_rec_toggle)
        _qt_raw_rec_toggle_check_box.stateChanged.connect(lambda i: self.set_qt_raw_rec_toggle(self._qt_raw_rec_toggle_choices[bool(i)]))
        self.settings_grid_layout_1.addWidget(_qt_raw_rec_toggle_check_box, 3, 0, 1, 1)
        for r in range(3, 4):
            self.settings_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.settings_grid_layout_1.setColumnStretch(c, 1)
        _qt_dec_rec_toggle_check_box = Qt.QCheckBox("Decoded data recording")
        self._qt_dec_rec_toggle_choices = {True: True, False: False}
        self._qt_dec_rec_toggle_choices_inv = dict((v,k) for k,v in self._qt_dec_rec_toggle_choices.items())
        self._qt_dec_rec_toggle_callback = lambda i: Qt.QMetaObject.invokeMethod(_qt_dec_rec_toggle_check_box, "setChecked", Qt.Q_ARG("bool", self._qt_dec_rec_toggle_choices_inv[i]))
        self._qt_dec_rec_toggle_callback(self.qt_dec_rec_toggle)
        _qt_dec_rec_toggle_check_box.stateChanged.connect(lambda i: self.set_qt_dec_rec_toggle(self._qt_dec_rec_toggle_choices[bool(i)]))
        self.settings_grid_layout_1.addWidget(_qt_dec_rec_toggle_check_box, 4, 0, 1, 1)
        for r in range(4, 5):
            self.settings_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.settings_grid_layout_1.setColumnStretch(c, 1)
        self._gain_range = qtgui.Range(0, 60, 1, 40, 200)
        self._gain_win = qtgui.RangeWidget(self._gain_range, self.set_gain, "Manual Gain (dB)", "eng_slider", float, QtCore.Qt.Horizontal)
        self.settings_grid_layout_0.addWidget(self._gain_win, 1, 1, 1, 9)
        for r in range(1, 2):
            self.settings_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 10):
            self.settings_grid_layout_0.setColumnStretch(c, 1)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, recording_path+str(datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H.%M.%S"))+rec_note+"_DECODED.bin" if dec_rec else null_path, False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, (recording_path)+(str(datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H.%M.%S")))+"_"+rec_note+"_"+str(frequency/1000000)+"MHz_"+str(samp_rate/1000000)+"Msps_RAW.bin" if raw_rec else null_path, False)
        self.blocks_file_sink_0.set_unbuffered(False)
        # Create the options list
        self._antenna_options = ['RX2', 'TRX']
        # Create the labels list
        self._antenna_labels = ['RX2', 'TRX']
        # Create the combo box
        # Create the radio buttons
        self._antenna_group_box = Qt.QGroupBox("USRP Antenna Connection" + ": ")
        self._antenna_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._antenna_button_group = variable_chooser_button_group()
        self._antenna_group_box.setLayout(self._antenna_box)
        for i, _label in enumerate(self._antenna_labels):
            radio_button = Qt.QRadioButton(_label)
            self._antenna_box.addWidget(radio_button)
            self._antenna_button_group.addButton(radio_button, i)
        self._antenna_callback = lambda i: Qt.QMetaObject.invokeMethod(self._antenna_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._antenna_options.index(i)))
        self._antenna_callback(self.antenna)
        self._antenna_button_group.buttonClicked[int].connect(
            lambda i: self.set_antenna(self._antenna_options[i]))
        self.settings_grid_layout_0.addWidget(self._antenna_group_box, 0, 0, 1, 1)
        for r in range(0, 1):
            self.settings_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.settings_grid_layout_0.setColumnStretch(c, 1)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 2, 1000))), True)
        self.analog_phase_modulator_fc_0 = analog.phase_modulator_fc(1)
        self.analog_noise_source_x_1 = analog.noise_source_c(analog.GR_GAUSSIAN, 1, 0)
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, 1, 0)
        _agc_check_box = Qt.QCheckBox("AGC")
        self._agc_choices = {True: 'Enabled', False: 'Disabled'}
        self._agc_choices_inv = dict((v,k) for k,v in self._agc_choices.items())
        self._agc_callback = lambda i: Qt.QMetaObject.invokeMethod(_agc_check_box, "setChecked", Qt.Q_ARG("bool", self._agc_choices_inv[i]))
        self._agc_callback(self.agc)
        _agc_check_box.stateChanged.connect(lambda i: self.set_agc(self._agc_choices[bool(i)]))
        self.settings_grid_layout_0.addWidget(_agc_check_box, 1, 0, 1, 1)
        for r in range(1, 2):
            self.settings_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.settings_grid_layout_0.setColumnStretch(c, 1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.record_toggle, 'state'), (self.qtgui_ledindicator_0, 'state'))
        self.connect((self.analog_noise_source_x_0, 0), (self.analog_phase_modulator_fc_0, 0))
        self.connect((self.analog_noise_source_x_1, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.analog_phase_modulator_fc_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.analog_phase_modulator_fc_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.analog_phase_modulator_fc_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_file_sink_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "OQPSK_Quarter_HSTXC")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_record_toggle(self):
        return self.record_toggle

    def set_record_toggle(self, record_toggle):
        self.record_toggle = record_toggle
        self.set_dec_rec(self.qt_dec_rec_toggle and self.record_toggle)
        self.set_raw_rec(self.qt_raw_rec_toggle and self.record_toggle)
        self.qtgui_ledindicator_0.setState(self.record_toggle)

    def get_qt_raw_rec_toggle(self):
        return self.qt_raw_rec_toggle

    def set_qt_raw_rec_toggle(self, qt_raw_rec_toggle):
        self.qt_raw_rec_toggle = qt_raw_rec_toggle
        self._qt_raw_rec_toggle_callback(self.qt_raw_rec_toggle)
        self.set_raw_rec(self.qt_raw_rec_toggle and self.record_toggle)

    def get_qt_dec_rec_toggle(self):
        return self.qt_dec_rec_toggle

    def set_qt_dec_rec_toggle(self, qt_dec_rec_toggle):
        self.qt_dec_rec_toggle = qt_dec_rec_toggle
        self.set_dec_rec(self.qt_dec_rec_toggle and self.record_toggle)
        self._qt_dec_rec_toggle_callback(self.qt_dec_rec_toggle)

    def get_platform(self):
        return self.platform

    def set_platform(self, platform):
        self.platform = platform
        self.set_null_path("NUL:" if self.platform == "nt" else "/dev/null")

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_file_sink_0.open((self.recording_path)+(str(datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H.%M.%S")))+"_"+self.rec_note+"_"+str(self.frequency/1000000)+"MHz_"+str(self.samp_rate/1000000)+"Msps_RAW.bin" if self.raw_rec else self.null_path)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.frequency, self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.frequency, self.samp_rate)

    def get_recording_path(self):
        return self.recording_path

    def set_recording_path(self, recording_path):
        self.recording_path = recording_path
        Qt.QMetaObject.invokeMethod(self._recording_path_line_edit, "setText", Qt.Q_ARG("QString", str(self.recording_path)))
        self.blocks_file_sink_0.open((self.recording_path)+(str(datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H.%M.%S")))+"_"+self.rec_note+"_"+str(self.frequency/1000000)+"MHz_"+str(self.samp_rate/1000000)+"Msps_RAW.bin" if self.raw_rec else self.null_path)
        self.blocks_file_sink_0_0.open(self.recording_path+str(datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H.%M.%S"))+self.rec_note+"_DECODED.bin" if self.dec_rec else self.null_path)

    def get_rec_note(self):
        return self.rec_note

    def set_rec_note(self, rec_note):
        self.rec_note = rec_note
        Qt.QMetaObject.invokeMethod(self._rec_note_line_edit, "setText", Qt.Q_ARG("QString", str(self.rec_note)))
        self.blocks_file_sink_0.open((self.recording_path)+(str(datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H.%M.%S")))+"_"+self.rec_note+"_"+str(self.frequency/1000000)+"MHz_"+str(self.samp_rate/1000000)+"Msps_RAW.bin" if self.raw_rec else self.null_path)
        self.blocks_file_sink_0_0.open(self.recording_path+str(datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H.%M.%S"))+self.rec_note+"_DECODED.bin" if self.dec_rec else self.null_path)

    def get_raw_rec(self):
        return self.raw_rec

    def set_raw_rec(self, raw_rec):
        self.raw_rec = raw_rec
        self.blocks_file_sink_0.open((self.recording_path)+(str(datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H.%M.%S")))+"_"+self.rec_note+"_"+str(self.frequency/1000000)+"MHz_"+str(self.samp_rate/1000000)+"Msps_RAW.bin" if self.raw_rec else self.null_path)

    def get_null_path(self):
        return self.null_path

    def set_null_path(self, null_path):
        self.null_path = null_path
        self.blocks_file_sink_0.open((self.recording_path)+(str(datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H.%M.%S")))+"_"+self.rec_note+"_"+str(self.frequency/1000000)+"MHz_"+str(self.samp_rate/1000000)+"Msps_RAW.bin" if self.raw_rec else self.null_path)
        self.blocks_file_sink_0_0.open(self.recording_path+str(datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H.%M.%S"))+self.rec_note+"_DECODED.bin" if self.dec_rec else self.null_path)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.blocks_file_sink_0.open((self.recording_path)+(str(datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H.%M.%S")))+"_"+self.rec_note+"_"+str(self.frequency/1000000)+"MHz_"+str(self.samp_rate/1000000)+"Msps_RAW.bin" if self.raw_rec else self.null_path)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.frequency, self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.frequency, self.samp_rate)

    def get_dec_rec(self):
        return self.dec_rec

    def set_dec_rec(self, dec_rec):
        self.dec_rec = dec_rec
        self.blocks_file_sink_0_0.open(self.recording_path+str(datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H.%M.%S"))+self.rec_note+"_DECODED.bin" if self.dec_rec else self.null_path)

    def get_antenna(self):
        return self.antenna

    def set_antenna(self, antenna):
        self.antenna = antenna
        self._antenna_callback(self.antenna)

    def get_agc(self):
        return self.agc

    def set_agc(self, agc):
        self.agc = agc
        self._agc_callback(self.agc)




def main(top_block_cls=OQPSK_Quarter_HSTXC, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
