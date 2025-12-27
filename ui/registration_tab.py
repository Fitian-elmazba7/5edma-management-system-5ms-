# registration_tab.py - Dashboard Grid Layout with Stats
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QLabel, QPushButton, QGroupBox, QTextEdit, 
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QCompleter, QComboBox, QMenu, QAction, QDialog,
                             QFrame, QSizePolicy, QSpacerItem, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from utils.database import DatabaseManager
import json
import os
from datetime import datetime
from .modern_widget import ModernWidget
from .child_details_dialog import ChildDetailsDialog

class RegistrationTab(ModernWidget):
    registration_finished = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.registered_codes = set()
        self.all_children = []
        self.session_file = "data/current_session.json"
        self.current_selected_child = None
        self.name_to_child_map = {}
        self.setup_ui()
        self.load_children_data()
        self.load_current_session()
        self.apply_scaled_stylesheet()
    
    def setup_ui(self):
        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(24, 24, 24, 24)
        
        # ═══════════════════════════════════════════════════════════════
        # ROW 1: STATS CARDS (4 cards in a row)
        # ═══════════════════════════════════════════════════════════════
        stats_row = QHBoxLayout()
        stats_row.setSpacing(16)
        
        # Get stats data
        all_children = self.db.get_all_children()
        total_children = len(all_children)
        
        # Stat Card 1: Total Children
        self.stat_total = self.create_stat_card(
            "إجمالي الأطفال", 
            str(total_children), 
            "👥",
            "#22c55e"  # Green
        )
        stats_row.addWidget(self.stat_total)
        
        # Stat Card 2: Registered Today
        self.stat_registered = self.create_stat_card(
            "مسجلين اليوم", 
            "0", 
            "✅",
            "#3b82f6"  # Blue
        )
        stats_row.addWidget(self.stat_registered)
        
        # Stat Card 3: Remaining
        self.stat_remaining = self.create_stat_card(
            "المتبقين", 
            str(total_children), 
            "⏳",
            "#f59e0b"  # Amber
        )
        stats_row.addWidget(self.stat_remaining)
        
        # Stat Card 4: Session Time
        self.stat_time = self.create_stat_card(
            "وقت الجلسة", 
            datetime.now().strftime("%H:%M"), 
            "🕐",
            "#8b5cf6"  # Purple
        )
        stats_row.addWidget(self.stat_time)
        
        main_layout.addLayout(stats_row)
        
        # ═══════════════════════════════════════════════════════════════
        # ROW 2: INPUT SECTION + INFO SECTION (Grid 2 columns)
        # ═══════════════════════════════════════════════════════════════
        middle_row = QHBoxLayout()
        middle_row.setSpacing(16)
        
        # LEFT SIDE: Input Card (wider - 2/3)
        input_card = QFrame()
        input_card.setObjectName("inputCard")
        input_card.setProperty("class", "dashboard-card")
        input_card_layout = QVBoxLayout(input_card)
        input_card_layout.setSpacing(16)
        input_card_layout.setContentsMargins(20, 20, 20, 20)
        
        # Card Header with icon
        input_header_row = QHBoxLayout()
        input_icon = QLabel("🎯")
        input_icon.setProperty("class", "card-icon")
        input_title = QLabel("تسجيل الحضور")
        input_title.setProperty("class", "card-title")
        input_header_row.addWidget(input_icon)
        input_header_row.addWidget(input_title)
        input_header_row.addStretch()
        input_card_layout.addLayout(input_header_row)
        
        # Separator line
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)
        separator1.setProperty("class", "card-separator")
        input_card_layout.addWidget(separator1)
        
        # Code Input Row
        code_row = QHBoxLayout()
        code_row.setSpacing(12)
        
        code_label = QLabel("الكود:")
        code_label.setProperty("class", "input-label")
        code_label.setFixedWidth(50)
        
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("أدخل كود الطفل...")
        self.code_input.setProperty("class", "dashboard-input")
        self.code_input.setMinimumHeight(44)
        self.code_input.returnPressed.connect(self.register_by_code)
        self.code_input.textChanged.connect(self.on_code_changed)
        
        self.register_btn = QPushButton("تسجيل")
        self.register_btn.setProperty("class", "btn-success")
        self.register_btn.setMinimumHeight(44)
        self.register_btn.setMinimumWidth(100)
        self.register_btn.clicked.connect(self.register_by_code)
        
        code_row.addWidget(code_label)
        code_row.addWidget(self.code_input, 1)
        code_row.addWidget(self.register_btn)
        input_card_layout.addLayout(code_row)
        
        # Name Input Row
        name_row = QHBoxLayout()
        name_row.setSpacing(12)
        
        name_label = QLabel("الاسم:")
        name_label.setProperty("class", "input-label")
        name_label.setFixedWidth(50)
        
        self.name_input = QComboBox()
        self.name_input.setEditable(True)
        self.name_input.setPlaceholderText("ابحث باسم الطفل...")
        self.name_input.setProperty("class", "dashboard-combo")
        self.name_input.setMinimumHeight(44)
        self.name_input.lineEdit().textChanged.connect(self.on_name_changed)
        self.name_input.lineEdit().returnPressed.connect(self.register_by_name_enter)
        
        self.search_btn = QPushButton("بحث")
        self.search_btn.setProperty("class", "btn-secondary")
        self.search_btn.setMinimumHeight(44)
        self.search_btn.setMinimumWidth(100)
        self.search_btn.clicked.connect(self.search_by_name)
        
        name_row.addWidget(name_label)
        name_row.addWidget(self.name_input, 1)
        name_row.addWidget(self.search_btn)
        input_card_layout.addLayout(name_row)
        
        middle_row.addWidget(input_card, 2)  # 2/3 width
        
        # RIGHT SIDE: Child Info Card (1/3)
        info_card = QFrame()
        info_card.setObjectName("infoCard")
        info_card.setProperty("class", "dashboard-card")
        info_card_layout = QVBoxLayout(info_card)
        info_card_layout.setSpacing(12)
        info_card_layout.setContentsMargins(20, 20, 20, 20)
        
        # Card Header
        info_header_row = QHBoxLayout()
        info_icon = QLabel("📋")
        info_icon.setProperty("class", "card-icon")
        info_title = QLabel("بيانات الطفل")
        info_title.setProperty("class", "card-title")
        info_header_row.addWidget(info_icon)
        info_header_row.addWidget(info_title)
        info_header_row.addStretch()
        info_card_layout.addLayout(info_header_row)
        
        # Separator
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setProperty("class", "card-separator")
        info_card_layout.addWidget(separator2)
        
        # Info Display
        self.info_display = QTextEdit()
        self.info_display.setReadOnly(True)
        self.info_display.setProperty("class", "info-display")
        self.info_display.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        info_card_layout.addWidget(self.info_display, 1)
        
        middle_row.addWidget(info_card, 1)  # 1/3 width
        
        main_layout.addLayout(middle_row)
        
        # ═══════════════════════════════════════════════════════════════
        # ROW 3: SEARCH CARD + TABLE PREVIEW (Grid 2 columns)
        # ═══════════════════════════════════════════════════════════════
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(16)
        
        # LEFT: Session Search
        search_card = QFrame()
        search_card.setObjectName("searchCard")
        search_card.setProperty("class", "dashboard-card")
        search_card_layout = QVBoxLayout(search_card)
        search_card_layout.setSpacing(12)
        search_card_layout.setContentsMargins(20, 20, 20, 20)
        
        # Card Header
        search_header_row = QHBoxLayout()
        search_icon = QLabel("🔍")
        search_icon.setProperty("class", "card-icon")
        search_title = QLabel("بحث في الجلسة")
        search_title.setProperty("class", "card-title")
        search_header_row.addWidget(search_icon)
        search_header_row.addWidget(search_title)
        search_header_row.addStretch()
        search_card_layout.addLayout(search_header_row)
        
        # Separator
        separator3 = QFrame()
        separator3.setFrameShape(QFrame.HLine)
        separator3.setProperty("class", "card-separator")
        search_card_layout.addWidget(separator3)
        
        # Search Input
        search_input_row = QHBoxLayout()
        search_input_row.setSpacing(8)
        
        self.session_search_input = QLineEdit()
        self.session_search_input.setPlaceholderText("ابحث بالاسم أو الكود...")
        self.session_search_input.setProperty("class", "dashboard-input")
        self.session_search_input.setMinimumHeight(40)
        self.session_search_input.textChanged.connect(self.search_in_current_session)
        
        self.clear_search_btn = QPushButton("مسح")
        self.clear_search_btn.setProperty("class", "btn-danger")
        self.clear_search_btn.setMinimumHeight(40)
        self.clear_search_btn.clicked.connect(self.clear_session_search)
        
        search_input_row.addWidget(self.session_search_input, 1)
        search_input_row.addWidget(self.clear_search_btn)
        search_card_layout.addLayout(search_input_row)
        
        # Search Results
        self.search_results_display = QTextEdit()
        self.search_results_display.setReadOnly(True)
        self.search_results_display.setMaximumHeight(120)
        self.search_results_display.setProperty("class", "results-display")
        search_card_layout.addWidget(self.search_results_display)
        
        bottom_row.addWidget(search_card, 1)
        
        # RIGHT: Attendance Table
        table_card = QFrame()
        table_card.setObjectName("tableCard")
        table_card.setProperty("class", "dashboard-card")
        table_card_layout = QVBoxLayout(table_card)
        table_card_layout.setSpacing(12)
        table_card_layout.setContentsMargins(20, 20, 20, 20)
        
        # Card Header with action buttons
        table_header_row = QHBoxLayout()
        table_icon = QLabel("📊")
        table_icon.setProperty("class", "card-icon")
        table_title = QLabel("قائمة الحضور")
        table_title.setProperty("class", "card-title")
        table_header_row.addWidget(table_icon)
        table_header_row.addWidget(table_title)
        table_header_row.addStretch()
        
        # Mini action buttons
        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.setProperty("class", "btn-icon")
        self.refresh_btn.setFixedSize(36, 36)
        self.refresh_btn.setToolTip("تحديث البيانات")
        self.refresh_btn.clicked.connect(self.refresh_data)
        table_header_row.addWidget(self.refresh_btn)
        
        table_card_layout.addLayout(table_header_row)
        
        # Separator
        separator4 = QFrame()
        separator4.setFrameShape(QFrame.HLine)
        separator4.setProperty("class", "card-separator")
        table_card_layout.addWidget(separator4)
        
        # Attendance Table
        self.attendance_table = QTableWidget()
        self.attendance_table.setColumnCount(5)
        self.attendance_table.setHorizontalHeaderLabels(["الكود", "الاسم", "الصف", "الوقت", "التاريخ"])
        self.attendance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.attendance_table.setSortingEnabled(True)
        self.attendance_table.setAlternatingRowColors(True)
        self.attendance_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.attendance_table.customContextMenuRequested.connect(self.show_attendance_context_menu)
        self.attendance_table.setProperty("class", "dashboard-table")
        table_card_layout.addWidget(self.attendance_table, 1)
        
        bottom_row.addWidget(table_card, 2)
        
        main_layout.addLayout(bottom_row, 1)  # Stretch
        
        # ═══════════════════════════════════════════════════════════════
        # ROW 4: ACTION BUTTONS BAR
        # ═══════════════════════════════════════════════════════════════
        action_bar = QFrame()
        action_bar.setProperty("class", "action-bar")
        action_layout = QHBoxLayout(action_bar)
        action_layout.setSpacing(12)
        action_layout.setContentsMargins(0, 16, 0, 0)
        
        action_layout.addStretch()
        
        self.clear_btn = QPushButton("🗑️ مسح الكل")
        self.clear_btn.setProperty("class", "btn-danger")
        self.clear_btn.setMinimumHeight(44)
        self.clear_btn.setMinimumWidth(120)
        self.clear_btn.clicked.connect(self.clear_session)
        
        self.finish_btn = QPushButton("✅ إنهاء الجلسة")
        self.finish_btn.setProperty("class", "btn-success")
        self.finish_btn.setMinimumHeight(44)
        self.finish_btn.setMinimumWidth(140)
        self.finish_btn.clicked.connect(self.finish_session)
        
        action_layout.addWidget(self.clear_btn)
        action_layout.addWidget(self.finish_btn)
        
        main_layout.addWidget(action_bar)
        
        self.setLayout(main_layout)
    
    def create_stat_card(self, title, value, icon, color):
        """Create a stat card widget"""
        card = QFrame()
        card.setProperty("class", "stat-card")
        card.setMinimumHeight(100)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        layout.setContentsMargins(20, 16, 20, 16)
        
        # Top row: icon and title
        top_row = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setProperty("class", "stat-icon")
        icon_label.setStyleSheet(f"font-size: 24px; color: {color};")
        
        title_label = QLabel(title)
        title_label.setProperty("class", "stat-title")
        
        top_row.addWidget(icon_label)
        top_row.addStretch()
        
        layout.addLayout(top_row)
        
        # Value
        value_label = QLabel(value)
        value_label.setObjectName(f"stat_value_{title}")
        value_label.setProperty("class", "stat-value")
        value_label.setStyleSheet(f"color: {color};")
        layout.addWidget(value_label)
        
        # Title below value
        subtitle_label = QLabel(title)
        subtitle_label.setProperty("class", "stat-subtitle")
        layout.addWidget(subtitle_label)
        
        layout.addStretch()
        
        return card
    
    def update_stats(self):
        """Update the stat cards"""
        registered_count = len(self.registered_codes)
        all_children = self.db.get_all_children()
        total = len(all_children)
        remaining = total - registered_count
        
        # Update stat card values
        for card in [self.stat_total, self.stat_registered, self.stat_remaining, self.stat_time]:
            value_label = card.findChild(QLabel, card.findChildren(QLabel)[0].objectName() if card.findChildren(QLabel) else None)
        
        # Simple update via re-finding labels
        self.stat_registered.findChildren(QLabel)[1].setText(str(registered_count))
        self.stat_remaining.findChildren(QLabel)[1].setText(str(remaining))
        self.stat_time.findChildren(QLabel)[1].setText(datetime.now().strftime("%H:%M"))
    
    def apply_scaled_stylesheet(self):
        """No-op: Styles are handled by main.qss"""
        pass

    def save_current_session(self):
        """حفظ الجلسة الحالية في ملف"""
        try:
            session_data = {
                'registered_codes': list(self.registered_codes),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Error saving session: {e}")
    
    def load_current_session(self):
        """تحميل الجلسة السابقة من ملف"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                for code in session_data.get('registered_codes', []):
                    child = self.db.get_child_by_code(code)
                    if child and code not in self.registered_codes:
                        self.add_to_attendance_table(child)
                        self.registered_codes.add(code)
                
                if self.registered_codes:
                    self.update_buttons_state()
                    self.update_stats()
                    QMessageBox.information(self, "تم استعادة الجلسة", 
                                          f"تم استعادة {len(self.registered_codes)} طفل من الجلسة السابقة")
                    
        except Exception as e:
            print(f"Error loading session: {e}")
    
    def clear_session_file(self):
        """مسح ملف الجلسة"""
        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
        except Exception as e:
            print(f"Error clearing session file: {e}")
    
    def normalize_arabic_text(self, text):
        """تقوم بتطبيع النص العربي"""
        if not text:
            return text
        replacements = {
            'أ': 'ا', 'إ': 'ا', 'آ': 'ا',
            'ى': 'ي', 'ئ': 'ي', 'ة': 'ه',
        }
        normalized_text = str(text)
        for old_char, new_char in replacements.items():
            normalized_text = normalized_text.replace(old_char, new_char)
        return normalized_text
    
    def load_children_data(self):
        """تحميل بيانات الأطفال"""
        self.all_children = self.db.get_all_children()
        names = []
        self.name_to_child_map = {}
        
        for child in self.all_children:
            name = child.get('name', '')
            if name and name != 'غير محدد':
                names.append(name)
                self.name_to_child_map[name] = child
        
        completer = QCompleter(names)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        
        self.name_input.setCompleter(completer)
        self.name_input.clear()
        self.name_input.addItems(names)
        
        # Update total stat
        if hasattr(self, 'stat_total'):
            self.stat_total.findChildren(QLabel)[1].setText(str(len(self.all_children)))
    
    def on_name_changed(self, text):
        """عرض تفاصيل الطفل"""
        name = text.strip()
        if not name:
            self.info_display.clear()
            self.current_selected_child = None
            return
        
        child = self.name_to_child_map.get(name)
        if child:
            self.current_selected_child = child
            self.show_child_details(child)
            self.code_input.setText(child.get('code', ''))
            return
        
        found_child = None
        normalized_search = self.normalize_arabic_text(name).lower()
        
        for child_name, child_obj in self.name_to_child_map.items():
            normalized_child_name = self.normalize_arabic_text(child_name).lower()
            if normalized_child_name == normalized_search:
                found_child = child_obj
                break
        
        if found_child:
            self.current_selected_child = found_child
            self.show_child_details(found_child)
            self.code_input.setText(found_child.get('code', ''))
            self.name_input.lineEdit().setText(found_child.get('name', ''))
        else:
            self.info_display.clear()
            self.current_selected_child = None
    
    def search_by_name(self):
        name = self.name_input.currentText().strip()
        if name:
            self.on_name_changed(name)
    
    def register_by_name_enter(self):
        if self.current_selected_child:
            self.register_child(self.current_selected_child)
        else:
            name = self.name_input.currentText().strip()
            if name:
                self.on_name_changed(name)
                if self.current_selected_child:
                    self.register_child(self.current_selected_child)
    
    def on_code_changed(self, text):
        if text.strip():
            child = self.db.get_child_by_code(text.strip())
            if child:
                self.current_selected_child = child
                self.show_child_details(child)
                self.name_input.setCurrentText(child.get('name', ''))
            else:
                self.info_display.setHtml("<div style='color: #f59e0b; text-align: center; padding: 20px;'>⚠️ الكود غير موجود</div>")
                self.current_selected_child = None
        else:
            self.info_display.clear()
            self.current_selected_child = None
    
    def show_child_details(self, child):
        details = f"""
<div style="font-family: 'Segoe UI'; color: #e2e8f0; line-height: 1.8;">
<div style="background: linear-gradient(135deg, #22c55e, #16a34a); color: white; padding: 12px; border-radius: 8px; text-align: center; font-size: 14px; font-weight: 600; margin-bottom: 12px;">
{child.get('name', 'غير محدد')}
</div>
<div style="font-size: 12px;">
<p><span style="color: #94a3b8;">الكود:</span> <b>{child.get('code', '-')}</b></p>
<p><span style="color: #94a3b8;">الصف:</span> {child.get('class', '-')}</p>
<p><span style="color: #94a3b8;">المنطقة:</span> {child.get('region', '-')}</p>
<p><span style="color: #94a3b8;">الهاتف:</span> {child.get('موبيل الولد', '-')}</p>
</div>
</div>
"""
        self.info_display.setHtml(details)
    
    def register_child(self, child):
        code = child.get('code', '')
        if not code:
            return
        
        if code in self.registered_codes:
            QMessageBox.warning(self, "تحذير", "تم تسجيل هذا الطفل مسبقاً!")
            return
        
        success = self.db.save_immediate_attendance(code)
        
        if success:
            self.show_child_details(child)
            self.add_to_attendance_table(child)
            self.registered_codes.add(code)
            self.save_current_session()
            
            self.code_input.clear()
            self.name_input.setCurrentIndex(-1)
            self.name_input.setCurrentText("")
            self.current_selected_child = None
            self.code_input.setFocus()
            
            self.update_buttons_state()
            self.update_stats()
            
            QMessageBox.information(self, "تم التسجيل", f"تم تسجيل {child.get('name', '')} بنجاح!")
        else:
            QMessageBox.critical(self, "خطأ", "حدث خطأ أثناء الحفظ!")
    
    def register_by_code(self):
        code = self.code_input.text().strip()
        if not code:
            return
        
        if code in self.registered_codes:
            QMessageBox.warning(self, "تحذير", "تم تسجيل هذا الطفل مسبقاً!")
            return
            
        child = self.db.get_child_by_code(code)
        if child:
            self.current_selected_child = child
            self.register_child(child)
        else:
            self.info_display.setHtml("<div style='color: #ef4444; text-align: center; padding: 20px;'>⚠️ الكود غير موجود</div>")
    
    def add_to_attendance_table(self, child):
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%Y-%m-%d")
        
        self.attendance_table.setSortingEnabled(False)
        row = self.attendance_table.rowCount()
        self.attendance_table.insertRow(row)
        
        self.attendance_table.setItem(row, 0, QTableWidgetItem(child.get('code', '')))
        self.attendance_table.setItem(row, 1, QTableWidgetItem(child.get('name', '')))
        self.attendance_table.setItem(row, 2, QTableWidgetItem(child.get('class', '')))
        self.attendance_table.setItem(row, 3, QTableWidgetItem(time_str))
        self.attendance_table.setItem(row, 4, QTableWidgetItem(date_str))
        
        self.attendance_table.setSortingEnabled(True)
    
    def show_attendance_context_menu(self, position):
        row = self.attendance_table.rowAt(position.y())
        if row >= 0:
            menu = QMenu()
            details_action = QAction("📋 عرض التفاصيل", self)
            details_action.triggered.connect(lambda: self.show_child_details_dialog(row))
            menu.addAction(details_action)
            
            delete_action = QAction("🗑️ حذف", self)
            delete_action.triggered.connect(lambda: self.delete_attendance_row(row))
            menu.addAction(delete_action)
            
            menu.exec_(self.attendance_table.viewport().mapToGlobal(position))
    
    def show_child_details_dialog(self, row):
        try:
            code = self.attendance_table.item(row, 0).text()
            child = self.db.get_child_by_code(code)
            if child:
                dialog = ChildDetailsDialog(child, self)
                dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", str(e))
    
    def delete_attendance_row(self, row):
        try:
            code = self.attendance_table.item(row, 0).text()
            name = self.attendance_table.item(row, 1).text()
            
            reply = QMessageBox.question(self, "تأكيد", f"حذف {name}؟",
                                       QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.db.remove_attendance(code)
                self.attendance_table.removeRow(row)
                self.registered_codes.discard(code)
                self.save_current_session()
                self.update_buttons_state()
                self.update_stats()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", str(e))
    
    def update_buttons_state(self):
        has_records = self.attendance_table.rowCount() > 0
        self.finish_btn.setEnabled(has_records)
        self.clear_btn.setEnabled(has_records)
    
    def finish_session(self):
        if not self.registered_codes:
            QMessageBox.information(self, "معلومة", "لا يوجد أطفال مسجلين")
            return
        
        self.registration_finished.emit()
        QMessageBox.information(self, "تم", f"تم تسجيل {len(self.registered_codes)} طفل")
        self.clear_session()
    
    def clear_session(self):
        self.attendance_table.setRowCount(0)
        self.registered_codes.clear()
        self.info_display.clear()
        self.code_input.clear()
        self.name_input.setCurrentText("")
        self.current_selected_child = None
        self.code_input.setFocus()
        self.update_buttons_state()
        self.update_stats()
        self.clear_session_file()
    
    def refresh_data(self):
        try:
            self.load_children_data()
            self.update_stats()
            QMessageBox.information(self, "تم", "تم تحديث البيانات")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", str(e))

    def search_in_current_session(self, search_text):
        search_text = search_text.strip()
        if not search_text:
            self.search_results_display.clear()
            return
        
        normalized_search = self.normalize_arabic_text(search_text).lower()
        found = []
        
        for code in self.registered_codes:
            child = self.db.get_child_by_code(code)
            if child:
                child_name = self.normalize_arabic_text(child.get('name', '')).lower()
                child_code = str(child.get('code', '')).lower()
                
                if normalized_search in child_name or normalized_search in child_code:
                    found.append(child)
        
        if found:
            html = f"<div style='color: #22c55e; font-weight: 600; margin-bottom: 8px;'>🔍 {len(found)} نتيجة</div>"
            for child in found:
                html += f"<div style='color: #e2e8f0; padding: 4px 0;'>{child.get('name', '')} - {child.get('code', '')}</div>"
            self.search_results_display.setHtml(html)
        else:
            self.search_results_display.setHtml("<div style='color: #94a3b8; text-align: center;'>لا توجد نتائج</div>")

    def clear_session_search(self):
        self.session_search_input.clear()
        self.search_results_display.clear()