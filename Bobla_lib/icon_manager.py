
import os
from PIL import Image
from module.volume_soket.volume_socket import SocketVolume
import sys
from PySide6.QtCore import QTimer
class IconCl(object):
    """
    This class represents an icon object for AdMX. the object contains all the properties of the icon.
    """

    __icon = []
    __num = -1
    __state = -1
    __name = ''
    __path = ''
    __volume_level = 0
    __last_volume_level = 0
    __socket = None
    __pid = -1

    def __init__(self, path: str, num = -1):
        self.__path = path
        self.__num = num
        if path != None:
            self.__name = path[path.rindex("__")+2:-3] + "exe"
    @property
    def icon(self):
        """
        property icon is icon
        :return: bytes array icon
        """
        if (self.__icon == []):
            if self.__path == None:
                self.__icon = bytes([0]) * 352
            else:
                self.__icon = self.__bmp_to_byte_array(self.__path)
        return self.__icon
    def __bmp_to_byte_array(self, image_path: str) -> bytes:
        """
        #преобразование картинок в байт массив
        :param image_path: - путь к иконками
        :return: байт массив
        """
        img = Image.open(image_path)
        if img.mode != '1':
            print(image_path)
            self.__path = ""
            self.__name = ""
            return bytes([0]) * 352

            # raise ValueError("Изображение не является монохромным")
        img_bytes = img.tobytes()
        return img_bytes
    @property
    def num(self):
        return self.__num

    @property
    def pid(self):
        return self.__pid
    @property
    def state(self):
        return self.__state
    @property
    def name(self):
        return self.__name
    @property
    def volume_level(self):
        return self.__volume_level
    @volume_level.setter
    def volume_level(self, level):
        self.__volume_level = level

    @property
    def last_volume_level(self):
        return self.__last_volume_level

    @last_volume_level.setter
    def last_volume_level(self, level):
        self.__last_volume_level = level

    @pid.setter
    def pid(self, vl):
        self.__pid = vl





class IcomReader():
    """
    This class represents an array icons object.  To create
    :py:class:`~IcomReader.loadIcons` objects, use the appropriate factory
    functions.

    * :py:func:`~IcomReader.setLastLevel`
    """
    # __icon_mass = []

    @staticmethod
    def loadIcons( path: str, open_poccess_list: list, len_: int, irq_massege = None) -> list[IconCl]:
        __icon_mass = IcomReader.__processFolder(path, open_poccess_list, irq_massege)
        while (len(__icon_mass) < len_):
            __icon_mass.append(IconCl(None, len(__icon_mass)))

        return __icon_mass
    @staticmethod
    def __processFolder(folder_path: str, poccess_list: list, irq_massege) -> list[bytes]:
        """
        #читает иконки из папки и прогоняет их через преобразование
        :param folder_path: - относительный путь к папку и иконками
        :return: массив байтовых строк
        """

        name_list_open = [item[0] for item in poccess_list]
        icon_mass = []

        for filename in os.listdir(folder_path):

            if filename.endswith(".bmp"):
                if (len(icon_mass) > 4):
                    return icon_mass

                file_path = os.path.join(folder_path, filename)
                tmp = IconCl(file_path, len(icon_mass))
                for it in poccess_list:
                    if tmp.name == it[0]:
                        tmp.pid = it[1]

                if tmp.name in name_list_open:
                    if (len(tmp.icon) == 352):
                        icon_mass.append(tmp)
                else:
                    if irq_massege != None:
                        irq_massege(tmp.name)
                    # self.trayIcon.masegeIconWarning(str(filename[8:-4]))
        return icon_mass
    @staticmethod
    def setLastLevel(mas: list[IconCl], level: int):
        for ms in mas:
            ms.last_volume_level = level


class VaveLight():
    __old_pid = []
    __mas_vol_socket = []
    __serW = None
    def __init__(self, mas_icon: list[IconCl], serWrite):
        self.__serW = serWrite
        self.timer = QTimer()
        self.timer.timeout.connect(self.__sendCom)
        self.timer.setInterval(33)
        for icon in mas_icon:
            if icon.pid != -1:
                self.__mas_vol_socket.append([icon.num, SocketVolume(icon.pid), 0.])
            else:
                self.__mas_vol_socket.append([icon.num, 0., -1])
            self.__old_pid.append(icon.pid)

    @property
    def volume(self):
        return [float(it[1]) for it in self.__mas_vol_socket]

    def __sendCom(self):

        com = ""
        for it in self.volume:
            com += str(it*3) + "|"
        print(self.__mas_vol_socket)


        self.__serW("VOL:"+ com[:-1] + "\n\r")
    def avtoUpdateStop(self):
        self.timer.stop()
        self.timer.blockSignals(True)
    def avtoUpdateStart(self):
        self.timer.start()
        self.timer.blockSignals(False)

    def updateList(self,  mas_icon: list[IconCl]):
        new_pid = [icon.pid for icon in mas_icon]
        if len(new_pid) == len(self.__old_pid):
            for i in range(len(self.__old_pid)):
                if self.__old_pid[i] != new_pid[i]:
                    del self.__mas_vol_socket[i]
                    self.__mas_vol_socket.insert(i, [i, SocketVolume(mas_icon[i].pid), 0.])
                    # return
        # elif len(new_pid) == len(self.__old_pid) - 1:
        #     for i in range(len(self.__old_pid)):
        #         if self.__old_pid[i] != new_pid[i]:
        #             self.__mas_vol_socket[i].stop()
        #             self.__mas_vol_socket.pop(i)
        #             return
    def stop(self):

        for vl in self.__mas_vol_socket:
            if vl[2] != -1:
                print(vl)
                vl[1].stop()
        self.__mas_vol_socket.clear()

