#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Watermark_Pattern_TX
# Author: Meles Weldegebriel
# Copyright: 2024
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
import sip

class Watermark_Pattern_TX(gr.top_block, Qt.QWidget):
    def __init__(self, Carrier_freq=3385e6, Constant=0.5, TX_gain=25, Samp_rate=1000000):
    # def __init__(self):
        gr.top_block.__init__(self, "Watermark_Pattern_TX", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Watermark_Pattern_TX")
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

        self.settings = Qt.QSettings("GNU Radio", "Watermark_Pattern_TX")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
                
        self.TX_gain = TX_gain
        self.Samp_rate = Samp_rate 
        self.Constant = Constant 
        self.Carrier_freq = Carrier_freq
#         self.TX_gain = TX_gain = 25
#         self.Samp_rate = Samp_rate = 1000000
#         self.Constant = Constant = 0.5
#         self.Carrier_freq = Carrier_freq = 3385000000

        ##################################################
        # Blocks
        ##################################################

        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(Samp_rate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0.set_center_freq(Carrier_freq, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_bandwidth(Samp_rate, 0)
        self.uhd_usrp_sink_0.set_gain(TX_gain, 0)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            512, #size
            Samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.1)
        self.qtgui_time_sink_x_0.set_y_axis(-2.0, 2.0)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(Constant)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, 'TX_image_data.iq', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Watermark_Pattern_TX")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_TX_gain(self):
        return self.TX_gain

    def set_TX_gain(self, TX_gain):
        self.TX_gain = TX_gain
        self.uhd_usrp_sink_0.set_gain(self.TX_gain, 0)

    def get_Samp_rate(self):
        return self.Samp_rate

    def set_Samp_rate(self, Samp_rate):
        self.Samp_rate = Samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.Samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.Samp_rate)
        self.uhd_usrp_sink_0.set_bandwidth(self.Samp_rate, 0)

    def get_Constant(self):
        return self.Constant

    def set_Constant(self, Constant):
        self.Constant = Constant
        self.blocks_multiply_const_vxx_0.set_k(self.Constant)

    def get_Carrier_freq(self):
        return self.Carrier_freq

    def set_Carrier_freq(self, Carrier_freq):
        self.Carrier_freq = Carrier_freq
        self.uhd_usrp_sink_0.set_center_freq(self.Carrier_freq, 0)

def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-f", "--Carrier-freq", dest="Carrier_freq", type=eng_float, default="3.385G",
        help="Set Carrier_freq [default=%(default)r]")
    parser.add_argument(
        "-c", "--Constant", dest="Constant", type=eng_float, default="500.0m",
        help="Set Constant [default=%(default)r]")
    parser.add_argument(
        "-g", "--TX_gain", dest="TX_gain", type=eng_float, default="25.0",
        help="Set TX_gain [default=%(default)r]")
    parser.add_argument(
        "-s", "--Samp-rate", dest="Samp_rate", type=eng_float, default="1.0M",
        help="Set Samp_rate [default=%(default)r]")
    return parser

def main(top_block_cls=Watermark_Pattern_TX, options=None):
    
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(Carrier_freq=options.Carrier_freq, Constant=options.Constant, TX_gain=options.TX_gain, Samp_rate=options.Samp_rate)
    
#     tb = top_block_cls()

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
