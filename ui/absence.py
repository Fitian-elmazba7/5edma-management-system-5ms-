# absence.py - Dashboard Grid Layout for Absence Tracking
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QComboBox, QGroupBox, QPushButton, QMessageBox,
                             QTabWidget, QProgressBar, QSplitter, QFrame,
                             QCheckBox, QScrollArea)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont
from utils.database import DatabaseManager
from utils.excel_handler import ExcelHandler
from datetime import datetime
from .server_assignment_dialog import ServerAssignmentDialog

class AbsenceTab(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.excel_handler = ExcelHandler()
        self.current_absent_children = []
        self.current_date = None
        self.setup_ui()
        self.load_dates()
        
    def setup_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(24, 24, 24, 24)
        
        # ═══════════════════════════════════════════════════════════════
        # LEFT PANEL: Controls & Stats
        # ═══════════════════════════════════════════════════════════════
        left_panel = QFrame()
        left_panel.setProperty("class", "dashboard-card")
        left_panel.setFixedWidth(320)
        # Header
        header_widget = QWidget()
        header = QHBoxLayout(header_widget)
        header_icon = QLabel("𓃻")
        header_icon.setProperty("class", "card-icon")
        header_title = QLabel("متابعة الغياب")
        header_title.setProperty("class", "card-title")
        header.addWidget(header_icon)
        header.addWidget(header_title)
        header.addStretch()
        
        # Scroll Area for the rest of the controls
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(16)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        
        # Move controls into scroll_layout instead of left_layout
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.addWidget(header_widget)
        
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setProperty("class", "card-separator")
        scroll_layout.addWidget(sep)
        
        # Date Selection
        date_section = QLabel("📅 اختر التاريخ")
        date_section.setProperty("class", "input-label")
        scroll_layout.addWidget(date_section)
        
        self.date_selector = QComboBox()
        self.date_selector.setProperty("class", "dashboard-combo")
        self.date_selector.setMinimumHeight(40)
        self.date_selector.currentTextChanged.connect(self.load_absence_data)
        scroll_layout.addWidget(self.date_selector)
        
        self.date_info_label = QLabel("")
        self.date_info_label.setProperty("class", "stat-subtitle")
        scroll_layout.addWidget(self.date_info_label)
        
        self.service_days_only = QCheckBox("عرض أيام الخدمة فقط")
        self.service_days_only.stateChanged.connect(self.load_dates)
        scroll_layout.addWidget(self.service_days_only)
        
        # Stats Section
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        sep2.setProperty("class", "card-separator")
        scroll_layout.addWidget(sep2)
        
        stats_label = QLabel("📊 الإحصائيات")
        stats_label.setProperty("class", "input-label")
        scroll_layout.addWidget(stats_label)
        
        # Stats Cards Grid
        stats_grid_layout = QVBoxLayout()
        stats_grid_layout.setSpacing(8)
        
        self.total_label = self.create_stat_row("👥 إجمالي الأطفال", "0")
        self.absent_label = self.create_stat_row("❌ الغياب الكلي", "0")
        self.attendance_rate_label = self.create_stat_row("✅ نسبة الحضور", "0%")
        self.class1_label = self.create_stat_row("📚 الصف الأول", "0")
        self.class2_label = self.create_stat_row("📚 الصف الثاني", "0")
        self.class3_label = self.create_stat_row("📚 الصف الثالث", "0")
        
        stats_grid_layout.addWidget(self.total_label)
        stats_grid_layout.addWidget(self.absent_label)
        stats_grid_layout.addWidget(self.attendance_rate_label)
        stats_grid_layout.addWidget(self.class1_label)
        stats_grid_layout.addWidget(self.class2_label)
        stats_grid_layout.addWidget(self.class3_label)
        scroll_layout.addLayout(stats_grid_layout)
        
        # Action Buttons
        sep3 = QFrame()
        sep3.setFrameShape(QFrame.HLine)
        sep3.setProperty("class", "card-separator")
        scroll_layout.addWidget(sep3)
        
        self.server_assignment_btn = QPushButton("👥 توزيع على الخدام")
        self.server_assignment_btn.setProperty("class", "btn-purple")
        self.server_assignment_btn.setMinimumHeight(40)
        self.server_assignment_btn.clicked.connect(self.open_server_assignment)
        self.server_assignment_btn.setEnabled(False)
        scroll_layout.addWidget(self.server_assignment_btn)
        
        self.refresh_btn = QPushButton("🔄 تحديث")
        self.refresh_btn.setProperty("class", "btn-secondary")
        self.refresh_btn.setMinimumHeight(40)
        self.refresh_btn.clicked.connect(self.refresh_data)
        scroll_layout.addWidget(self.refresh_btn)
        
        # Export buttons
        export_label = QLabel("📤 تصدير التقارير")
        export_label.setProperty("class", "input-label")
        scroll_layout.addWidget(export_label)
        
        self.export_all_btn = QPushButton("تصدير الكل")
        self.export_all_btn.setProperty("class", "btn-success")
        self.export_all_btn.clicked.connect(self.export_all_absence)
        scroll_layout.addWidget(self.export_all_btn)
        
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_content)
        left_layout.addWidget(scroll)
        
        main_layout.addWidget(left_panel)
        
        # ═══════════════════════════════════════════════════════════════
        # RIGHT PANEL: Tables
        # ═══════════════════════════════════════════════════════════════
        right_panel = QFrame()
        right_panel.setProperty("class", "dashboard-card")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(12)
        right_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        table_header = QHBoxLayout()
        table_icon = QLabel("📊")
        table_icon.setProperty("class", "card-icon")
        table_title = QLabel("قوائم الغياب")
        table_title.setProperty("class", "card-title")
        table_header.addWidget(table_icon)
        table_header.addWidget(table_title)
        table_header.addStretch()
        right_layout.addLayout(table_header)
        
        sep4 = QFrame()
        sep4.setFrameShape(QFrame.HLine)
        sep4.setProperty("class", "card-separator")
        right_layout.addWidget(sep4)
        
        # Tabs
        self.tabs = QTabWidget()
        
        self.all_absence_tab = QWidget()
        self.class1_tab = QWidget()
        self.class2_tab = QWidget()
        self.class3_tab = QWidget()
        
        self.tabs.addTab(self.all_absence_tab, "الغياب الكلي")
        self.tabs.addTab(self.class1_tab, "الصف الأول")
        self.tabs.addTab(self.class2_tab, "الصف الثاني")
        self.tabs.addTab(self.class3_tab, "الصف الثالث")
        
        self.setup_absence_table(self.all_absence_tab, "الكل")
        self.setup_absence_table(self.class1_tab, "الصف الأول")
        self.setup_absence_table(self.class2_tab, "الصف الثاني")
        self.setup_absence_table(self.class3_tab, "الصف الثالث")
        
        right_layout.addWidget(self.tabs, 1)
        
        main_layout.addWidget(right_panel, 1)
        self.setLayout(main_layout)
    
    def create_stat_row(self, label, value):
        """Create a stat row widget"""
        frame = QFrame()
        frame.setStyleSheet("background: #0f0f1a; border-radius: 6px; padding: 8px;")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 8, 10, 8)
        
        lbl = QLabel(label)
        lbl.setProperty("class", "stat-subtitle")
        
        val = QLabel(value)
        val.setStyleSheet("font-weight: 600; color: #e2e8f0;")
        
        layout.addWidget(lbl)
        layout.addStretch()
        layout.addWidget(val)
        
        return frame
    
    def update_stat_row(self, frame, value):
        """Update stat row value"""
        labels = frame.findChildren(QLabel)
        if len(labels) >= 2:
            labels[1].setText(str(value))
    
    def setup_absence_table(self, tab, class_name):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        table = QTableWidget()
        table.setObjectName(f"table_{class_name}")
        table.setProperty("class", "dashboard-table")
        
        table.setColumnCount(10)
        table.setHorizontalHeaderLabels([
            "الكود", "الاسم", "العمارة", "الشارع", "الدور", "الشقة",
            "موبيل الولد", "موبايل الأب", "موبايل الأم", "تليفون"
        ])
        
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(True)
        
        layout.addWidget(table)
        tab.setLayout(layout)
    
    def load_dates(self):
        try:
            dates_info = self.db.get_attendance_dates_with_info()
            
            if self.service_days_only.isChecked():
                dates_info = [d for d in dates_info if d['is_service_day']]
            
            self.date_selector.clear()
            for date_info in dates_info:
                self.date_selector.addItem(date_info['display'], date_info['date'])
            
            if dates_info:
                self.date_selector.setCurrentIndex(0)
                self.update_date_info(dates_info[0])
            else:
                self.date_info_label.setText("لا توجد تواريخ")
                
        except Exception as e:
            QMessageBox.warning(self, "تحذير", f"خطأ: {str(e)}")
    
    def update_date_info(self, date_info):
        info = f"{date_info['day_name']}"
        if date_info['is_service_day']:
            info += " ✅"
        self.date_info_label.setText(info)
    
    def load_absence_data(self):
        try:
            if self.date_selector.currentIndex() < 0:
                return
                
            selected_date = self.date_selector.currentData()
            if not selected_date:
                selected_date = self.date_selector.currentText().split(' ')[0]
            
            self.current_date = selected_date
            
            date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
            day_name = date_obj.strftime("%A")
            arabic_day = self.db.arabic_days.get(day_name, day_name)
            settings = self.db.get_settings()
            is_service_day = (day_name == settings.get('service_day', 'Thursday'))
            
            self.update_date_info({
                'date': selected_date,
                'day_name': arabic_day,
                'is_service_day': is_service_day
            })
            
            self.current_absent_children = self.db.get_absent_children(selected_date)
            self.server_assignment_btn.setEnabled(len(self.current_absent_children) > 0)
            
            class1 = [c for c in self.current_absent_children if c.get('class') == 'الصف الأول']
            class2 = [c for c in self.current_absent_children if c.get('class') == 'الصف الثاني']
            class3 = [c for c in self.current_absent_children if c.get('class') == 'الصف الثالث']
            
            self.update_absence_table('الكل', self.current_absent_children)
            self.update_absence_table('الصف الأول', class1)
            self.update_absence_table('الصف الثاني', class2)
            self.update_absence_table('الصف الثالث', class3)
            
            self.update_stats(selected_date)
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ: {str(e)}")
    
    def update_absence_table(self, class_name, children):
        try:
            table = self.findChild(QTableWidget, f"table_{class_name}")
            if table:
                table.setSortingEnabled(False)
                table.setRowCount(0)
                
                for child in children:
                    row = table.rowCount()
                    table.insertRow(row)
                    
                    table.setItem(row, 0, QTableWidgetItem(str(child.get('code', '-'))))
                    table.setItem(row, 1, QTableWidgetItem(child.get('name', '-')))
                    table.setItem(row, 2, QTableWidgetItem(str(child.get('عماره', '-'))))
                    table.setItem(row, 3, QTableWidgetItem(child.get('شارع', '-')))
                    table.setItem(row, 4, QTableWidgetItem(str(child.get('دور', '-'))))
                    table.setItem(row, 5, QTableWidgetItem(str(child.get('شقه', '-'))))
                    table.setItem(row, 6, QTableWidgetItem(child.get('موبيل الولد', '-')))
                    table.setItem(row, 7, QTableWidgetItem(child.get('موبايل الاب', '-')))
                    table.setItem(row, 8, QTableWidgetItem(child.get('موبايل الام', '-')))
                    table.setItem(row, 9, QTableWidgetItem(child.get('تليفون', '-')))
                
                table.setSortingEnabled(True)
                
                if not children:
                    table.setRowCount(1)
                    table.setItem(0, 0, QTableWidgetItem("🎉 لا يوجد غياب"))
                    table.setSpan(0, 0, 1, 10)
                    
        except Exception as e:
            print(f"Error: {e}")
    
    def update_stats(self, date):
        try:
            stats = self.db.get_attendance_stats_by_date(date)
            if not stats:
                return
            
            self.update_stat_row(self.total_label, stats['total'])
            self.update_stat_row(self.absent_label, stats['absent'])
            self.update_stat_row(self.attendance_rate_label, f"{stats['attendance_rate']:.0f}%")
            
            classes = stats.get('classes', {})
            self.update_stat_row(self.class1_label, classes.get('الصف الأول', {}).get('absent', 0))
            self.update_stat_row(self.class2_label, classes.get('الصف الثاني', {}).get('absent', 0))
            self.update_stat_row(self.class3_label, classes.get('الصف الثالث', {}).get('absent', 0))
            
        except Exception as e:
            print(f"Error: {e}")
    
    def refresh_data(self):
        self.load_dates()
        if self.date_selector.currentIndex() >= 0:
            self.load_absence_data()
        QMessageBox.information(self, "تم", "تم التحديث")
    
    def export_all_absence(self):
        if not self.current_absent_children:
            QMessageBox.information(self, "معلومة", "لا توجد بيانات")
            return
        
        try:
            from PyQt5.QtWidgets import QFileDialog
            selected_date = self.date_selector.currentData()
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, "حفظ التقرير", 
                f"غياب_{selected_date}.xlsx", 
                "Excel (*.xlsx)"
            )
            
            if file_path:
                self.excel_handler.export_absence_report(
                    self.current_absent_children, file_path, selected_date, "الغياب الكلي"
                )
                QMessageBox.information(self, "تم", "تم التصدير")
                
        except Exception as e:
            QMessageBox.critical(self, "خطأ", str(e))
    
    def export_class_absence(self, class_name):
        children = [c for c in self.current_absent_children if c.get('class') == class_name]
        
        if not children:
            QMessageBox.information(self, "معلومة", f"لا توجد بيانات لـ{class_name}")
            return
        
        try:
            from PyQt5.QtWidgets import QFileDialog
            selected_date = self.date_selector.currentData()
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, f"حفظ تقرير {class_name}", 
                f"غياب_{class_name}_{selected_date}.xlsx", 
                "Excel (*.xlsx)"
            )
            
            if file_path:
                self.excel_handler.export_absence_report(children, file_path, selected_date, class_name)
                QMessageBox.information(self, "تم", "تم التصدير")
                
        except Exception as e:
            QMessageBox.critical(self, "خطأ", str(e))
    
    def open_server_assignment(self):
        if not self.current_absent_children:
            QMessageBox.information(self, "معلومة", "لا توجد أطفال غائبين")
            return
        
        if not self.current_date:
            QMessageBox.warning(self, "تحذير", "لم يتم تحديد تاريخ")
            return
        
        try:
            dialog = ServerAssignmentDialog(self.current_absent_children, self.current_date, self)
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", str(e))