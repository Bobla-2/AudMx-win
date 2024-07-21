# AudMix GUI
Приложение для работы с микшером грамкости. Данное приложение запускаеться в трее

## Содержание
- [Использование](#использование)
- [Работа_с_исходным_кодом](#Работа_с_исходным_кодом)

## Использование
Для использования данных програм вам 
## Работа_с_исходным_кодом
Для работы с исходным кодом нужен нужен интерпретатор с библиотеками **PySide6**, **pywin32**, **Pillow**, **ctype**, **pycaw**. 
Для сборки вам потребуется **PyInstaller** и **Python** со всеми установленными библиотеками через **PIP**

 ```pyinstaller -i "C:\Users\savva\Documents\github\AudMx-win\resurce\icon.ico" --hidden-import pycaw  --hidden-import Pillow  --hidden-import ctype  --hidden-import pywin32 --add data=".\module\volume_soket\msvcp140d.dll;." --add-data=".\module\volume_soket\ucrtbased.dll;." --add-data=".\module\volume_soket\vcruntime140_1d.dll;." --add-data=".\module\volume_soket\vcruntime140d.dll;." --add data=".\module\volume_soket\volumepid.exe;." AudMX.py```

## Команда проекта
 - ушла :/
