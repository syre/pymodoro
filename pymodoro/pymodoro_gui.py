# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QLineEdit, QWidgetAction, QAction, QGridLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, QCoreApplication
from PyQt5.QtGui import QIcon
from pomodoro import Pomodoro


class PymodoroGUI(QWidget):
    """
        GUI for Pymodoro
    """
    def __init__(self):
        """
            Initializer for the Pomodoro GUI class
        """
        super(PymodoroGUI, self).__init__()

        self.res_dir = os.path.join("../ext/")
        self.green_tomato_icon = os.path.join(self.res_dir, "greentomato.png")
        self.red_tomato_icon = os.path.join(self.res_dir, "redtomato.png")
        self.tray = QSystemTrayIcon(QIcon(self.green_tomato_icon))
        self.pom = Pomodoro()
        self.pom.ringer.connect(self.signal)
        self.init_ui()

    def signal(self, pomodori):
        """
            Callback given to the Pomodoro class.
            Called when a pomodoro is up
        """
        if pomodori % 4 == 0 and pomodori != 0:
            self.tray.showMessage("4 Pomodori has passed!",
                                   "Take a long break: 15-30min",
                                   QSystemTrayIcon.Information)
        else:
            self.tray.showMessage("Pomodoro's up!",
                                   "Take a short break: 3-5min",
                                   QSystemTrayIcon.Information)
        self.tray.setIcon(QIcon(self.green_tomato_icon))

    def init_tray(self):
        """
            Initializes the systray menu
        """
        traymenu = QMenu("Menu")
        self.tray.setContextMenu(traymenu)
        self.tray.show()
        self.tray.activated.connect(self.tray_click)
        self.tray.setToolTip("Pomodori: "+str(self.pom.pomodori))

        set_timer_tray = QLineEdit()
        set_timer_tray.setPlaceholderText("Set timer")
        set_timer_tray.textChanged.connect(lambda:
                                           self.update_timer_text(set_timer_tray.text()))
        traywidget = QWidgetAction(set_timer_tray)
        traywidget.setDefaultWidget(set_timer_tray)
        traymenu.addAction(traywidget)

        start_timer_action = QAction("&Start Timer", self)
        start_timer_action.triggered.connect(self.start_timer_click)
        traymenu.addAction(start_timer_action)

        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(QCoreApplication.instance().quit)
        traymenu.addAction(exit_action)

    def tray_click(self, activation):
        """
            Method called when clicking the tray icon
        """
        if activation == QSystemTrayIcon.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show()
        elif activation == QSystemTrayIcon.Context:
            self._tray.show()

    def close_event(self, event):
        self._tray.showMessage("Running in system tray",
                                """The program will keep running in the system tray.\n
                                To terminate the program choose exit from the context menu""",
                                QSystemTrayIcon.Information)
        self.hide()
        event.ignore()

    def wheel_event(self, event):
        if event.delta() > 0:
            timervalue = int(self.settimertext.text())
            timervalue = timervalue + 1
            self.settimertext.setText(str(timervalue))
        else:
            timervalue = int(self.settimertext.text())
            timervalue = timervalue - 1
            self.settimertext.setText(str(timervalue))

    def init_ui(self):
        """
            Initializes the GUI
        """
        self.init_tray()
        resolution = QApplication.desktop().availableGeometry()
        width = 150
        height = 100

        # place exactly in center of screen
        self.setGeometry((resolution.width() / 2) - (width / 2),
                         (resolution.height() / 2) - (height / 2),
                         width, height)
        self.setWindowTitle("Pomodoro")
        self.setWindowIcon(QIcon(os.path.join(self.res_dir, "redtomato.png")))

        grid = QGridLayout()
        grid.setSpacing(5)
        self.settimertext = QLineEdit()
        grid.addWidget(self.settimertext, 1, 0)

        self.errortext = QLabel()
        grid.addWidget(self.errortext, 2, 0)
        self.errortext.hide()

        self.settimertext.setText(str(25))
        self.settimertext.textChanged.connect(lambda:
                                              self.update_timer_text(
                                                 self.settimertext.text()))

        self.start_timerbutton = QPushButton("start timer")
        grid.addWidget(self.start_timerbutton, 3, 0)
        self.start_timerbutton.clicked.connect(self.start_timer_click)

        self.setLayout(grid)
        self.show()

    def start_timer_click(self):
        """
            Method run when starting the pomodoro timer
        """
        self.pom.start_timer()
        self.tray.setIcon(QIcon(self.red_tomato_icon))
        self.hide()

    def update_timer_text(self, number):
        """
            Method run when setting the number of minutes in the timer
        """
        try:
            self.pom.set_timer_minutes(int(number))
            self.errortext.hide()
        except ValueError:
            self.errortext.setText("Please input a number")
            self.errortext.show()

if __name__ == '__main__':
    APP = QApplication(sys.argv)
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "no tray", "no system tray was found")
        sys.exit(1)
    GUI = PymodoroGUI()
    sys.exit(APP.exec_())
