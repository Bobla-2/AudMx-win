from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QWidget
from PySide6.QtCore import QTimer, Signal, QCoreApplication, QPoint
from ..ENUM.enums import LIGHT_MODE


class SystemTrayIcon(QSystemTrayIcon):           #класс приложения в трее
    flag_warning = True
    SignalLIghtMode = Signal(int)
    SignalActSet = Signal()
    SignalButtonExit = Signal()
    def __init__(self, parent=None):
        QSystemTrayIcon.__init__(self, parent)
        self.setToolTip("AudMX")
        self.menu = QMenu(parent)

        self.menu_light = self.menu.addMenu("light")
        self.settings = self.menu.addAction("setting")
        self.Action2 = self.menu.addAction("Action2")
        self.exitAction = self.menu.addAction("EXIT")

        self.Action_light1 = self.menu_light.addAction("white")
        self.Action_light2 = self.menu_light.addAction("wave")
        self.Action_light3 = self.menu_light.addAction("volume_level")

        self.setContextMenu(self.menu)
        self.Action_light1.triggered.connect(lambda : self.SignalLIghtMode.emit(LIGHT_MODE.WHITE.value))
        self.Action_light2.triggered.connect(lambda : self.SignalLIghtMode.emit(LIGHT_MODE.WAVE.value))
        self.Action_light3.triggered.connect(lambda : self.SignalLIghtMode.emit(LIGHT_MODE.VOLUME_LEVEL.value))
        self.exitAction.triggered.connect(self.exit)
        self.Action2.triggered.connect(self.action2)
        self.settings.triggered.connect(self.actSet)
        self.activated.connect(self.onTrayIconActivated)

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # Left click
            cursor_position = QCursor.pos()
            # self.menu.show()#(QPoint(cursor_position.x(), cursor_position.y() - 110))
            # self.menu.popup(QPoint(cursor_position.x(), cursor_position.y() - 110))
    def actSet(self):
        self.SignalActSet.emit()

    def setFont(self, font):
        self.exitAction.setFont(font)
        self.Action2.setFont(font)

    def exit(self):
        self.SignalButtonExit.emit()

    def action2(self):
        if self.flag_warning:
            self.showMessage("hui", "sosi hui")
    def masegeIconWarning(self, file_name: str):
        if self.flag_warning:
            self.showMessage("ERROR ICON", "icon: '" + file_name + "' don't have size 60x44px")
