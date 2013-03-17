import sys
import threading
from PySide.QtCore import *
from PySide.QtGui import *


class GUI(QWidget):

    def __init__(self):
        super(GUI, self).__init__()
        self._pom = Pomodoro()
        self._pom.ringer.connect(self.signal)
        self.initUI()

    def signal(self, pomodori):
        if (pomodori % 4 == 0 and pomodori != 0):
            self._tray.showMessage("4 Pomodori has passed!",
                                "Take a long break: 15-30min",
                                QSystemTrayIcon.Information)
        else:
            self._tray.showMessage("Pomodoro's up!",
                                 "Take a short break: 3-5min",
                                 QSystemTrayIcon.Information)
        self._tray.setIcon(QIcon("greentomato.png"))

    def initTray(self):
        self._tray = QSystemTrayIcon(QIcon("redtomato.png"))
        traymenu = QMenu("Menu")
        self._tray.setContextMenu(traymenu)
        self._tray.show()
        self._tray.activated.connect(self.Tray_click)

        setTimerTray = QLineEdit()
        setTimerTray.setPlaceholderText("Set timer")
        setTimerTray.textChanged.connect(lambda:
                                    self.updateTimerText(setTimerTray.text()))
        traywidget = QWidgetAction(setTimerTray)
        traywidget.setDefaultWidget(setTimerTray)
        traymenu.addAction(traywidget)

        startTimerAction = QAction("&Start Timer", self)
        startTimerAction.triggered.connect(self.StartTimer_click)
        traymenu.addAction(startTimerAction)

        exitAction = QAction("&Exit", self)
        exitAction.triggered.connect(QCoreApplication.instance().quit)
        traymenu.addAction(exitAction)

    def Tray_click(self, activation):
        if activation == QSystemTrayIcon.DoubleClick:
            self.show()
        elif activation == QSystemTrayIcon.Context:
            self._tray.show()

    def closeEvent(self, event):
        self._tray.showMessage("Running in system tray",
                                """The program will keep running in the system tray.\n To terminate the program choose quit from the context menu""",
                                QSystemTrayIcon.Information)
        self.hide()
        event.ignore()

    def wheelEvent(self, event):
        if event.delta() > 0:
            timervalue = int(self.settimertext.text())
            timervalue = timervalue + 1
            self.settimertext.setText(str(timervalue))
        else:
            timervalue = int(self.settimertext.text())
            timervalue = timervalue - 1
            self.settimertext.setText(str(timervalue))

    def initUI(self):
        self.initTray()
        resolution = QApplication.desktop().availableGeometry()
        width = 150
        height = 100

        # place exactly in center of screen
        self.setGeometry((resolution.width() / 2) - (width / 2),
                         (resolution.height() / 2) - (height / 2),
                          width, height)
        self.setWindowTitle("Pomodoro")
        self.setWindowIcon(QIcon("redtomato.png"))

        grid = QGridLayout()
        grid.setSpacing(5)
        self.settimertext = QLineEdit()
        grid.addWidget(self.settimertext, 1, 0)

        self.errortext = QLabel()
        grid.addWidget(self.errortext, 2, 0)
        self.errortext.hide()

        self.settimertext.setText(str(25))
        self.settimertext.textChanged.connect(lambda:
                                self.updateTimerText(self.settimertext.text()))

        self.starttimerbutton = QPushButton("start timer")
        grid.addWidget(self.starttimerbutton, 3, 0)
        self.starttimerbutton.clicked.connect(self.StartTimer_click)

        self.setLayout(grid)

    def StartTimer_click(self):
        self._pom.startTimer()
        self._tray.setIcon(QIcon("redtomato.png"))

    def updateTimerText(self, number):
        try:
            self._pom.setTimerMinutes(int(number))
            self.errortext.hide()
        except ValueError:
            self.errortext.setText("Please input a number")
            self.errortext.show()


class Pomodoro(QObject):

    ringer = Signal(int)

    def __init__(self):
        # initializes Pomodoro as a QObject so it can emit signals
        QObject.__init__(self)
        self._pomodori = 0
        self._timerminutes = 25

    def setTimerMinutes(self, minutes):
        if (minutes > 0):
            self._timerminutes = minutes
        else:
            raise Exception("minutes cannot be lower than zero")

    def ring(self):
        self._pomodori = self._pomodori + 1
        self.ringer.emit(self._pomodori)

    def startTimer(self):
        self.timer = threading.Timer(self._timerminutes * 60, self.ring)
        self.timer.start()
        self.running = True


def main():
    app = QApplication(sys.argv)
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "no tray", "no system tray was found")
        sys.exit(1)
    g = GUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
