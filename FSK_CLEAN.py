#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FSK DEMODULATION
# Author: pi
# GNU Radio version: 3.10.5.1

from packaging.version import Version as StrictVersion

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
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
import math
from gnuradio import digital
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import gpredict
import satellites
import satellites.components.demodulators



from gnuradio import qtgui

class FSK_CLEAN(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FSK DEMODULATION", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FSK DEMODULATION")
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

        self.settings = Qt.QSettings("GNU Radio", "FSK_CLEAN")

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
        self.samp_rate = samp_rate = 96000
        self.maxvalue = maxvalue = -30
        self.freq_shift = freq_shift = 0
        self.freq = freq = 437500000

        ##################################################
        # Blocks
        ##################################################

        self._maxvalue_range = Range(-100, 0, 10, -30, 200)
        self._maxvalue_win = RangeWidget(self._maxvalue_range, self.set_maxvalue, "Waterfall maximum intensity", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._maxvalue_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_shift_range = Range(-10000, 10000, 100, 0, 200)
        self._freq_shift_win = RangeWidget(self._freq_shift_range, self.set_freq_shift, "Manual frequency shift", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._freq_shift_win, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.soapy_plutosdr_source_0 = None
        dev = 'driver=plutosdr'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_plutosdr_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_plutosdr_source_0.set_sample_rate(0, samp_rate)
        self.soapy_plutosdr_source_0.set_bandwidth(0, int(samp_rate))
        self.soapy_plutosdr_source_0.set_gain_mode(0, False)
        self.soapy_plutosdr_source_0.set_frequency(0, freq)
        self.soapy_plutosdr_source_0.set_gain(0, min(max(60, 0.0), 73.0))
        self.satellites_nrzi_decode_0_0 = satellites.nrzi_decode()
        self.satellites_hdlc_deframer_1_0 = satellites.hdlc_deframer(check_fcs=True, max_length=10000)
        self.satellites_fsk_demodulator_0 = satellites.components.demodulators.fsk_demodulator(baudrate = 9600, samp_rate = samp_rate, iq = True, subaudio = False, options="")
        self.qtgui_waterfall_sink_x_1 = qtgui.waterfall_sink_c(
            2048, #size
            window.WIN_HAMMING, #wintype
            0, #fc
            samp_rate, #bw
            '', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_1.set_update_time(0.04)
        self.qtgui_waterfall_sink_x_1.enable_grid(True)
        self.qtgui_waterfall_sink_x_1.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_1.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_1.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_1.set_intensity_range(-140, maxvalue)

        self._qtgui_waterfall_sink_x_1_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_1.qwidget(), Qt.QWidget)

        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_1_win, 0, 0, 5, 1)
        for r in range(0, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_ledindicator_0 = self._qtgui_ledindicator_0_win = qtgui.GrLEDIndicator("AOS", "green", "red", False, 40, 1, 1, 1, self)
        self.qtgui_ledindicator_0 = self._qtgui_ledindicator_0_win
        self.top_grid_layout.addWidget(self._qtgui_ledindicator_0_win, 4, 1, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            4096, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            '', #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.04)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.05)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



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
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_edit_box_msg_0 = qtgui.edit_box_msg(qtgui.FLOAT, '', 'Doppler corrected frequency', True, True, 'freq', None)
        self._qtgui_edit_box_msg_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_edit_box_msg_0_win, 3, 1, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.gpredict_doppler_0_0 = gpredict.doppler('0.0.0.0', 4532, False)
        self.gpredict_MsgPairToVar_0_0 = gpredict.MsgPairToVar(self.set_freq)
        self.digital_descrambler_bb_0_0_0 = digital.descrambler_bb(0x21, 0x00, 16)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_message_debug_0_1 = blocks.message_debug(True)
        self.blocks_message_debug_0_0 = blocks.message_debug(True)
        self.blocks_freqshift_cc_0 = blocks.rotator_cc(2.0*math.pi*freq_shift/samp_rate)
        self.blocks_correctiq_0 = blocks.correctiq()


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.gpredict_doppler_0_0, 'state'), (self.blocks_message_debug_0_0, 'print'))
        self.msg_connect((self.gpredict_doppler_0_0, 'freq'), (self.gpredict_MsgPairToVar_0_0, 'inpair'))
        self.msg_connect((self.gpredict_doppler_0_0, 'freq'), (self.qtgui_edit_box_msg_0, 'val'))
        self.msg_connect((self.gpredict_doppler_0_0, 'state'), (self.qtgui_ledindicator_0, 'state'))
        self.msg_connect((self.satellites_hdlc_deframer_1_0, 'out'), (self.blocks_message_debug_0_1, 'print'))
        self.connect((self.blocks_correctiq_0, 0), (self.blocks_freqshift_cc_0, 0))
        self.connect((self.blocks_freqshift_cc_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_freqshift_cc_0, 0), (self.qtgui_waterfall_sink_x_1, 0))
        self.connect((self.blocks_freqshift_cc_0, 0), (self.satellites_fsk_demodulator_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.satellites_nrzi_decode_0_0, 0))
        self.connect((self.digital_descrambler_bb_0_0_0, 0), (self.satellites_hdlc_deframer_1_0, 0))
        self.connect((self.satellites_fsk_demodulator_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.satellites_nrzi_decode_0_0, 0), (self.digital_descrambler_bb_0_0_0, 0))
        self.connect((self.soapy_plutosdr_source_0, 0), (self.blocks_correctiq_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "FSK_CLEAN")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*self.freq_shift/self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_waterfall_sink_x_1.set_frequency_range(0, self.samp_rate)
        self.soapy_plutosdr_source_0.set_sample_rate(0, self.samp_rate)
        self.soapy_plutosdr_source_0.set_bandwidth(0, int(self.samp_rate))

    def get_maxvalue(self):
        return self.maxvalue

    def set_maxvalue(self, maxvalue):
        self.maxvalue = maxvalue
        self.qtgui_waterfall_sink_x_1.set_intensity_range(-140, self.maxvalue)

    def get_freq_shift(self):
        return self.freq_shift

    def set_freq_shift(self, freq_shift):
        self.freq_shift = freq_shift
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*self.freq_shift/self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.soapy_plutosdr_source_0.set_frequency(0, self.freq)




def main(top_block_cls=FSK_CLEAN, options=None):

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
