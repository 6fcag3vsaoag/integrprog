"""
Страница управления адресами клиентов.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QLabel, QPushButton, QTableWidgetItem,
    QComboBox
)
from PyQt6.QtCore import Qt
from typing import List

from .base_page import BasePage
from database.models import Address


class AddressDialog(QDialog):
    """Диалог для добавления/редактирования адреса."""
    
    def __init__(self, db_manager, address: Address = None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.address = address or Address()
        self._setup_ui()
        
        # Загрузка городов в выпадающий список
        self._load_cities()
        
        if address:
            self.client_input.setText(address.client_name or "")
            self.street_input.setText(address.street)
            self.house_input.setText(address.house or "")
            self.apartment_input.setText(address.apartment or "")
            self.setWindowTitle("Редактирование адреса")
            # Выбор города
            if address.city_id:
                for i in range(self.city_combo.count()):
                    if self.city_combo.itemData(i) == address.city_id:
                        self.city_combo.setCurrentIndex(i)
                        break
        else:
            self.setWindowTitle("Добавление адреса")
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Имя клиента
        client_layout = QHBoxLayout()
        client_layout.addWidget(QLabel("Клиент:"))
        self.client_input = QLineEdit()
        self.client_input.setPlaceholderText("Имя клиента")
        client_layout.addWidget(self.client_input)
        layout.addLayout(client_layout)
        
        # Выбор города
        city_layout = QHBoxLayout()
        city_layout.addWidget(QLabel("Город:"))
        self.city_combo = QComboBox()
        self.city_combo.setPlaceholderText("Выберите город")
        city_layout.addWidget(self.city_combo)
        layout.addLayout(city_layout)
        
        # Улица
        street_layout = QHBoxLayout()
        street_layout.addWidget(QLabel("Улица:"))
        self.street_input = QLineEdit()
        self.street_input.setPlaceholderText("Название улицы")
        street_layout.addWidget(self.street_input)
        layout.addLayout(street_layout)
        
        # Дом и квартира в одной строке
        house_layout = QHBoxLayout()
        house_layout.addWidget(QLabel("Дом:"))
        self.house_input = QLineEdit()
        self.house_input.setPlaceholderText("Номер дома")
        self.house_input.setMaximumWidth(100)
        house_layout.addWidget(self.house_input)
        
        house_layout.addWidget(QLabel("Кв.:"))
        self.apartment_input = QLineEdit()
        self.apartment_input.setPlaceholderText("Номер квартиры")
        self.apartment_input.setMaximumWidth(100)
        house_layout.addWidget(self.apartment_input)
        house_layout.addStretch()
        layout.addLayout(house_layout)
        
        # Кнопки
        button_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
    
    def _load_cities(self):
        """Загрузка городов в выпадающий список."""
        cities = self.db_manager.get_all_cities()
        self.city_combo.clear()
        for city in cities:
            self.city_combo.addItem(
                f"{city.name} ({city.region_name}, {city.country_name})",
                city.id
            )
    
    def get_address(self) -> Address:
        """Возвращает адрес с данными из диалога."""
        city_id = self.city_combo.currentData()
        return Address(
            id=self.address.id,
            city_id=city_id,
            street=self.street_input.text().strip(),
            house=self.house_input.text().strip() or None,
            apartment=self.apartment_input.text().strip() or None,
            client_name=self.client_input.text().strip() or None
        )


class AddressPage(BasePage):
    """Страница управления адресами."""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(db_manager, "Управление адресами клиентов", parent)
        self._setup_table()
        self.refresh_data()
    
    def _setup_table(self):
        """Настройка столбцов таблицы."""
        headers = ["ID", "Клиент", "Страна", "Регион", "Город", "Улица", "Дом", "Кв."]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setColumnHidden(0, True)  # Скрыть столбец ID
    
    def _get_table_columns(self) -> List[str]:
        return ["ID", "Клиент", "Страна", "Регион", "Город", "Улица", "Дом", "Кв."]
    
    def _load_data(self) -> List[Address]:
        return self.db_manager.get_all_addresses()
    
    def _display_data(self, data: List[Address]):
        """Отображение адресов в таблице."""
        self.table.setRowCount(len(data))
        for row, address in enumerate(data):
            # ID (скрыт, хранится как пользовательские данные)
            id_item = QTableWidgetItem(str(address.id))
            id_item.setData(Qt.ItemDataRole.UserRole, address.id)
            self.table.setItem(row, 0, id_item)
            
            # Имя клиента
            client_item = QTableWidgetItem(address.client_name or "")
            self.table.setItem(row, 1, client_item)
            
            # Данные о местоположении (используем properties)
            country_item = QTableWidgetItem(address.country_name)
            self.table.setItem(row, 2, country_item)
            
            region_item = QTableWidgetItem(address.region_name)
            self.table.setItem(row, 3, region_item)
            
            city_item = QTableWidgetItem(address.city_name)
            self.table.setItem(row, 4, city_item)
            
            # Улица
            street_item = QTableWidgetItem(address.street)
            self.table.setItem(row, 5, street_item)
            
            # Дом
            house_item = QTableWidgetItem(address.house or "")
            self.table.setItem(row, 6, house_item)
            
            # Квартира
            apartment_item = QTableWidgetItem(address.apartment or "")
            self.table.setItem(row, 7, apartment_item)
    
    def _on_search(self, text: str):
        """Обработка изменения текста поиска."""
        if text:
            # Поиск по имени клиента, улице или городу
            data = self.db_manager.search_addresses(text)
        else:
            data = self._load_data()
        self._display_data(data)
    
    def _on_add(self):
        """Обработка нажатия кнопки Добавить."""
        dialog = AddressDialog(self.db_manager, parent=self)
        if dialog.exec():
            address = dialog.get_address()
            if not address.street:
                self.show_warning("Улица обязательна для заполнения")
                return
            if not address.city_id:
                self.show_warning("Выберите город")
                return
            
            try:
                self.db_manager.add_address(address)
                self.refresh_data()
                self.data_changed.emit()
                self.show_info("Адрес успешно добавлен")
            except Exception as e:
                self.show_error(f"Ошибка при добавлении: {str(e)}")
    
    def _on_edit(self):
        """Обработка нажатия кнопки Редактировать."""
        if not self._selected_id:
            return
        
        address = self.db_manager.get_address_by_id(self._selected_id)
        if not address:
            self.show_error("Адрес не найден")
            return
        
        dialog = AddressDialog(self.db_manager, address=address, parent=self)
        if dialog.exec():
            updated_address = dialog.get_address()
            if not updated_address.street:
                self.show_warning("Улица обязательна для заполнения")
                return
            if not updated_address.city_id:
                self.show_warning("Выберите город")
                return
            
            try:
                self.db_manager.update_address(updated_address)
                self.refresh_data()
                self.data_changed.emit()
                self.show_info("Адрес успешно обновлен")
            except Exception as e:
                self.show_error(f"Ошибка при обновлении: {str(e)}")
    
    def _on_delete(self):
        """Обработка нажатия кнопки Удалить."""
        if not self._selected_id:
            return
        
        address = self.db_manager.get_address_by_id(self._selected_id)
        if not address:
            return
        
        display_name = f"{address.client_name or 'Без имени'} - {address.full_address}"
        if self.confirm_delete(display_name):
            try:
                if self.db_manager.delete_address(self._selected_id):
                    self.refresh_data()
                    self.data_changed.emit()
                    self.show_info("Адрес успешно удален")
                else:
                    self.show_warning("Не удалось удалить адрес")
            except Exception as e:
                self.show_error(f"Ошибка при удалении: {str(e)}")
    
    def search_by_client(self, client_name: str):
        """Поиск адресов по имени клиента."""
        if client_name:
            data = self.db_manager.search_addresses_by_client(client_name)
        else:
            data = self._load_data()
        self._display_data(data)
