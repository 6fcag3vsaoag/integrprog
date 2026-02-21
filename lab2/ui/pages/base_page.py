"""
Базовый виджет страницы с общим функционалом для всех страниц CRUD.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLineEdit, QTableWidget, QMessageBox,
    QLabel, QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import List, Optional, Any


class BasePage(QWidget):
    """Базовый класс для страниц CRUD с общим функционалом."""
    
    # Сигналы для навигации по страницам
    data_changed = pyqtSignal()
    
    def __init__(self, db_manager, title: str, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.title = title
        self._selected_id: Optional[int] = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Настройка базовой структуры интерфейса."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Заголовок
        title_label = QLabel(self.title)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Панель поиска
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск...")
        self.search_input.textChanged.connect(self._on_search)
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Таблица
        self.table = QTableWidget()
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        layout.addWidget(self.table)
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self._on_add)
        button_layout.addWidget(self.add_btn)
        
        self.edit_btn = QPushButton("Редактировать")
        self.edit_btn.clicked.connect(self._on_edit)
        self.edit_btn.setEnabled(False)
        button_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self._on_delete)
        self.delete_btn.setEnabled(False)
        button_layout.addWidget(self.delete_btn)
        
        self.refresh_btn = QPushButton("Обновить")
        self.refresh_btn.clicked.connect(self.refresh_data)
        button_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(button_layout)
    
    def _get_table_columns(self) -> List[str]:
        """Возвращает список заголовков столбцов таблицы. Переопределить в подклассах."""
        return []
    
    def _load_data(self) -> List[Any]:
        """Загрузить данные из базы данных. Переопределить в подклассах."""
        return []
    
    def _display_data(self, data: List[Any]):
        """Отобразить данные в таблице. Переопределить в подклассах."""
        pass
    
    def _on_search(self, text: str):
        """Обработка изменения текста поиска."""
        pass
    
    def _on_selection_changed(self):
        """Обработка изменения выбора в таблице."""
        selected_rows = self.table.selectedItems()
        if selected_rows:
            row = selected_rows[0].row()
            # Предполагаем, что ID хранится в данных первого столбца
            id_item = self.table.item(row, 0)
            if id_item:
                self._selected_id = id_item.data(Qt.ItemDataRole.UserRole)
            self.edit_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
        else:
            self._selected_id = None
            self.edit_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
    
    def _on_add(self):
        """Обработка нажатия кнопки Добавить. Переопределить в подклассах."""
        pass
    
    def _on_edit(self):
        """Обработка нажатия кнопки Редактировать. Переопределить в подклассах."""
        pass
    
    def _on_delete(self):
        """Обработка нажатия кнопки Удалить. Переопределить в подклассах."""
        pass
    
    def refresh_data(self):
        """Обновить данные таблицы."""
        data = self._load_data()
        self._display_data(data)
        self._selected_id = None
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
    
    def show_info(self, message: str):
        """Показать информационное сообщение."""
        QMessageBox.information(self, "Информация", message)
    
    def show_warning(self, message: str):
        """Показать предупреждение."""
        QMessageBox.warning(self, "Предупреждение", message)
    
    def show_error(self, message: str):
        """Показать сообщение об ошибке."""
        QMessageBox.critical(self, "Ошибка", message)
    
    def confirm_delete(self, item_name: str) -> bool:
        """Показать диалог подтверждения удаления."""
        reply = QMessageBox.question(
            self, "Подтверждение удаления",
            f"Вы уверены, что хотите удалить '{item_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes
