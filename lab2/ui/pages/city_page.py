"""
Страница управления городами.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QComboBox
)
from PyQt6.QtCore import Qt
from typing import List, Optional

from .base_page import BasePage
from database.models import City, Region


class CityDialog(QDialog):
    """Диалог для добавления/редактирования города."""
    
    def __init__(self, db_manager, city: City = None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.city = city or City()
        self._setup_ui()
        
        # Загрузка регионов в выпадающий список
        self._load_regions()
        
        if city:
            self.name_input.setText(city.name)
            self.postal_input.setText(city.postal_code or "")
            self.setWindowTitle("Редактирование города")
            # Выбор региона
            if city.region_id:
                for i in range(self.region_combo.count()):
                    if self.region_combo.itemData(i) == city.region_id:
                        self.region_combo.setCurrentIndex(i)
                        break
        else:
            self.setWindowTitle("Добавление города")
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Выбор региона
        region_layout = QHBoxLayout()
        region_layout.addWidget(QLabel("Регион:"))
        self.region_combo = QComboBox()
        self.region_combo.setPlaceholderText("Выберите регион")
        region_layout.addWidget(self.region_combo)
        layout.addLayout(region_layout)
        
        # Поле названия
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Название:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название города")
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Поле почтового индекса
        postal_layout = QHBoxLayout()
        postal_layout.addWidget(QLabel("Почтовый индекс:"))
        self.postal_input = QLineEdit()
        self.postal_input.setPlaceholderText("Введите почтовый индекс")
        postal_layout.addWidget(self.postal_input)
        layout.addLayout(postal_layout)
        
        # Кнопки
        button_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
    
    def _load_regions(self):
        """Загрузка регионов в выпадающий список."""
        regions = self.db_manager.get_all_regions()
        self.region_combo.clear()
        for region in regions:
            self.region_combo.addItem(f"{region.name} ({region.country_name})", region.id)
    
    def get_city(self) -> City:
        """Возвращает город с данными из диалога."""
        region_id = self.region_combo.currentData()
        return City(
            id=self.city.id,
            region_id=region_id,
            name=self.name_input.text().strip(),
            postal_code=self.postal_input.text().strip() or None
        )


class CityPage(BasePage):
    """Страница управления городами."""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(db_manager, "Управление городами", parent)
        self._setup_table()
        self.refresh_data()
    
    def _setup_table(self):
        """Настройка столбцов таблицы."""
        headers = ["ID", "Регион", "Страна", "Название", "Индекс"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setColumnHidden(0, True)  # Скрыть столбец ID
    
    def _get_table_columns(self) -> List[str]:
        return ["ID", "Регион", "Страна", "Название", "Индекс"]
    
    def _load_data(self) -> List[City]:
        return self.db_manager.get_all_cities()
    
    def _display_data(self, data: List[City]):
        """Отображение городов в таблице."""
        self.table.setRowCount(len(data))
        for row, city in enumerate(data):
            # ID (скрыт, хранится как пользовательские данные)
            id_item = QTableWidgetItem(str(city.id))
            id_item.setData(Qt.ItemDataRole.UserRole, city.id)
            self.table.setItem(row, 0, id_item)
            
            # Названия региона и страны (используем properties)
            region_item = QTableWidgetItem(city.region_name)
            self.table.setItem(row, 1, region_item)
            
            country_item = QTableWidgetItem(city.country_name)
            self.table.setItem(row, 2, country_item)
            
            # Название города
            name_item = QTableWidgetItem(city.name)
            self.table.setItem(row, 3, name_item)
            
            # Почтовый индекс
            postal_item = QTableWidgetItem(city.postal_code or "")
            self.table.setItem(row, 4, postal_item)
    
    def _on_search(self, text: str):
        """Обработка изменения текста поиска."""
        if text:
            data = self.db_manager.search_cities(text)
        else:
            data = self._load_data()
        self._display_data(data)
    
    def _on_add(self):
        """Обработка нажатия кнопки Добавить."""
        dialog = CityDialog(self.db_manager, parent=self)
        if dialog.exec():
            city = dialog.get_city()
            if not city.name:
                self.show_warning("Название города обязательно для заполнения")
                return
            if not city.region_id:
                self.show_warning("Выберите регион")
                return
            
            try:
                self.db_manager.add_city(city)
                self.refresh_data()
                self.data_changed.emit()
                self.show_info("Город успешно добавлен")
            except Exception as e:
                self.show_error(f"Ошибка при добавлении: {str(e)}")
    
    def _on_edit(self):
        """Обработка нажатия кнопки Редактировать."""
        if not self._selected_id:
            return
        
        city = self.db_manager.get_city_by_id(self._selected_id)
        if not city:
            self.show_error("Город не найден")
            return
        
        dialog = CityDialog(self.db_manager, city=city, parent=self)
        if dialog.exec():
            updated_city = dialog.get_city()
            if not updated_city.name:
                self.show_warning("Название города обязательно для заполнения")
                return
            if not updated_city.region_id:
                self.show_warning("Выберите регион")
                return
            
            try:
                self.db_manager.update_city(updated_city)
                self.refresh_data()
                self.data_changed.emit()
                self.show_info("Город успешно обновлен")
            except Exception as e:
                self.show_error(f"Ошибка при обновлении: {str(e)}")
    
    def _on_delete(self):
        """Обработка нажатия кнопки Удалить."""
        if not self._selected_id:
            return
        
        city = self.db_manager.get_city_by_id(self._selected_id)
        if not city:
            return
        
        if self.confirm_delete(city.name):
            try:
                if self.db_manager.delete_city(self._selected_id):
                    self.refresh_data()
                    self.data_changed.emit()
                    self.show_info("Город успешно удален")
                else:
                    self.show_warning("Не удалось удалить город")
            except Exception as e:
                self.show_error(f"Ошибка при удалении: {str(e)}")
