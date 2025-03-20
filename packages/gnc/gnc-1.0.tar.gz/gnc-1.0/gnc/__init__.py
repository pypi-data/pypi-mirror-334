import os
# import sys
import ctypes

# Отримуємо шлях до поточної папки
# _package_dir = os.path.dirname(os.path.abspath(__file__))
_dll_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "opencv_world4100.dll")

# Завантажуємо DLL, якщо вона існує
if os.path.exists(_dll_path):
    ctypes.windll.kernel32.LoadLibraryW(_dll_path)