"""
Менеджер базы данных для подсистемы ведения адресов клиентов.
Обеспечивает подключение к SQLite и операции CRUD с использованием SQLAlchemy.
"""

from pathlib import Path
from typing import Optional, List
from contextlib import contextmanager

from sqlalchemy import create_engine, select, func, or_
from sqlalchemy.orm import Session, sessionmaker, joinedload

from .base import Base
from .models import Country, Region, City, Address


class DatabaseManager:
    """Управляет подключением к SQLite и операциями с базой данных через SQLAlchemy."""
    
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
        
        # Создание движка SQLAlchemy
        self.engine = create_engine(f"sqlite:///{self.db_path}", echo=False)
        
        # Фабрика сессий
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Создание таблиц
        Base.metadata.create_all(self.engine)
    
    @contextmanager
    def get_session(self):
        """Контекстный менеджер для сессии базы данных."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def close(self):
        """Закрыть подключение к базе данных."""
        self.engine.dispose()
    
    # ==================== CRUD для стран ====================
    
    def get_all_countries(self) -> List[Country]:
        """Получить все страны из базы данных."""
        with self.get_session() as session:
            stmt = select(Country).order_by(Country.name)
            # Делаем копии объектов, чтобы они были доступны после закрытия сессии
            countries = []
            for c in session.scalars(stmt).all():
                countries.append(Country(id=c.id, name=c.name, code=c.code))
            return countries
    
    def get_country_by_id(self, country_id: int) -> Optional[Country]:
        """Получить страну по ID."""
        with self.get_session() as session:
            c = session.get(Country, country_id)
            if c:
                return Country(id=c.id, name=c.name, code=c.code)
            return None
    
    def add_country(self, country: Country) -> int:
        """Добавить новую страну и вернуть её ID."""
        with self.get_session() as session:
            new_country = Country(name=country.name, code=country.code)
            session.add(new_country)
            session.flush()  # Получаем ID до коммита
            return new_country.id
    
    def update_country(self, country: Country) -> bool:
        """Обновить существующую страну. Возвращает True при успехе."""
        with self.get_session() as session:
            existing = session.get(Country, country.id)
            if existing:
                existing.name = country.name
                existing.code = country.code
                return True
            return False
    
    def delete_country(self, country_id: int) -> bool:
        """Удалить страну по ID. Возвращает True при успехе."""
        with self.get_session() as session:
            country = session.get(Country, country_id)
            if country:
                session.delete(country)
                return True
            return False
    
    def search_countries(self, query: str) -> List[Country]:
        """Поиск стран по названию или коду."""
        with self.get_session() as session:
            stmt = select(Country).where(
                or_(
                    Country.name.ilike(f"%{query}%"),
                    Country.code.ilike(f"%{query}%")
                )
            ).order_by(Country.name)
            countries = []
            for c in session.scalars(stmt).all():
                countries.append(Country(id=c.id, name=c.name, code=c.code))
            return countries
    
    # ==================== CRUD для регионов ====================
    
    def get_all_regions(self, country_id: Optional[int] = None) -> List[Region]:
        """Получить все регионы, опционально отфильтрованные по стране."""
        with self.get_session() as session:
            if country_id:
                stmt = select(Region).where(Region.country_id == country_id).order_by(Region.name)
            else:
                stmt = select(Region).options(joinedload(Region.country)).order_by(Region.name)
            regions = []
            for r in session.scalars(stmt).all():
                region = Region(id=r.id, country_id=r.country_id, name=r.name)
                # Сохраняем название страны для отображения
                if r.country:
                    region._country_name = r.country.name
                regions.append(region)
            return regions
    
    def get_region_by_id(self, region_id: int) -> Optional[Region]:
        """Получить регион по ID."""
        with self.get_session() as session:
            r = session.get(Region, region_id)
            if r:
                region = Region(id=r.id, country_id=r.country_id, name=r.name)
                if r.country:
                    region._country_name = r.country.name
                return region
            return None
    
    def add_region(self, region: Region) -> int:
        """Добавить новый регион и вернуть его ID."""
        with self.get_session() as session:
            new_region = Region(country_id=region.country_id, name=region.name)
            session.add(new_region)
            session.flush()
            return new_region.id
    
    def update_region(self, region: Region) -> bool:
        """Обновить существующий регион. Возвращает True при успехе."""
        with self.get_session() as session:
            existing = session.get(Region, region.id)
            if existing:
                existing.country_id = region.country_id
                existing.name = region.name
                return True
            return False
    
    def delete_region(self, region_id: int) -> bool:
        """Удалить регион по ID. Возвращает True при успехе."""
        with self.get_session() as session:
            region = session.get(Region, region_id)
            if region:
                session.delete(region)
                return True
            return False
    
    def search_regions(self, query: str, country_id: Optional[int] = None) -> List[Region]:
        """Поиск регионов по названию."""
        with self.get_session() as session:
            conditions = [Region.name.ilike(f"%{query}%")]
            if country_id:
                conditions.append(Region.country_id == country_id)
            stmt = select(Region).where(*conditions).order_by(Region.name)
            regions = []
            for r in session.scalars(stmt).all():
                region = Region(id=r.id, country_id=r.country_id, name=r.name)
                if r.country:
                    region._country_name = r.country.name
                regions.append(region)
            return regions
    
    # ==================== CRUD для городов ====================
    
    def get_all_cities(self, region_id: Optional[int] = None) -> List[City]:
        """Получить все города, опционально отфильтрованные по региону."""
        with self.get_session() as session:
            if region_id:
                stmt = select(City).where(City.region_id == region_id).order_by(City.name)
            else:
                stmt = select(City).options(
                    joinedload(City.region).joinedload(Region.country)
                ).order_by(City.name)
            cities = []
            for c in session.scalars(stmt).all():
                city = City(id=c.id, region_id=c.region_id, name=c.name, postal_code=c.postal_code)
                if c.region:
                    city._region_name = c.region.name
                    if c.region.country:
                        city._country_name = c.region.country.name
                cities.append(city)
            return cities
    
    def get_city_by_id(self, city_id: int) -> Optional[City]:
        """Получить город по ID."""
        with self.get_session() as session:
            c = session.get(City, city_id)
            if c:
                city = City(id=c.id, region_id=c.region_id, name=c.name, postal_code=c.postal_code)
                if c.region:
                    city._region_name = c.region.name
                    if c.region.country:
                        city._country_name = c.region.country.name
                return city
            return None
    
    def add_city(self, city: City) -> int:
        """Добавить новый город и вернуть его ID."""
        with self.get_session() as session:
            new_city = City(region_id=city.region_id, name=city.name, postal_code=city.postal_code)
            session.add(new_city)
            session.flush()
            return new_city.id
    
    def update_city(self, city: City) -> bool:
        """Обновить существующий город. Возвращает True при успехе."""
        with self.get_session() as session:
            existing = session.get(City, city.id)
            if existing:
                existing.region_id = city.region_id
                existing.name = city.name
                existing.postal_code = city.postal_code
                return True
            return False
    
    def delete_city(self, city_id: int) -> bool:
        """Удалить город по ID. Возвращает True при успехе."""
        with self.get_session() as session:
            city = session.get(City, city_id)
            if city:
                session.delete(city)
                return True
            return False
    
    def search_cities(self, query: str, region_id: Optional[int] = None) -> List[City]:
        """Поиск городов по названию или почтовому индексу."""
        with self.get_session() as session:
            conditions = [
                or_(
                    City.name.ilike(f"%{query}%"),
                    City.postal_code.ilike(f"%{query}%")
                )
            ]
            if region_id:
                conditions.append(City.region_id == region_id)
            stmt = select(City).options(
                joinedload(City.region).joinedload(Region.country)
            ).where(*conditions).order_by(City.name)
            cities = []
            for c in session.scalars(stmt).all():
                city = City(id=c.id, region_id=c.region_id, name=c.name, postal_code=c.postal_code)
                if c.region:
                    city._region_name = c.region.name
                    if c.region.country:
                        city._country_name = c.region.country.name
                cities.append(city)
            return cities
    
    # ==================== CRUD для адресов ====================
    
    def get_all_addresses(self) -> List[Address]:
        """Получить все адреса с данными о местоположении."""
        with self.get_session() as session:
            stmt = select(Address).options(
                joinedload(Address.city).joinedload(City.region).joinedload(Region.country)
            ).order_by(Address.client_name, Address.street)
            addresses = []
            for a in session.scalars(stmt).all():
                address = Address(
                    id=a.id, city_id=a.city_id, street=a.street,
                    house=a.house, apartment=a.apartment, client_name=a.client_name
                )
                if a.city:
                    address._city_name = a.city.name
                    if a.city.region:
                        address._region_name = a.city.region.name
                        if a.city.region.country:
                            address._country_name = a.city.region.country.name
                addresses.append(address)
            return addresses
    
    def get_address_by_id(self, address_id: int) -> Optional[Address]:
        """Получить адрес по ID с данными о местоположении."""
        with self.get_session() as session:
            a = session.get(Address, address_id, options=[
                joinedload(Address.city).joinedload(City.region).joinedload(Region.country)
            ])
            if a:
                address = Address(
                    id=a.id, city_id=a.city_id, street=a.street,
                    house=a.house, apartment=a.apartment, client_name=a.client_name
                )
                if a.city:
                    address._city_name = a.city.name
                    if a.city.region:
                        address._region_name = a.city.region.name
                        if a.city.region.country:
                            address._country_name = a.city.region.country.name
                return address
            return None
    
    def add_address(self, address: Address) -> int:
        """Добавить новый адрес и вернуть его ID."""
        with self.get_session() as session:
            new_address = Address(
                city_id=address.city_id, street=address.street,
                house=address.house, apartment=address.apartment, client_name=address.client_name
            )
            session.add(new_address)
            session.flush()
            return new_address.id
    
    def update_address(self, address: Address) -> bool:
        """Обновить существующий адрес. Возвращает True при успехе."""
        with self.get_session() as session:
            existing = session.get(Address, address.id)
            if existing:
                existing.city_id = address.city_id
                existing.street = address.street
                existing.house = address.house
                existing.apartment = address.apartment
                existing.client_name = address.client_name
                return True
            return False
    
    def delete_address(self, address_id: int) -> bool:
        """Удалить адрес по ID. Возвращает True при успехе."""
        with self.get_session() as session:
            address = session.get(Address, address_id)
            if address:
                session.delete(address)
                return True
            return False
    
    def search_addresses_by_client(self, client_name: str) -> List[Address]:
        """Поиск адресов по имени клиента."""
        with self.get_session() as session:
            stmt = select(Address).options(
                joinedload(Address.city).joinedload(City.region).joinedload(Region.country)
            ).where(
                Address.client_name.ilike(f"%{client_name}%")
            ).order_by(Address.client_name, Address.street)
            addresses = []
            for a in session.scalars(stmt).all():
                address = Address(
                    id=a.id, city_id=a.city_id, street=a.street,
                    house=a.house, apartment=a.apartment, client_name=a.client_name
                )
                if a.city:
                    address._city_name = a.city.name
                    if a.city.region:
                        address._region_name = a.city.region.name
                        if a.city.region.country:
                            address._country_name = a.city.region.country.name
                addresses.append(address)
            return addresses
    
    def search_addresses(self, query: str) -> List[Address]:
        """Поиск адресов по имени клиента, улице или городу."""
        with self.get_session() as session:
            # Используем join для поиска по названию города
            stmt = select(Address).join(City).options(
                joinedload(Address.city).joinedload(City.region).joinedload(Region.country)
            ).where(
                or_(
                    Address.client_name.ilike(f"%{query}%"),
                    Address.street.ilike(f"%{query}%"),
                    City.name.ilike(f"%{query}%")
                )
            ).order_by(Address.client_name, Address.street)
            addresses = []
            for a in session.scalars(stmt).all():
                address = Address(
                    id=a.id, city_id=a.city_id, street=a.street,
                    house=a.house, apartment=a.apartment, client_name=a.client_name
                )
                if a.city:
                    address._city_name = a.city.name
                    if a.city.region:
                        address._region_name = a.city.region.name
                        if a.city.region.country:
                            address._country_name = a.city.region.country.name
                addresses.append(address)
            return addresses
    
    # ==================== Вспомогательные методы ====================
    
    def get_location_path(self, city_id: int) -> tuple:
        """
        Получить полный путь местоположения для города.
        Возвращает (название_страны, название_региона, название_города).
        """
        with self.get_session() as session:
            city = session.get(City, city_id, options=[
                joinedload(City.region).joinedload(Region.country)
            ])
            if city and city.region and city.region.country:
                return (city.region.country.name, city.region.name, city.name)
            return (None, None, None)
    
    def get_statistics(self) -> dict:
        """Получить статистику базы данных."""
        with self.get_session() as session:
            stats = {
                'countries': session.scalar(select(func.count()).select_from(Country)),
                'regions': session.scalar(select(func.count()).select_from(Region)),
                'cities': session.scalar(select(func.count()).select_from(City)),
                'addresses': session.scalar(select(func.count()).select_from(Address))
            }
            return stats
