"""
Модели данных для подсистемы ведения адресов клиентов.
Определяет структуру таблиц базы данных.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Country:
    """Модель страны."""
    id: Optional[int] = None
    name: str = ""
    code: str = ""  # ISO код страны (например, "BY", "RU")
    
    def __post_init__(self):
        """Валидация данных после инициализации."""
        if self.name:
            self.name = self.name.strip()
        if self.code:
            self.code = self.code.strip().upper()


@dataclass
class Region:
    """Модель региона/области/края."""
    id: Optional[int] = None
    country_id: Optional[int] = None
    name: str = ""
    
    def __post_init__(self):
        """Валидация данных после инициализации."""
        if self.name:
            self.name = self.name.strip()


@dataclass
class City:
    """Модель города."""
    id: Optional[int] = None
    region_id: Optional[int] = None
    name: str = ""
    postal_code: str = ""
    
    def __post_init__(self):
        """Валидация данных после инициализации."""
        if self.name:
            self.name = self.name.strip()
        if self.postal_code:
            self.postal_code = self.postal_code.strip()


@dataclass
class Address:
    """Модель полного адреса."""
    id: Optional[int] = None
    city_id: Optional[int] = None
    street: str = ""
    house: str = ""
    apartment: str = ""
    client_name: str = ""
    
    # Дополнительные поля для отображения (из связанных таблиц)
    city_name: str = ""
    region_name: str = ""
    country_name: str = ""
    
    def __post_init__(self):
        """Валидация данных после инициализации."""
        if self.street:
            self.street = self.street.strip()
        if self.house:
            self.house = self.house.strip()
        if self.apartment:
            self.apartment = self.apartment.strip()
        if self.client_name:
            self.client_name = self.client_name.strip()
    
    @property
    def full_address(self) -> str:
        """Возвращает отформатированный полный адрес."""
        parts = []
        if self.country_name:
            parts.append(self.country_name)
        if self.region_name:
            parts.append(self.region_name)
        if self.city_name:
            parts.append(self.city_name)
        if self.street:
            parts.append(self.street)
        if self.house:
            parts.append(f"д. {self.house}")
        if self.apartment:
            parts.append(f"кв. {self.apartment}")
        return ", ".join(parts)


# Схемы таблиц для создания базы данных
TABLE_SCHEMAS = {
    'country': '''
        CREATE TABLE IF NOT EXISTS country (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            code TEXT(2) UNIQUE
        )
    ''',
    'region': '''
        CREATE TABLE IF NOT EXISTS region (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (country_id) REFERENCES country(id) ON DELETE CASCADE,
            UNIQUE(country_id, name)
        )
    ''',
    'city': '''
        CREATE TABLE IF NOT EXISTS city (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            postal_code TEXT,
            FOREIGN KEY (region_id) REFERENCES region(id) ON DELETE CASCADE,
            UNIQUE(region_id, name)
        )
    ''',
    'address': '''
        CREATE TABLE IF NOT EXISTS address (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER NOT NULL,
            street TEXT NOT NULL,
            house TEXT,
            apartment TEXT,
            client_name TEXT,
            FOREIGN KEY (city_id) REFERENCES city(id) ON DELETE CASCADE
        )
    '''
}
