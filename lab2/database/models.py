"""
ORM модели данных для подсистемы ведения адресов клиентов.
Определяет структуру таблиц базы данных с использованием SQLAlchemy.
"""

from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

from .base import Base


class Country(Base):
    """Модель страны."""
    __tablename__ = "country"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    code: Mapped[Optional[str]] = mapped_column(String(2), unique=True, nullable=True)
    
    # Связи
    regions: Mapped[List["Region"]] = relationship(back_populates="country", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"Country(id={self.id}, name='{self.name}', code='{self.code}')"


class Region(Base):
    """Модель региона/области/края."""
    __tablename__ = "region"
    __table_args__ = (
        UniqueConstraint('country_id', 'name', name='uq_region_country_name'),
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("country.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Временное поле для хранения названия страны (используется при отображении)
    _country_name: str = ""
    
    # Связи
    country: Mapped["Country"] = relationship(back_populates="regions")
    cities: Mapped[List["City"]] = relationship(back_populates="region", cascade="all, delete-orphan")
    
    @property
    def country_name(self) -> str:
        """Название страны."""
        return self._country_name or (self.country.name if self.country else "")
    
    def __repr__(self) -> str:
        return f"Region(id={self.id}, name='{self.name}', country_id={self.country_id})"


class City(Base):
    """Модель города."""
    __tablename__ = "city"
    __table_args__ = (
        UniqueConstraint('region_id', 'name', name='uq_city_region_name'),
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey("region.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # Временные поля для хранения названий (используются при отображении)
    _region_name: str = ""
    _country_name: str = ""
    
    # Связи
    region: Mapped["Region"] = relationship(back_populates="cities")
    addresses: Mapped[List["Address"]] = relationship(back_populates="city", cascade="all, delete-orphan")
    
    @property
    def region_name(self) -> str:
        """Название региона."""
        return self._region_name or (self.region.name if self.region else "")
    
    @property
    def country_name(self) -> str:
        """Название страны."""
        if self._country_name:
            return self._country_name
        if self.region and self.region.country:
            return self.region.country.name
        return ""
    
    def __repr__(self) -> str:
        return f"City(id={self.id}, name='{self.name}', postal_code='{self.postal_code}')"


class Address(Base):
    """Модель полного адреса."""
    __tablename__ = "address"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("city.id", ondelete="CASCADE"), nullable=False)
    street: Mapped[str] = mapped_column(String(200), nullable=False)
    house: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    apartment: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    client_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    
    # Временные поля для хранения названий (используются при отображении)
    _city_name: str = ""
    _region_name: str = ""
    _country_name: str = ""
    
    # Связи
    city: Mapped["City"] = relationship(back_populates="addresses")
    
    @property
    def full_address(self) -> str:
        """Возвращает отформатированный полный адрес."""
        parts = []
        
        # Используем кэшированные значения или связи
        if self._country_name:
            parts.append(self._country_name)
        elif self.city and self.city.region and self.city.region.country:
            parts.append(self.city.region.country.name)
            
        if self._region_name:
            parts.append(self._region_name)
        elif self.city and self.city.region:
            parts.append(self.city.region.name)
            
        if self._city_name:
            parts.append(self._city_name)
        elif self.city:
            parts.append(self.city.name)
        
        if self.street:
            parts.append(self.street)
        if self.house:
            parts.append(f"д. {self.house}")
        if self.apartment:
            parts.append(f"кв. {self.apartment}")
        
        return ", ".join(parts)
    
    @property
    def country_name(self) -> str:
        """Название страны."""
        if self._country_name:
            return self._country_name
        if self.city and self.city.region and self.city.region.country:
            return self.city.region.country.name
        return ""
    
    @property
    def region_name(self) -> str:
        """Название региона."""
        if self._region_name:
            return self._region_name
        if self.city and self.city.region:
            return self.city.region.name
        return ""
    
    @property
    def city_name(self) -> str:
        """Название города."""
        if self._city_name:
            return self._city_name
        if self.city:
            return self.city.name
        return ""
    
    def __repr__(self) -> str:
        return f"Address(id={self.id}, client='{self.client_name}', street='{self.street}')"
