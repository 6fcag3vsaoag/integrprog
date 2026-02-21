"""
Менеджер базы данных для подсистемы ведения адресов клиентов.
Обеспечивает подключение к SQLite и операции CRUD.
"""

import sqlite3
from pathlib import Path
from typing import Optional, List
from contextlib import contextmanager

from .models import Country, Region, City, Address, TABLE_SCHEMAS


class DatabaseManager:
    """Управляет подключением к SQLite и операциями с базой данных."""
    
    def __init__(self, db_path: str = None):
        """
        Инициализация менеджера базы данных.
        
        Аргументы:
            db_path: Путь к файлу базы данных SQLite.
                     Если None, используется путь по умолчанию в папке database.
        """
        if db_path is None:
            # Путь по умолчанию: lab2/database/addresses.db
            current_dir = Path(__file__).parent
            db_path = current_dir / "addresses.db"
        
        self.db_path = str(db_path)
        self._connection: Optional[sqlite3.Connection] = None
        self._initialize_database()
    
    @contextmanager
    def get_cursor(self):
        """Контекстный менеджер для курсора базы данных."""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
    
    def _get_connection(self) -> sqlite3.Connection:
        """Получить или создать подключение к базе данных."""
        if self._connection is None:
            self._connection = sqlite3.connect(self.db_path)
            # Включить поддержку внешних ключей
            self._connection.execute("PRAGMA foreign_keys = ON")
            # Возвращать строки как словари
            self._connection.row_factory = sqlite3.Row
        return self._connection
    
    def _initialize_database(self):
        """Создать таблицы, если они не существуют."""
        with self.get_cursor() as cursor:
            for table_name, schema in TABLE_SCHEMAS.items():
                cursor.execute(schema)
    
    def close(self):
        """Закрыть подключение к базе данных."""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    # ==================== CRUD для стран ====================
    
    def get_all_countries(self) -> List[Country]:
        """Получить все страны из базы данных."""
        with self.get_cursor() as cursor:
            cursor.execute("SELECT id, name, code FROM country ORDER BY name")
            return [Country(id=row['id'], name=row['name'], code=row['code']) 
                    for row in cursor.fetchall()]
    
    def get_country_by_id(self, country_id: int) -> Optional[Country]:
        """Получить страну по ID."""
        with self.get_cursor() as cursor:
            cursor.execute("SELECT id, name, code FROM country WHERE id = ?", (country_id,))
            row = cursor.fetchone()
            if row:
                return Country(id=row['id'], name=row['name'], code=row['code'])
            return None
    
    def add_country(self, country: Country) -> int:
        """Добавить новую страну и вернуть её ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO country (name, code) VALUES (?, ?)",
                (country.name, country.code or None)
            )
            return cursor.lastrowid
    
    def update_country(self, country: Country) -> bool:
        """Обновить существующую страну. Возвращает True при успехе."""
        with self.get_cursor() as cursor:
            cursor.execute(
                "UPDATE country SET name = ?, code = ? WHERE id = ?",
                (country.name, country.code or None, country.id)
            )
            return cursor.rowcount > 0
    
    def delete_country(self, country_id: int) -> bool:
        """Удалить страну по ID. Возвращает True при успехе."""
        with self.get_cursor() as cursor:
            cursor.execute("DELETE FROM country WHERE id = ?", (country_id,))
            return cursor.rowcount > 0
    
    def search_countries(self, query: str) -> List[Country]:
        """Поиск стран по названию или коду."""
        with self.get_cursor() as cursor:
            cursor.execute(
                "SELECT id, name, code FROM country WHERE name LIKE ? OR code LIKE ? ORDER BY name",
                (f"%{query}%", f"%{query}%")
            )
            return [Country(id=row['id'], name=row['name'], code=row['code']) 
                    for row in cursor.fetchall()]
    
    # ==================== CRUD для регионов ====================
    
    def get_all_regions(self, country_id: Optional[int] = None) -> List[Region]:
        """Получить все регионы, опционально отфильтрованные по стране."""
        with self.get_cursor() as cursor:
            if country_id:
                cursor.execute(
                    "SELECT id, country_id, name FROM region WHERE country_id = ? ORDER BY name",
                    (country_id,)
                )
            else:
                cursor.execute("SELECT id, country_id, name FROM region ORDER BY name")
            return [Region(id=row['id'], country_id=row['country_id'], name=row['name']) 
                    for row in cursor.fetchall()]
    
    def get_region_by_id(self, region_id: int) -> Optional[Region]:
        """Получить регион по ID."""
        with self.get_cursor() as cursor:
            cursor.execute("SELECT id, country_id, name FROM region WHERE id = ?", (region_id,))
            row = cursor.fetchone()
            if row:
                return Region(id=row['id'], country_id=row['country_id'], name=row['name'])
            return None
    
    def add_region(self, region: Region) -> int:
        """Добавить новый регион и вернуть его ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO region (country_id, name) VALUES (?, ?)",
                (region.country_id, region.name)
            )
            return cursor.lastrowid
    
    def update_region(self, region: Region) -> bool:
        """Обновить существующий регион. Возвращает True при успехе."""
        with self.get_cursor() as cursor:
            cursor.execute(
                "UPDATE region SET country_id = ?, name = ? WHERE id = ?",
                (region.country_id, region.name, region.id)
            )
            return cursor.rowcount > 0
    
    def delete_region(self, region_id: int) -> bool:
        """Удалить регион по ID. Возвращает True при успехе."""
        with self.get_cursor() as cursor:
            cursor.execute("DELETE FROM region WHERE id = ?", (region_id,))
            return cursor.rowcount > 0
    
    def search_regions(self, query: str, country_id: Optional[int] = None) -> List[Region]:
        """Поиск регионов по названию."""
        with self.get_cursor() as cursor:
            if country_id:
                cursor.execute(
                    "SELECT id, country_id, name FROM region WHERE country_id = ? AND name LIKE ? ORDER BY name",
                    (country_id, f"%{query}%")
                )
            else:
                cursor.execute(
                    "SELECT id, country_id, name FROM region WHERE name LIKE ? ORDER BY name",
                    (f"%{query}%",)
                )
            return [Region(id=row['id'], country_id=row['country_id'], name=row['name']) 
                    for row in cursor.fetchall()]
    
    # ==================== CRUD для городов ====================
    
    def get_all_cities(self, region_id: Optional[int] = None) -> List[City]:
        """Получить все города, опционально отфильтрованные по региону."""
        with self.get_cursor() as cursor:
            if region_id:
                cursor.execute(
                    "SELECT id, region_id, name, postal_code FROM city WHERE region_id = ? ORDER BY name",
                    (region_id,)
                )
            else:
                cursor.execute("SELECT id, region_id, name, postal_code FROM city ORDER BY name")
            return [City(id=row['id'], region_id=row['region_id'], 
                         name=row['name'], postal_code=row['postal_code']) 
                    for row in cursor.fetchall()]
    
    def get_city_by_id(self, city_id: int) -> Optional[City]:
        """Получить город по ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                "SELECT id, region_id, name, postal_code FROM city WHERE id = ?", 
                (city_id,)
            )
            row = cursor.fetchone()
            if row:
                return City(id=row['id'], region_id=row['region_id'], 
                           name=row['name'], postal_code=row['postal_code'])
            return None
    
    def add_city(self, city: City) -> int:
        """Добавить новый город и вернуть его ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO city (region_id, name, postal_code) VALUES (?, ?, ?)",
                (city.region_id, city.name, city.postal_code or None)
            )
            return cursor.lastrowid
    
    def update_city(self, city: City) -> bool:
        """Обновить существующий город. Возвращает True при успехе."""
        with self.get_cursor() as cursor:
            cursor.execute(
                "UPDATE city SET region_id = ?, name = ?, postal_code = ? WHERE id = ?",
                (city.region_id, city.name, city.postal_code or None, city.id)
            )
            return cursor.rowcount > 0
    
    def delete_city(self, city_id: int) -> bool:
        """Удалить город по ID. Возвращает True при успехе."""
        with self.get_cursor() as cursor:
            cursor.execute("DELETE FROM city WHERE id = ?", (city_id,))
            return cursor.rowcount > 0
    
    def search_cities(self, query: str, region_id: Optional[int] = None) -> List[City]:
        """Поиск городов по названию или почтовому индексу."""
        with self.get_cursor() as cursor:
            if region_id:
                cursor.execute(
                    """SELECT id, region_id, name, postal_code FROM city 
                       WHERE region_id = ? AND (name LIKE ? OR postal_code LIKE ?) 
                       ORDER BY name""",
                    (region_id, f"%{query}%", f"%{query}%")
                )
            else:
                cursor.execute(
                    """SELECT id, region_id, name, postal_code FROM city 
                       WHERE name LIKE ? OR postal_code LIKE ? ORDER BY name""",
                    (f"%{query}%", f"%{query}%")
                )
            return [City(id=row['id'], region_id=row['region_id'], 
                         name=row['name'], postal_code=row['postal_code']) 
                    for row in cursor.fetchall()]
    
    # ==================== CRUD для адресов ====================
    
    def get_all_addresses(self) -> List[Address]:
        """Получить все адреса с данными о местоположении."""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT a.id, a.city_id, a.street, a.house, a.apartment, a.client_name,
                       c.name as city_name, r.name as region_name, co.name as country_name
                FROM address a
                JOIN city c ON a.city_id = c.id
                JOIN region r ON c.region_id = r.id
                JOIN country co ON r.country_id = co.id
                ORDER BY a.client_name, a.street
            """)
            return [self._row_to_address(row) for row in cursor.fetchall()]
    
    def get_address_by_id(self, address_id: int) -> Optional[Address]:
        """Получить адрес по ID с данными о местоположении."""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT a.id, a.city_id, a.street, a.house, a.apartment, a.client_name,
                       c.name as city_name, r.name as region_name, co.name as country_name
                FROM address a
                JOIN city c ON a.city_id = c.id
                JOIN region r ON c.region_id = r.id
                JOIN country co ON r.country_id = co.id
                WHERE a.id = ?
            """, (address_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_address(row)
            return None
    
    def _row_to_address(self, row) -> Address:
        """Преобразовать строку базы данных в объект Address."""
        return Address(
            id=row['id'],
            city_id=row['city_id'],
            street=row['street'],
            house=row['house'] or "",
            apartment=row['apartment'] or "",
            client_name=row['client_name'] or "",
            city_name=row['city_name'],
            region_name=row['region_name'],
            country_name=row['country_name']
        )
    
    def add_address(self, address: Address) -> int:
        """Добавить новый адрес и вернуть его ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """INSERT INTO address (city_id, street, house, apartment, client_name) 
                   VALUES (?, ?, ?, ?, ?)""",
                (address.city_id, address.street, address.house or None, 
                 address.apartment or None, address.client_name or None)
            )
            return cursor.lastrowid
    
    def update_address(self, address: Address) -> bool:
        """Обновить существующий адрес. Возвращает True при успехе."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """UPDATE address SET city_id = ?, street = ?, house = ?, 
                   apartment = ?, client_name = ? WHERE id = ?""",
                (address.city_id, address.street, address.house or None,
                 address.apartment or None, address.client_name or None, address.id)
            )
            return cursor.rowcount > 0
    
    def delete_address(self, address_id: int) -> bool:
        """Удалить адрес по ID. Возвращает True при успехе."""
        with self.get_cursor() as cursor:
            cursor.execute("DELETE FROM address WHERE id = ?", (address_id,))
            return cursor.rowcount > 0
    
    def search_addresses_by_client(self, client_name: str) -> List[Address]:
        """Поиск адресов по имени клиента."""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT a.id, a.city_id, a.street, a.house, a.apartment, a.client_name,
                       c.name as city_name, r.name as region_name, co.name as country_name
                FROM address a
                JOIN city c ON a.city_id = c.id
                JOIN region r ON c.region_id = r.id
                JOIN country co ON r.country_id = co.id
                WHERE a.client_name LIKE ?
                ORDER BY a.client_name, a.street
            """, (f"%{client_name}%",))
            return [self._row_to_address(row) for row in cursor.fetchall()]
    
    def search_addresses(self, query: str) -> List[Address]:
        """Поиск адресов по имени клиента, улице или городу."""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT a.id, a.city_id, a.street, a.house, a.apartment, a.client_name,
                       c.name as city_name, r.name as region_name, co.name as country_name
                FROM address a
                JOIN city c ON a.city_id = c.id
                JOIN region r ON c.region_id = r.id
                JOIN country co ON r.country_id = co.id
                WHERE a.client_name LIKE ? OR a.street LIKE ? OR c.name LIKE ?
                ORDER BY a.client_name, a.street
            """, (f"%{query}%", f"%{query}%", f"%{query}%"))
            return [self._row_to_address(row) for row in cursor.fetchall()]
    
    # ==================== Вспомогательные методы ====================
    
    def get_location_path(self, city_id: int) -> tuple:
        """
        Получить полный путь местоположения для города.
        Возвращает (название_страны, название_региона, название_города).
        """
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT co.name as country_name, r.name as region_name, c.name as city_name
                FROM city c
                JOIN region r ON c.region_id = r.id
                JOIN country co ON r.country_id = co.id
                WHERE c.id = ?
            """, (city_id,))
            row = cursor.fetchone()
            if row:
                return (row['country_name'], row['region_name'], row['city_name'])
            return (None, None, None)
    
    def get_statistics(self) -> dict:
        """Получить статистику базы данных."""
        with self.get_cursor() as cursor:
            stats = {}
            cursor.execute("SELECT COUNT(*) FROM country")
            stats['countries'] = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM region")
            stats['regions'] = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM city")
            stats['cities'] = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM address")
            stats['addresses'] = cursor.fetchone()[0]
            return stats
