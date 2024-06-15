from PyQt5.QtWidgets import QApplication
class Monitor():
    @staticmethod
    def getDictMonitor() -> dict:
        app = QApplication.instance()  # Получаем экземпляр приложения
        if app is None:
            app = QApplication([])  # Создаем приложение, если его нет

        dict_monitor = {}

        for screen in app.screens():
            dpi = screen.logicalDotsPerInch()
            scale_factor = dpi / 96.0
            dict_monitor[screen.name()] = scale_factor
        return dict_monitor
    # def temp(self, parent):
    #     parent.windowHandle().screenChanged.connect(lambda screen: parent.editSize(screen.name()))
    #
