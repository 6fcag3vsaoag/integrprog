"""
Модуль страниц для подсистемы ведения адресов клиентов.
Содержит отдельные виджеты страниц для каждой таблицы базы данных.
"""

from .country_page import CountryPage
from .region_page import RegionPage
from .city_page import CityPage
from .address_page import AddressPage

__all__ = ['CountryPage', 'RegionPage', 'CityPage', 'AddressPage']
