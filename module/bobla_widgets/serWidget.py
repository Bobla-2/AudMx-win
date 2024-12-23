from PyQt5.QtWidgets import QWidget, QPushButton, QFrame, QComboBox, QLabel
from typing import List

class SerialUi(QFrame):
    def __init__(self, phather, color="grei", touch_mode=False):
        super().__init__()
        self.__touch_mode = touch_mode
        self.setParent(phather)

        # self.move(450, 0)

        self.port_combo_box = QComboBox(self)
        self.serial_but = QPushButton('connect', self)

        self.__serial_work_indicator = QLabel('', self)

        self.setIndicatorState(False)
        if color == "grei":
            self.setObjectName("grei")
        else:
            self.setObjectName("white")
            self.serial_but.setObjectName("grei")
        self.resize_()

    def resize_(self):
        if self.__touch_mode == False:
            self.setFixedSize(150, 100)
            self.port_combo_box.move(10, 10)
            self.serial_but.move(10, 55)
            self.port_combo_box.setFixedSize(90, 35)
            self.serial_but.setFixedSize(130, 35)
            self.__serial_work_indicator.move(110, 10)
            self.__serial_work_indicator.setFixedSize(30, 35)
        else:
            self.setFixedSize(330, 120)
            self.port_combo_box.move(10, 45)
            self.port_combo_box.setFixedSize(140, 65)
            self.serial_but.move(180, 10)
            self.serial_but.setFixedSize(140, 100)
            self.__serial_work_indicator.move(10, 10)
            self.__serial_work_indicator.setFixedSize(140, 25)

    def move(self, x, y):
        super().move(x, y)

    @property
    def items(self):
        return ([item for item in list(self.__dict__.values()) if
                 issubclass(type(item), QWidget)])

    def blockUI(self, block: bool):
        self.port_combo_box.setDisabled(block)
        self.serial_but.setDisabled(block)

    def setStateWork(self, state: bool):
        self.port_combo_box.setDisabled(state)
        self.setIndicatorState(state)

    def setIndicatorState(self, state: bool):
        if state:
            self.serial_but.setText("disconnect")
            self.__serial_work_indicator.setStyleSheet("background-color: #99FF99;")
        else:
            self.serial_but.setText("connect")
            self.__serial_work_indicator.setStyleSheet("background-color: #FF9999;")

    def updateList(self, ports: List):
        ports = [port for port in ports if not "Bluetooth" in port.description()]
        ports = list(map(lambda port: port.portName(), ports))
        if [self.port_combo_box.itemText(i) for i in range(self.port_combo_box.count())] != ports:
            selected_port = self.port_combo_box.currentText()
            ports = [selected_port] + [port for port in ports if port != selected_port]
            ports = [str(port) for port in ports if port != '']
            self.port_combo_box.clear()
            self.port_combo_box.addItems(ports)

