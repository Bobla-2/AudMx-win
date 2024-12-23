# import base64
# from module.logger.logger import SimpleLogger
from cryptography.fernet import Fernet
import vk_api
from vk_api.utils import get_random_id
from .config import *
import os
from os import walk


    # break
# Собираем зашифрованный токен
ENCRYPTED_TOKEN = PART1 + PART2 + PART3 + PART4 + PART5 + PART6

def decrypt_token():
    """Расшифровывает токен."""
    try:
        cipher = Fernet(STATIC_KEY_PART)
        token = cipher.decrypt(ENCRYPTED_TOKEN).decode()
        return token
    except Exception as e:
        print(f"Ошибка при расшифровке токена: {e}")
        return None

def send_log(log_message):
    """Отправляет лог в ВКонтакте в виде текста."""
    token = decrypt_token()

    if not token:
        print("Не удалось расшифровать токен. Отправка отменена.")
        return

    try:
        vk_session = vk_api.VkApi(token=token)
        vk = vk_session.get_api()

        vk.messages.send(
            user_id=VK_USER_ID,
            message=log_message,
            random_id=get_random_id()
        )
        print("Лог успешно отправлен!")
    except Exception as e:
        print(f"Ошибка при отправке лога: {e}")

def send_log_file(file_path: list, name="") -> bool:
    """Отправляет лог в виде файла."""
    token = decrypt_token()
    if not token:
        print("Не удалось расшифровать токен. Отправка отменена.")
        return False

    try:
        vk_session = vk_api.VkApi(token=token)
        upload = vk_api.VkUpload(vk_session)
        vk = vk_session.get_api()
        docs = []
        for path in file_path:
            # Загружаем файл
            docs.append(upload.document_message(doc=path, peer_id=VK_USER_ID, title=path.split('\\')[-1]))

        vk.messages.send(
            user_id=VK_USER_ID,
            random_id=get_random_id(),
            message=f"Отправляю лог-файл: {name}",
            # title="log.txt",
            attachment=",".join((f'doc{doc["doc"]["owner_id"]}_{doc["doc"]["id"]}' for doc in docs))
        )

        print("Файл с логом успешно отправлен!")
        return True
    except Exception as e:
        print(f"Ошибка при отправке файла: {e}")
        return False

# --- Основной код ---

if __name__ == "__main__":
    # logger = SimpleLogger()

    # x = 1/0
    # Пример текста лога
    # error_log = """
    # [ERROR] Приложение упало с исключением:
    # Traceback (most recent call last):
    #   File "main.py", line 42, in <module>
    #     1 / 0
    # ZeroDivisionError: division by zero
    # """
    send_log("хуй")
    for (dirpath, dirnames, filenames) in walk("logs_backup"):
        print(dirpath, dirnames, filenames)
        backup_file = os.path.join("logs_backup", filenames[0])
        send_log_file(backup_file, name=filenames[0])

    # Пример отправки файла (укажите путь к файлу с логами)
    # send_log_file("path_to_log_file.txt")
