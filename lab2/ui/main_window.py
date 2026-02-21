"""
Главное окно приложения для управления адресами клиентов.
Обеспечивает навигацию между страницами и главное меню.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QStatusBar,
    QMessageBox
)
from PyQt6.QtGui import QAction

from database import DatabaseManager
from .pages import CountryPage, RegionPage, CityPage, AddressPage


class MainWindow(QMainWindow):
    """Главное окно приложения с навигацией по страницам."""
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self._setup_ui()
        self._setup_menu()
        self._update_status()
    
    def _setup_ui(self):
        """Настройка основного интерфейса."""
        self.setWindowTitle("Информационная подсистема ведения адресов клиентов")
        self.setMinimumSize(900, 600)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Панель навигации (левая сторона)
        nav_widget = QWidget()
        nav_widget.setObjectName("navPanel")
        nav_widget.setMaximumWidth(200)
        nav_widget.setMinimumWidth(180)
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(10, 10, 10, 10)
        nav_layout.setSpacing(5)
        
        # Кнопки навигации
        self.nav_buttons = []
        
        self.address_btn = QPushButton("Адреса")
        self.address_btn.setObjectName("navButton")
        self.address_btn.clicked.connect(lambda: self._show_page(0))
        nav_layout.addWidget(self.address_btn)
        self.nav_buttons.append(self.address_btn)
        
        self.country_btn = QPushButton("Страны")
        self.country_btn.setObjectName("navButton")
        self.country_btn.clicked.connect(lambda: self._show_page(1))
        nav_layout.addWidget(self.country_btn)
        self.nav_buttons.append(self.country_btn)
        
        self.region_btn = QPushButton("Регионы")
        self.region_btn.setObjectName("navButton")
        self.region_btn.clicked.connect(lambda: self._show_page(2))
        nav_layout.addWidget(self.region_btn)
        self.nav_buttons.append(self.region_btn)
        
        self.city_btn = QPushButton("Города")
        self.city_btn.setObjectName("navButton")
        self.city_btn.clicked.connect(lambda: self._show_page(3))
        nav_layout.addWidget(self.city_btn)
        self.nav_buttons.append(self.city_btn)
        
        nav_layout.addStretch()
        
        # Метка статистики
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("padding: 5px; font-size: 11px;")
        nav_layout.addWidget(self.stats_label)
        
        main_layout.addWidget(nav_widget)
        
        # Область контента (правая сторона)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        # Stacked widget для страниц
        self.pages = QStackedWidget()
        
        # Создание страниц
        self.address_page = AddressPage(self.db_manager)
        self.country_page = CountryPage(self.db_manager)
        self.region_page = RegionPage(self.db_manager)
        self.city_page = CityPage(self.db_manager)
        
        # Подключение сигналов изменения данных
        self.country_page.data_changed.connect(self._on_data_changed)
        self.region_page.data_changed.connect(self._on_data_changed)
        self.city_page.data_changed.connect(self._on_data_changed)
        self.address_page.data_changed.connect(self._on_data_changed)
        
        # Добавление страниц в стек
        self.pages.addWidget(self.address_page)
        self.pages.addWidget(self.country_page)
        self.pages.addWidget(self.region_page)
        self.pages.addWidget(self.city_page)
        
        content_layout.addWidget(self.pages)
        main_layout.addWidget(content_widget, 1)
        
        # Строка состояния
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готово")
        
        # Применение стилей
        self._apply_style()
        
        # Показ первой страницы
        self._show_page(0)
    
    def _setup_menu(self):
        """Настройка строки меню."""
        menubar = self.menuBar()
        
        # Меню Файл
        file_menu = menubar.addMenu("Файл")
        
        refresh_action = QAction("Обновить", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self._refresh_current_page)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Меню Вид
        view_menu = menubar.addMenu("Вид")
        
        addresses_action = QAction("Адреса", self)
        addresses_action.setShortcut("Ctrl+1")
        addresses_action.triggered.connect(lambda: self._show_page(0))
        view_menu.addAction(addresses_action)
        
        countries_action = QAction("Страны", self)
        countries_action.setShortcut("Ctrl+2")
        countries_action.triggered.connect(lambda: self._show_page(1))
        view_menu.addAction(countries_action)
        
        regions_action = QAction("Регионы", self)
        regions_action.setShortcut("Ctrl+3")
        regions_action.triggered.connect(lambda: self._show_page(2))
        view_menu.addAction(regions_action)
        
        cities_action = QAction("Города", self)
        cities_action.setShortcut("Ctrl+4")
        cities_action.triggered.connect(lambda: self._show_page(3))
        view_menu.addAction(cities_action)
        
        # Меню Справка
        help_menu = menubar.addMenu("Справка")
        
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _apply_style(self):
        """Применение стилей приложения."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            
            #navPanel {
                background-color: #4a5568;
            }
            
            #navButton {
                background-color: transparent;
                color: #e2e8f0;
                border: none;
                padding: 12px;
                text-align: left;
                font-size: 13px;
                border-radius: 6px;
            }
            
            #navButton:hover {
                background-color: #5a6778;
            }
            
            #navButton:checked, #navButton:pressed {
                background-color: #667eea;
            }
            
            QPushButton {
                padding: 8px 16px;
                background-color: #667eea;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 500;
            }
            
            QPushButton:hover {
                background-color: #5a67d8;
            }
            
            QPushButton:pressed {
                background-color: #4c51bf;
            }
            
            QPushButton:disabled {
                background-color: #cbd5e0;
            }
            
            QTableWidget {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                gridline-color: #edf2f7;
                color: #1a202c;
            }
            
            QTableWidget::item {
                padding: 8px;
                color: #1a202c;
            }
            
            QTableWidget::item:selected {
                background-color: #667eea;
                color: white;
            }
            
            QHeaderView::section {
                background-color: #4a5568;
                color: white;
                padding: 10px;
                border: none;
                font-weight: 500;
            }
            
            QLineEdit {
                padding: 10px;
                border: 2px solid #e2e8f0;
                border-radius: 6px;
                background-color: white;
                color: #1a202c;
            }
            
            QLineEdit:focus {
                border-color: #667eea;
            }
            
            QComboBox {
                padding: 10px;
                border: 2px solid #e2e8f0;
                border-radius: 6px;
                background-color: white;
                color: #1a202c;
            }
            
            QComboBox:focus {
                border-color: #667eea;
            }
            
            QComboBox QAbstractItemView {
                background-color: white;
                color: #1a202c;
                selection-background-color: #667eea;
                selection-color: white;
            }
            
            QStatusBar {
                background-color: #edf2f7;
                color: #4a5568;
            }
            
            QLabel {
                color: #2d3748;
            }
            
            QMenuBar {
                background-color: #4a5568;
                color: white;
            }
            
            QMenuBar::item:selected {
                background-color: #667eea;
            }
            
            QMenu {
                background-color: white;
                color: #1a202c;
                border: 1px solid #e2e8f0;
            }
            
            QMenu::item {
                color: #1a202c;
                padding: 8px 25px;
            }
            
            QMenu::item:selected {
                background-color: #667eea;
                color: white;
            }
            
            QMessageBox {
                background-color: white;
            }
            
            QMessageBox QLabel {
                color: #1a202c;
            }
        """)
    
    def _show_page(self, index: int):
        """Показать указанную страницу."""
        self.pages.setCurrentIndex(index)
        
        # Обновление состояния кнопок навигации
        for i, btn in enumerate(self.nav_buttons):
            btn.setProperty("checked", i == index)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        
        # Обновление строки состояния
        page_names = ["Адреса", "Страны", "Регионы", "Города"]
        self.status_bar.showMessage(f"Страница: {page_names[index]}")
    
    def _refresh_current_page(self):
        """Обновить текущую страницу."""
        current_page = self.pages.currentWidget()
        if hasattr(current_page, 'refresh_data'):
            current_page.refresh_data()
        self._update_status()
        self.status_bar.showMessage("Данные обновлены", 2000)
    
    def _on_data_changed(self):
        """Обработка сигнала изменения данных."""
        self._update_status()
    
    def _update_status(self):
        """Обновление отображения статистики."""
        stats = self.db_manager.get_statistics()
        stats_text = (
            f"Стран: {stats['countries']}\n"
            f"Регионов: {stats['regions']}\n"
            f"Городов: {stats['cities']}\n"
            f"Адресов: {stats['addresses']}"
        )
        self.stats_label.setText(stats_text)
        self.stats_label.setStyleSheet("padding: 5px; font-size: 11px; color: #cbd5e0;")
    
    def _show_about(self):
        """Показать диалог О программе."""
        QMessageBox.about(
            self,
            "О программе",
            "<h3>Информационная подсистема ведения адресов клиентов</h3>"
            "<p>Версия 1.0</p>"
            "<p>Приложение для управления адресами клиентов.</p>"
            "<p><b>Функции:</b></p>"
            "<ul>"
            "<li>Просмотр данных</li>"
            "<li>Ввод данных</li>"
            "<li>Редактирование данных</li>"
            "<li>Удаление данных</li>"
            "<li>Поиск данных по клиенту</li>"
            "</ul>"
            "<p>База данных: SQLite</p>"
        )
    
    def closeEvent(self, event):
        """Обработка события закрытия окна."""
        self.db_manager.close()
        event.accept()
