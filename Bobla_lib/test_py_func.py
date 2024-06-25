import asyncio
import random
import string
import threading
from bleak import BleakClient, BleakScanner
import queue
from PySide6.QtCore import QTimer, Signal, QObject
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget




class MyBlue:
    def __init__(self):
        self.my_queue = queue.Queue()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_queue)
        self.timer.setInterval(1500)
        self.timer.start()

        self.__loop = asyncio.new_event_loop()
        self.__t = threading.Thread(target=self.run_in_thread, args=(self.__loop, self.my_queue,))
        self.__t.daemon = True
        print(self.my_queue.get())
        self.__t.start()

    def check_queue(self):
        try:
            # Проверяем очередь на наличие нового элемента
            print(self.my_queue.get_nowait())

        except queue.Empty:
            print("asd")
            pass


    async def notification_handler(self, sender, data):
            data_str = data.decode("utf-8")  # Convert bytearray to string
            print(f"Notification from {sender}: {data_str}")

    async def find_device_address(self, device_name, queue):
        try:
            devices = await BleakScanner.discover()
        except:
            print("bluet. off")
            return None
        for device in devices:
            if device_name == device.name:
                return device.address
        return None

    async def send_blob_chunk(self,client, characteristic_uuid, chunk):
        try:
            await client.write_gatt_char(characteristic_uuid, chunk, response=True)
            print(f"Chunk sent: {chunk}")
        except Exception as e:
            print(f"Failed to send chunk: {e}")

    async def send_blob(self, client, characteristic_uuid, blob):
        chunk_size = 200
        for i in range(0, len(blob), chunk_size):
            chunk = blob[i:i + chunk_size]
            await self.send_blob_chunk(client, characteristic_uuid, chunk)

    async def send_img(self, client, characteristic_uuid):
        # Отправка мусора что бы сбросить входной буффер
        chunk = "!"
        await client.write_gatt_char("00002ff1-0000-1000-8000-00805f9b34fb", chunk.encode("UTF-8"), response=True)

        characters = string.ascii_letters + string.digits + string.punctuation
        # Рандомная хуйня что бы заплнить экран
        random_string = ''.join(random.choice(characters) for _ in range(352))

        await self.send_blob(client, characteristic_uuid, random_string.encode("UTF-8"))

    async def connect_and_subscribe(self, device_address, characteristic_uuid):
        try:
            async with BleakClient(device_address) as client:
                if client.is_connected:

                    # Уведомления для громкости
                    await client.start_notify(characteristic_uuid, self.notification_handler)
                    # У каждого дисплея уникальный адрес, 00002ff3 - он закодирован в последней цифре, 3 - это второй диспей, 2 - первый и тд
                    await self.send_img(client, "00002ff3-0000-1000-8000-00805f9b34fb")
                    # Тупо нихуя больше не делам
                    while True:
                        await asyncio.sleep(1)
        except Exception as e:
            print(f"Exception: {e}")

    async def main(self, queue):
        DEVICE_NAME = "AudMX"
        CHARACTERISTIC_UUID = "00002ff0-0000-1000-8000-00805f9b34fb"
        device_address = await self.find_device_address(DEVICE_NAME, queue)
        if device_address:
            await self.connect_and_subscribe(device_address, CHARACTERISTIC_UUID)
        else:
            queue.put("error")

    def run_in_thread(self, loop, queue):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.main(queue))



if __name__ == "__main__":
    c = MyBlue()
    while True:
        pass
    # loop = asyncio.new_event_loop()
    # t = threading.Thread(target=run_in_thread, args=(loop,))
    # t.daemon = True
    # t.start()
    # t.join()  # This will wait for the thread to finish if you want to block the main thread until the worker thread is done
