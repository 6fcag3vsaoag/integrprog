"""
Модуль базы данных для подсистемы ведения адресов клиентов.
Обеспечивает подключение к SQLite и модели данных.
"""

from .db_manager import DatabaseManager
from .models import Country, Region, City, Address

__all__ = ['DatabaseManager', 'Country', 'Region', 'City', 'Address']
