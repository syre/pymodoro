# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import threading
from PyQt5.QtCore import QObject, pyqtSignal


class Pomodoro(QObject):
    """
        Model class for Pymodoro
    """
    ringer = pyqtSignal(int)

    def __init__(self):
        # initializes Pomodoro as a QObject so it can emit signals
        QObject.__init__(self)
        self.pomodori = 0
        self.pomodoro_duration = 25
        self.running = False
        self.timer = threading.Timer(self.pomodoro_duration * 60, self.ring)

    def set_timer_minutes(self, minutes):
        """
        Sets the pomodoro duration in minutes, cannot be lower than zero
        """
        if minutes > 0:
            self.pomodoro_duration = minutes
        else:
            raise ValueError("minutes cannot be lower or equal to zero")

    def ring(self):
        """
            Called when a pomodoro has passed
        """
        self.pomodori += 1
        self.ringer.emit(self.pomodori)
        self.running = False

    def start_timer(self):
        """
            Starts the pomodoro timer
        """
        self.timer = threading.Timer(self.pomodoro_duration * 60, self.ring)
        self.timer.start()
        self.running = True
