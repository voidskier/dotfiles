#!/bin/python3

import sys
import threading
import time
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPainter, QPen, QColor
from Xlib import X, display
from Xlib.ext import record
from Xlib.protocol import rq

class ClockLabel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.X11BypassWindowManagerHint)

        self.setStyleSheet("background-color: black; color: #007FFF;")

        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.time_label.setStyleSheet("font-family:'DSEG7 Classic Mini'; font-size:112px;")

        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.date_label.setStyleSheet("font-family:'Arial'; font-size:24px;")

        layout = QVBoxLayout()
        layout.addWidget(self.time_label)
        layout.addStretch()
        layout.addWidget(self.date_label)
        layout.setContentsMargins(8, 32, 8, 24)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(10)
        self.update_time()

        screen = QApplication.primaryScreen().availableGeometry()
        width, height = 640, 210
        self.setGeometry(screen.width() - width - 20, screen.height() - height - 20, width, height)

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%A, %d %B %Y")
        self.time_label.setText(current_time)
        self.date_label.setText(current_date)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QColor("#005fff"))
        pen.setWidth(6)
        painter.setPen(pen)
        radius = 19
        painter.drawRoundedRect(1, 1, self.width()-2, self.height()-2, radius, radius)

app = QApplication(sys.argv)

clock = ClockLabel()
clock.hide()

# Connect to X server
local_dpy = display.Display()
record_dpy = display.Display()

# Super_L keycode
super_keycode = local_dpy.keysym_to_keycode(0xffeb)

def handler(reply):
    if reply.category != record.FromServer:
        return
    if reply.client_swapped:
        return
    if not reply.data:
        return

    data = reply.data
    while data:
        event, data = rq.EventField(None).parse_binary_value(
            data, record_dpy.display, None, None
        )
        if event.type == X.KeyPress and event.detail == super_keycode:
            if not clock.isVisible():
                clock.show()
        elif event.type == X.KeyRelease and event.detail == super_keycode:
            if clock.isVisible():
                clock.hide()

def x_listener():
    ctx = record_dpy.record_create_context(
        0,
        [record.AllClients],
        [{
            'core_requests': (0, 0),
            'core_replies': (0, 0),
            'ext_requests': (0, 0, 0, 0),
            'ext_replies': (0, 0, 0, 0),
            'delivered_events': (0, 0),
            'device_events': (X.KeyPress, X.KeyRelease),
            'errors': (0, 0),
            'client_started': False,
            'client_died': False,
        }]
    )
    record_dpy.record_enable_context(ctx, handler)
    record_dpy.record_free_context(ctx)

threading.Thread(target=x_listener, daemon=True).start()
sys.exit(app.exec())
