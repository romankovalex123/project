import sys
import os

# Добавляем путь к проекту в sys.path
path = '/home/yourusername/mysite'
if path not in sys.path:
    sys.path.append(path)

# Указываем PythonAnywhere где искать файлы
os.chdir(path)

# Импортируем Flask приложение
from app import app as application