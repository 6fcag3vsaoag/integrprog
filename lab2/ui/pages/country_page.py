"""
Страница управления странами.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QLabel, QPushButton, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from typing import List

from .base_page import BasePage
from database.models import Country


class CountryDialog(QDialog):
    """Диалог для добавления/редактирования страны."""
    
    def __init__(self, country: Country = None, parent=None):
        super().__init__(parent)
        self.country = country or Country()
        self._setup_ui()
        
        if country:
            self.name_input.setText(country.name)
            self.code_input.setText(country.code or "")
            self.setWindowTitle("Редактирование страны")
        else:
            self.setWindowTitle("Добавление страны")
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Поле названия
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Название:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название страны")
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Поле кода
        code_layout = QHBoxLayout()
        code_layout.addWidget(QLabel("Код (ISO):"))
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Например: BY, RU")
        self.code_input.setMaxLength(2)
        code_layout.addWidget(self.code_input)
        layout.addLayout(code_layout)
        
        # Кнопки
        button_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
    
    def get_country(self) -> Country:
        """Возвращает страну с данными из диалога."""
        return Country(
            id=self.country.id,
            name=self.name_input.text().strip(),
            code=self.code_input.text().strip().upper()
        )


class CountryPage(BasePage):
    """Страница управления странами."""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(db_manager, "Управление странами", parent)
        self._setup_table()
        self.refresh_data()
    
    def _setup_table(self):
        """Настройка столбцов таблицы."""
        headers = ["ID", "Название", "Код"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setColumnHidden(0, True)  # Скрыть столбец ID
    
    def _get_table_columns(self) -> List[str]:
        return ["ID", "Название", "Код"]
    
    def _load_data(self) -> List[Country]:
        return self.db_manager.get_all_countries()
    
    def _display_data(self, data: List[Country]):
        """Отображение стран в таблице."""
        self.table.setRowCount(len(data))
        for row, country in enumerate(data):
            # ID (скрыт, хранится как пользовательские данные)
            id_item = QTableWidgetItem(str(country.id))
            id_item.setData(Qt.ItemDataRole.UserRole, country.id)
            self.table.setItem(row, 0, id_item)
            
            # Название
            name_item = QTableWidgetItem(country.name)
            self.table.setItem(row, 1, name_item)
            
            # Код
            code_item = QTableWidgetItem(country.code or "")
            self.table.setItem(row, 2, code_item)
    
    def _on_search(self, text: str):
        """Обработка изменения текста поиска."""
        if text:
            data = self.db_manager.search_countries(text)
        else:
            data = self._load_data()
        self._display_data(data)
    
    def _on_add(self):
        """Обработка нажатия кнопки Добавить."""
        dialog = CountryDialog(parent=self)
        if dialog.exec():
            country = dialog.get_country()
            if not country.name:
                self.show_warning("Название страны обязательно для заполнения")
                return
            
            try:
                self.db_manager.add_country(country)
                self.refresh_data()
                self.data_changed.emit()
                self.show_info("Страна успешно добавлена")
            except Exception as e:
                self.show_error(f"Ошибка при добавлении: {str(e)}")
    
    def _on_edit(self):
        """Обработка нажатия кнопки Редактировать."""
        if not self._selected_id:
            return
        
        country = self.db_manager.get_country_by_id(self._selected_id)
        if not country:
            self.show_error("Страна не найдена")
            return
        
        dialog = CountryDialog(country=country, parent=self)
        if dialog.exec():
            updated_country = dialog.get_country()
            if not updated_country.name:
                self.show_warning("Название страны обязательно для заполнения")
                return
            
            try:
                self.db_manager.update_country(updated_country)
                self.refresh_data()
                self.data_changed.emit()
                self.show_info("Страна успешно обновлена")
            except Exception as e:
                self.show_error(f"Ошибка при обновлении: {str(e)}")
    
    def _on_delete(self):
        """Обработка нажатия кнопки Удалить."""
        if not self._selected_id:
            return
        
        country = self.db_manager.get_country_by_id(self._selected_id)
        if not country:
            return
        
        if self.confirm_delete(country.name):
            try:
                if self.db_manager.delete_country(self._selected_id):
                    self.refresh_data()
                    self.data_changed.emit()
                    self.show_info("Страна успешно удалена")
                else:
                    self.show_warning("Не удалось удалить страну")
            except Exception as e:
                self.show_error(f"Ошибка при удалении: {str(e)}")
