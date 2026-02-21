#!/usr/bin/env python3
"""
Точка входа для подсистемы ведения адресов клиентов.

Это приложение предоставляет графический интерфейс для управления адресами клиентов
со следующими функциями:
- Просмотр, добавление, редактирование и удаление стран, регионов, городов и адресов
- Поиск адресов по имени клиента
- База данных SQLite для портативного хранения данных

Запуск:
    uv run python lab2/main.py
"""

import sys
from pathlib import Path

# Добавление корня проекта в путь для импорта
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from ui.main_window import MainWindow


def main():
    """Точка входа приложения."""
    # Включение масштабирования для высокого DPI
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("Address Management System")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("IntegrProg")
    
    # Создание и отображение главного окна
    window = MainWindow()
    window.show()
    
    # Запуск цикла событий
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
