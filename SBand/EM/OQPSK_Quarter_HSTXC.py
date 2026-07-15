#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: [EX3-CM] S Band Receiver
# GNU Radio version: 3.9.8.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from datetime import datetime
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import fec
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
from os import name
from pathlib import Path
import satellites
import satellites.hier
import time



from gnuradio import qtgui

class OQPSK_Quarter_HSTXC(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "[EX3-CM] S Band Receiver", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("[EX3-CM] S Band Receiver")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
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

        self.settings = Qt.QSettings("GNU Radio", "OQPSK_Quarter_HSTXC")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.record_toggle = record_toggle = 0
        self.qt_raw_rec_toggle = qt_raw_rec_toggle = True
        self.qt_dec_rec_toggle = qt_dec_rec_toggle = True
        self.platform = platform = name
        self.nfilts = nfilts = 32
        self.timestamp = timestamp = str(datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H.%M.%S"))
        self.samp_rate = samp_rate = 4000000
        self.samp_per_sym = samp_per_sym = 4
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts,nfilts,1/float(4),0.35,11*4*nfilts)
        self.recording_path = recording_path = f"{Path.cwd()}\\rec\\"
        self.rec_note = rec_note = "recording"
        self.raw_rec = raw_rec = qt_raw_rec_toggle and record_toggle
        self.qpsk_const = qpsk_const = digital.constellation_rect([-0.707-0.707j, -0.707+0.707j, 0.707-0.707j, 0.707+0.707j], [0, 1, 2, 3],
        4, 2, 2, 1, 1).base()
        self.null_path = null_path = "NUL:" if platform == "nt" else "/dev/null"
        self.gain = gain = 40
        self.frequency = frequency = 2200000000
        self.freq = freq = 2200000000
        self.dec_rec = dec_rec = qt_dec_rec_toggle and record_toggle
        self.dec_cc = dec_cc = fec.cc_decoder.make(2048,7, 2, [83,113], 0, -1, fec.CC_STREAMING, False)
        self.center_freq = center_freq = 0
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
        if bool == bool:
        	self._record_toggle_choices = {'Pressed': bool(1), 'Released': bool(0)}
        elif bool == str:
        	self._record_toggle_choices = {'Pressed': "1".replace("'",""), 'Released': "0".replace("'","")}
        else:
        	self._record_toggle_choices = {'Pressed': 1, 'Released': 0}

        _record_toggle_toggle_button = qtgui.ToggleButton(self.set_record_toggle, 'Record', self._record_toggle_choices, False,"'value'".replace("'",""))
        _record_toggle_toggle_button.setColors("default","default","default","default")
        self.record_toggle = _record_toggle_toggle_button

        self.top_grid_layout.addWidget(_record_toggle_toggle_button, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._frequency_range = Range(2200000000, 2300000000, 100000, 2200000000, 200)
        self._frequency_win = RangeWidget(self._frequency_range, self.set_frequency, "Receive Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.settings_grid_layout_0.addWidget(self._frequency_win, 10, 0, 1, 10)
        for r in range(10, 11):
            self.settings_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 10):
            self.settings_grid_layout_0.setColumnStretch(c, 1)
        self.satellites_rms_agc_0_0 = satellites.hier.rms_agc(alpha=1e-2, reference=1)
        self.satellites_descrambler308_0 = satellites.descrambler308()
        self._recording_path_tool_bar = Qt.QToolBar(self)
        self._recording_path_tool_bar.addWidget(Qt.QLabel("Recording Location" + ": "))
        self._recording_path_line_edit = Qt.QLineEdit(str(self.recording_path))
        self._recording_path_tool_bar.addWidget(self._recording_path_line_edit)
        self._recording_path_line_edit.returnPressed.connect(
            lambda: self.set_recording_path(str(str(self._recording_path_line_edit.text()))))
        self.settings_grid_layout_1.addWidget(self._recording_path_tool_bar, 0, 0, 1, 1)
        for r in range(0, 1):
            self.settings_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.settings_grid_layout_1.setColumnStretch(c, 1)
        self._rec_note_tool_bar = Qt.QToolBar(self)
        self._rec_note_tool_bar.addWidget(Qt.QLabel("Recording Note" + ": "))
        self._rec_note_line_edit = Qt.QLineEdit(str(self.rec_note))
        self._rec_note_tool_bar.addWidget(self._rec_note_line_edit)
        self._rec_note_line_edit.returnPressed.connect(
            lambda: self.set_rec_note(str(str(self._rec_note_line_edit.text()))))
        self.settings_grid_layout_1.addWidget(self._rec_note_tool_bar, 1, 0, 1, 1)
        for r in range(1, 2):
            self.settings_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.settings_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win, 5, 1, 5, 10)
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
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
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
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(True)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
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
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_win)
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
        self._gain_range = Range(0, 60, 1, 40, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, "Manual Gain (dB)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.settings_grid_layout_0.addWidget(self._gain_win, 1, 1, 1, 9)
        for r in range(1, 2):
            self.settings_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 10):
            self.settings_grid_layout_0.setColumnStretch(c, 1)
        self.fec_extended_decoder_0_0_1 = fec.extended_decoder(decoder_obj_list=dec_cc, threading= None, ann=None, puncpat='11', integration_period=10000)
        self.digital_pfb_clock_sync_xxx_0_0 = digital.pfb_clock_sync_ccf(samp_per_sym, 0.001, rrc_taps, nfilts, 0, 0.1, 1)
        self.digital_map_bb_1 = digital.map_bb([-1, 1])
        self.digital_map_bb_0 = digital.map_bb([0, 1, 2, 3])
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2, digital.DIFF_DIFFERENTIAL)
        self.digital_costas_loop_cc_1 = digital.costas_loop_cc(0.01, 4, False)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(qpsk_const)
        self._center_freq_range = Range(-50000, 50000, 50, 0, 200)
        self._center_freq_win = RangeWidget(self._center_freq_range, self.set_center_freq, "center_freq", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._center_freq_win)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(2)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/sam/Downloads/hstxc_2mbit_oqpsk_noscram_testmode_4msamp.bin', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_char*1, '/home/sam/absat/ex3_sdr/SBand/EM/outputtest.txt', False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blocks_char_to_float_1 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
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
        self.connect((self.blocks_char_to_float_0, 0), (self.fec_extended_decoder_0_0_1, 0))
        self.connect((self.blocks_char_to_float_1, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.blocks_throttle_0, 0), (self.satellites_rms_agc_0_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.digital_map_bb_1, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_map_bb_0, 0))
        self.connect((self.digital_costas_loop_cc_1, 0), (self.digital_pfb_clock_sync_xxx_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.satellites_descrambler308_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.digital_map_bb_1, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.fec_extended_decoder_0_0_1, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.satellites_descrambler308_0, 0), (self.blocks_char_to_float_1, 0))
        self.connect((self.satellites_descrambler308_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.satellites_rms_agc_0_0, 0), (self.digital_costas_loop_cc_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "OQPSK_Quarter_HSTXC")
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

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts,self.nfilts,1/float(4),0.35,11*4*self.nfilts))

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.frequency, self.samp_rate)

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0_0.update_taps(self.rrc_taps)

    def get_recording_path(self):
        return self.recording_path

    def set_recording_path(self, recording_path):
        self.recording_path = recording_path
        Qt.QMetaObject.invokeMethod(self._recording_path_line_edit, "setText", Qt.Q_ARG("QString", str(self.recording_path)))

    def get_rec_note(self):
        return self.rec_note

    def set_rec_note(self, rec_note):
        self.rec_note = rec_note
        Qt.QMetaObject.invokeMethod(self._rec_note_line_edit, "setText", Qt.Q_ARG("QString", str(self.rec_note)))

    def get_raw_rec(self):
        return self.raw_rec

    def set_raw_rec(self, raw_rec):
        self.raw_rec = raw_rec

    def get_qpsk_const(self):
        return self.qpsk_const

    def set_qpsk_const(self, qpsk_const):
        self.qpsk_const = qpsk_const

    def get_null_path(self):
        return self.null_path

    def set_null_path(self, null_path):
        self.null_path = null_path

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.qtgui_freq_sink_x_0.set_frequency_range(self.frequency, self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_dec_rec(self):
        return self.dec_rec

    def set_dec_rec(self, dec_rec):
        self.dec_rec = dec_rec

    def get_dec_cc(self):
        return self.dec_cc

    def set_dec_cc(self, dec_cc):
        self.dec_cc = dec_cc

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq

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

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

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
