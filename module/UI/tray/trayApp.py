from PySide6.QtWidgets import QMenu, QSystemTrayIcon
from PySide6.QtCore import Signal
# from module.ENUM.enums import LIGHT_MODE


class SystemTrayIcon(QSystemTrayIcon):  # класс приложения в трее
    flag_warning = True
    # SignalLIghtMode = Signal(int)
    SignalActSet = Signal()
    SignalChangeBluSer = Signal()
    SignalButtonExit = Signal()

    def __init__(self, parent=None):
        QSystemTrayIcon.__init__(self, parent)
        self.setToolTip("AudMX")
        self.menu = QMenu(parent)

        print(self.menu.parent())

        self.settings = self.menu.addAction("setting")
        self.Action2 = self.menu.addAction("set BLU")
        self.exitAction = self.menu.addAction("EXIT")

        self.setContextMenu(self.menu)
        self.exitAction.triggered.connect(self.exit)
        self.Action2.triggered.connect(self.action2)
        self.settings.triggered.connect(self.actSet)
        self.activated.connect(self.onTrayIconActivated)

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # Left click
            pass

    def actSet(self):
        self.SignalActSet.emit()

    def setFont(self, font):
        self.exitAction.setFont(font)
        self.Action2.setFont(font)

    def exit(self):
        self.SignalButtonExit.emit()

    def action2(self):
        if self.Action2.text() == "set BLU":
            self.Action2.setText("set USB")
        else:
            self.Action2.setText("set BLU")
        self.SignalChangeBluSer.emit()

    def masegeIconWarning(self, file_name: str):
        if self.flag_warning:
            self.showMessage("ERROR ICON", "icon: '" + file_name + "' don't have size 60x44px")

    def masegeWarningBLE(self):
        if self.flag_warning:
            self.showMessage("ERROR BLUETOOTH", "bluet. off")
            self.show()
