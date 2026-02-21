"""
Страница управления регионами.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QComboBox
)
from PyQt6.QtCore import Qt
from typing import List, Optional

from .base_page import BasePage
from database.models import Region, Country


class RegionDialog(QDialog):
    """Диалог для добавления/редактирования региона."""
    
    def __init__(self, db_manager, region: Region = None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.region = region or Region()
        self._setup_ui()
        
        # Загрузка стран в выпадающий список
        self._load_countries()
        
        if region:
            self.name_input.setText(region.name)
            self.setWindowTitle("Редактирование региона")
            # Выбор страны
            if region.country_id:
                for i in range(self.country_combo.count()):
                    if self.country_combo.itemData(i) == region.country_id:
                        self.country_combo.setCurrentIndex(i)
                        break
        else:
            self.setWindowTitle("Добавление региона")
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Выбор страны
        country_layout = QHBoxLayout()
        country_layout.addWidget(QLabel("Страна:"))
        self.country_combo = QComboBox()
        self.country_combo.setPlaceholderText("Выберите страну")
        country_layout.addWidget(self.country_combo)
        layout.addLayout(country_layout)
        
        # Поле названия
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Название:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название региона")
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Кнопки
        button_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
    
    def _load_countries(self):
        """Загрузка стран в выпадающий список."""
        countries = self.db_manager.get_all_countries()
        self.country_combo.clear()
        for country in countries:
            self.country_combo.addItem(country.name, country.id)
    
    def get_region(self) -> Region:
        """Возвращает регион с данными из диалога."""
        country_id = self.country_combo.currentData()
        return Region(
            id=self.region.id,
            country_id=country_id,
            name=self.name_input.text().strip()
        )


class RegionPage(BasePage):
    """Страница управления регионами."""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(db_manager, "Управление регионами", parent)
        self._setup_table()
        self.refresh_data()
    
    def _setup_table(self):
        """Настройка столбцов таблицы."""
        headers = ["ID", "Страна", "Название"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setColumnHidden(0, True)  # Скрыть столбец ID
    
    def _get_table_columns(self) -> List[str]:
        return ["ID", "Страна", "Название"]
    
    def _load_data(self) -> List[Region]:
        return self.db_manager.get_all_regions()
    
    def _display_data(self, data: List[Region]):
        """Отображение регионов в таблице."""
        self.table.setRowCount(len(data))
        for row, region in enumerate(data):
            # ID (скрыт, хранится как пользовательские данные)
            id_item = QTableWidgetItem(str(region.id))
            id_item.setData(Qt.ItemDataRole.UserRole, region.id)
            self.table.setItem(row, 0, id_item)
            
            # Название страны
            country = self.db_manager.get_country_by_id(region.country_id)
            country_item = QTableWidgetItem(country.name if country else "")
            self.table.setItem(row, 1, country_item)
            
            # Название региона
            name_item = QTableWidgetItem(region.name)
            self.table.setItem(row, 2, name_item)
    
    def _on_search(self, text: str):
        """Обработка изменения текста поиска."""
        if text:
            data = self.db_manager.search_regions(text)
        else:
            data = self._load_data()
        self._display_data(data)
    
    def _on_add(self):
        """Обработка нажатия кнопки Добавить."""
        dialog = RegionDialog(self.db_manager, parent=self)
        if dialog.exec():
            region = dialog.get_region()
            if not region.name:
                self.show_warning("Название региона обязательно для заполнения")
                return
            if not region.country_id:
                self.show_warning("Выберите страну")
                return
            
            try:
                self.db_manager.add_region(region)
                self.refresh_data()
                self.data_changed.emit()
                self.show_info("Регион успешно добавлен")
            except Exception as e:
                self.show_error(f"Ошибка при добавлении: {str(e)}")
    
    def _on_edit(self):
        """Обработка нажатия кнопки Редактировать."""
        if not self._selected_id:
            return
        
        region = self.db_manager.get_region_by_id(self._selected_id)
        if not region:
            self.show_error("Регион не найден")
            return
        
        dialog = RegionDialog(self.db_manager, region=region, parent=self)
        if dialog.exec():
            updated_region = dialog.get_region()
            if not updated_region.name:
                self.show_warning("Название региона обязательно для заполнения")
                return
            if not updated_region.country_id:
                self.show_warning("Выберите страну")
                return
            
            try:
                self.db_manager.update_region(updated_region)
                self.refresh_data()
                self.data_changed.emit()
                self.show_info("Регион успешно обновлен")
            except Exception as e:
                self.show_error(f"Ошибка при обновлении: {str(e)}")
    
    def _on_delete(self):
        """Обработка нажатия кнопки Удалить."""
        if not self._selected_id:
            return
        
        region = self.db_manager.get_region_by_id(self._selected_id)
        if not region:
            return
        
        if self.confirm_delete(region.name):
            try:
                if self.db_manager.delete_region(self._selected_id):
                    self.refresh_data()
                    self.data_changed.emit()
                    self.show_info("Регион успешно удален")
                else:
                    self.show_warning("Не удалось удалить регион")
            except Exception as e:
                self.show_error(f"Ошибка при удалении: {str(e)}")
