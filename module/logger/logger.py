# import gc
import shutil
from datetime import datetime
import sys
import traceback
# from module.UI_manager.monitor_func import Monitor
from module.vk_log_bot.bot import *
from PySide6 import QtWidgets
from module.UI_manager.theme.windows_thames import AutoUpdateStile
from PySide6.QtCore import QCoreApplication
import platform

APPLICATION_NAME = 'AudMX v1.5'
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


@singleton
class SimpleLogger:
    def __init__(self, log_dir="logs", backup_dir="logs_backup", end_log_marker="END_LOG"):
        self.log_dir = log_dir
        self.backup_dir = backup_dir
        self.end_log_marker = end_log_marker
        self.log_file = os.path.join(log_dir, "current_log.txt")
        sys.excepthook = self._log_uncaught_exceptions
        print("Current working directory:", os.getcwd())
        # Создаем директории, если они не существуют
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

        # Проверяем последний лог
        self._check_last_log()

    def _log_uncaught_exceptions(self, exc_type, exc_value, exc_traceback):
        """Логгирует необработанные исключения."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backup_dir, f"crash_{timestamp}.txt")
        with open(backup_file, "w") as crash_file:
            crash_file.write("Необработанная ошибка:\n")
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=crash_file)
        print("Приложение завершилось с необработанной ошибкой. Лог сохранен в 'crash.log'.")

    def _check_last_log(self):

        # Проверяем наличие текущего лога
        if os.path.exists(self.log_file):
            last_line = None
            with open(self.log_file, "r") as file:
                lines = file.readlines()
                if lines:
                    last_line = lines[-1].strip() if file else ""

            # Если последний лог не завершён, сохраняем его в архив
            if last_line and last_line.split()[-1] != self.end_log_marker:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = os.path.join(self.backup_dir, f"log_backup_{timestamp}.txt")
                shutil.move(self.log_file, backup_file)
        with open(self.log_file, "w") as file:
            file.write("")
        if list(walk("logs_backup"))[0][2]:
            self.asd = CrashMenu()
            self.asd.setLinkOnWindows(self.asd)

    def log(self, message):
        # Записываем сообщение в лог
        with open(self.log_file, "a") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp} - {message}\n")
            print(message)

    def end_log(self):
        # Записываем маркер завершения
        self.log(self.end_log_marker)


class CrashMenu():
    def __init__(self, text="Предыдйщий запуск приложения завершился с "
                            "\nнеобработанной ошибкой.\n Отправить ошибку разработчикам?") -> None:
        self.__msgBox = QtWidgets.QDialog()
        self.__msgBox.setWindowTitle("")
        self.__layout = QtWidgets.QGridLayout()
        self.__level_lb = QtWidgets.QLabel(text)
        self.__level_lb.setFixedSize(300, 100)
        self.__button_ok = QtWidgets.QPushButton("ОК")
        self.__button_cancel = QtWidgets.QPushButton("Cancel")
        self.__layout.addWidget(self.__level_lb, 1, 0, 1, 2)
        self.__layout.addWidget(self.__button_ok, 3, 0, 1, 1)
        self.__layout.addWidget(self.__button_cancel, 3, 1, 1, 1)
        self.__button_ok.clicked.connect(self.__send_log)
        self.__button_ok.setFixedSize(100, 50)
        self.__button_cancel.clicked.connect(self.__close)
        self.__button_cancel.setFixedSize(100, 50)
        self.__msgBox.setLayout(self.__layout)
        self.__msgBox.show()
        self.auto_udate_theme = AutoUpdateStile()
        self.auto_udate_theme.appendedCallback(self.__msgBox.setStyleSheet, ":/qss/W_sylete", ":/qss/B_sylete",
                                               "CSS")
        self.__link = None
        # self.timp = Monitor()
        # self.timp.appendWindow(self.__msgBox, self.items)
        # self.__msgBox.show()

    def setLinkOnWindows(self, link):
        self.__link = link

    def __close(self):
        self.auto_udate_theme.removeCallback(self.__msgBox.setStyleSheet)
        self.__msgBox.close()
        for i in reversed(range(self.__layout.count())):
            widget = self.__layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.__msgBox.deleteLater()
        if self.__link:
            del self.__link
        # print(gc.get_referrers(self))
        del self
        print("-----")


    def __send_log(self):
        self.__level_lb.setText("Отправка. \nЭто может занять некоторое время")
        QCoreApplication.processEvents()
        dirpath = list(walk("logs_backup"))
        backup_files = [os.path.join(dirpath[0][0], dir) for dir in dirpath[0][2]]
        if send_log_file(backup_files, name=f"{APPLICATION_NAME}--{platform.platform()}"
                                            f"--{platform.node()}"):
            for file in backup_files:
                os.remove(file)
            self.__close()
        else:
            self.__level_lb.setText("Не удалось отправить!!!")
            self.__button_ok.setText("Повторить")


    # @property
    # def items(self):
    #     return [self.__button, self.__level_lb]


