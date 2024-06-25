from PySide6.QtWidgets import QPushButton

class CheckButton():
    __is_pressed = 0
    def __init__(self, parent = None, text = ""):
        super().__init__()
        self.__btn = QPushButton(text, parent)
        self.__btn.clicked.connect(self.__click)
        self.__btn.setStyleSheet("background-color: #f3f3f3")
    def __setColor(self):
        if self.__is_pressed == 1:
            self.__btn.setStyleSheet("background-color: #bbbbff")
        else:
            self.__btn.setStyleSheet("background-color: #f3f3f3")
    def __click(self):
        self.__is_pressed = not self.__is_pressed
        self.__setColor()
    @property
    def isPressed(self):
        return self.__is_pressed
    def setChecked(self, state):
        self.__is_pressed = state
        self.__setColor()
    def isChecked(self):
        return self.__is_pressed
    def setFixedSize(self, w: int, h: int):
        self.__btn.setFixedSize(w, h)
    def move(self, ax: int, ay: int):
        self.__btn.move(ax, ay)
    def setFont(self, font):
        self.__btn.setFont(font)
    def setDisabled(self, bool):
        self.__btn.setDisabled(bool)
    @property
    def widget(self):
        return self.__btn
    def setFixedSize(self, w: int, h: int):
        self.__btn.setFixedSize(w, h)
    def setFixedHeight(self, h):
        self.__btn.setFixedHeight(h)
    def setFixedWidth(self, w):
        self.__btn.setFixedWidth(w)

    def height(self):
        return self.__btn.height()

    def width(self):
        return self.__btn.width()
    def pos(self):
        return self.__btn.pos()