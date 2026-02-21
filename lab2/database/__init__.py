"""
Модуль базы данных для подсистемы ведения адресов клиентов.
Обеспечивает подключение к SQLite через SQLAlchemy ORM и модели данных.
"""

from .base import Base
from .db_manager import DatabaseManager
from .models import Country, Region, City, Address

__all__ = ['Base', 'DatabaseManager', 'Country', 'Region', 'City', 'Address']
