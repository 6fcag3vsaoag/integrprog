"""
Модуль интерфейса для подсистемы ведения адресов клиентов.
Содержит виджеты и окна PyQt6.
"""

from .main_window import MainWindow
from .pages import CountryPage, RegionPage, CityPage, AddressPage

__all__ = ['MainWindow', 'CountryPage', 'RegionPage', 'CityPage', 'AddressPage']
