from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QComboBox, QGroupBox, QPushButton, QMessageBox,
                             QTabWidget, QProgressBar, QSplitter,
                             QCheckBox)
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
        
        # Splitter لتقسيم الشاشة
        splitter = QSplitter(Qt.Horizontal)
        
        # اللوحة اليسرى: التحكم والإحصائيات
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # عنوان القسم
        title_label = QLabel("𓃻 نظام متابعة الغياب")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setProperty("class", "page-title")

        
        # مجموعة التحكم
        control_group = QGroupBox("إعدادات التقرير")
        control_layout = QVBoxLayout()
        
        # خيار عرض أيام الخدمة فقط
        self.service_days_only = QCheckBox("عرض أيام الخدمة فقط")
        self.service_days_only.stateChanged.connect(self.load_dates)
        
        control_layout.addWidget(self.service_days_only)
        
        # زر توزيع المتابعة على الخدام
        self.server_assignment_btn = QPushButton("👥 توزيع المتابعة على الخدام")
        self.server_assignment_btn.setProperty("class", "btn-purple")

        self.server_assignment_btn.clicked.connect(self.open_server_assignment)
        self.server_assignment_btn.setEnabled(False)  # Initially disabled
        
        control_layout.addWidget(self.server_assignment_btn)
        control_layout.addWidget(QLabel("اختر تاريخ الخدمة:"))
        self.date_selector = QComboBox()
        self.date_selector.currentTextChanged.connect(self.load_absence_data)
        
        # معلومات التاريخ المحدد
        self.date_info_label = QLabel("")
        self.date_info_label.setProperty("class", "info-label")

        
        self.refresh_btn = QPushButton("تحديث البيانات")
        self.refresh_btn.clicked.connect(self.refresh_data)
        
        control_layout.addWidget(self.date_selector)
        control_layout.addWidget(self.date_info_label)
        control_layout.addWidget(self.refresh_btn)
        
        control_group.setLayout(control_layout)
        
        # الإحصائيات
        stats_group = QGroupBox("الإحصائيات الفورية")
        stats_layout = QVBoxLayout()
        
        self.total_label = QLabel("إجمالي الأطفال: 0")
        self.absent_label = QLabel("الغياب الكلي: 0")
        self.attendance_rate_label = QLabel("نسبة الحضور: 0%")
        self.class1_label = QLabel("الصف الأول: 0")
        self.class2_label = QLabel("الصف الثاني: 0") 
        self.class3_label = QLabel("الصف الثالث: 0")
        
        for label in [self.total_label, self.absent_label, self.attendance_rate_label, 
                     self.class1_label, self.class2_label, self.class3_label]:
            label.setStyleSheet("QLabel { font-weight: bold; padding: 5px; }")
            stats_layout.addWidget(label)
        
        stats_group.setLayout(stats_layout)
        
        # أزرار التصدير
        export_group = QGroupBox("تصدير التقارير")
        export_layout = QVBoxLayout()
        
        self.export_all_btn = QPushButton("تصدير الغياب الكلي")
        self.export_all_btn.clicked.connect(self.export_all_absence)
        
        self.export_class1_btn = QPushButton("تصدير غياب الصف الأول")
        self.export_class1_btn.clicked.connect(lambda: self.export_class_absence('الصف الأول'))
        
        self.export_class2_btn = QPushButton("تصدير غياب الصف الثاني")
        self.export_class2_btn.clicked.connect(lambda: self.export_class_absence('الصف الثاني'))
        
        self.export_class3_btn = QPushButton("تصدير غياب الصف الثالث")
        self.export_class3_btn.clicked.connect(lambda: self.export_class_absence('الصف الثالث'))
        
        export_layout.addWidget(self.export_all_btn)
        export_layout.addWidget(self.export_class1_btn)
        export_layout.addWidget(self.export_class2_btn)
        export_layout.addWidget(self.export_class3_btn)
        export_group.setLayout(export_layout)
        
        left_layout.addWidget(title_label)
        left_layout.addWidget(control_group)
        left_layout.addWidget(stats_group)
        left_layout.addWidget(export_group)
        left_layout.addStretch()
        
        left_panel.setLayout(left_layout)
        
        # اللوحة اليمنى: عرض البيانات
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        # تبويبات للفصول
        self.tabs = QTabWidget()
        
        self.all_absence_tab = QWidget()
        self.class1_tab = QWidget()
        self.class2_tab = QWidget()
        self.class3_tab = QWidget()
        
        self.tabs.addTab(self.all_absence_tab, "الغياب الكلي")
        self.tabs.addTab(self.class1_tab, "الصف الأول")
        self.tabs.addTab(self.class2_tab, "الصف الثاني")
        self.tabs.addTab(self.class3_tab, "الصف الثالث")
        
        # إعداد الجداول
        self.setup_absence_table(self.all_absence_tab, "الكل")
        self.setup_absence_table(self.class1_tab, "الصف الأول")
        self.setup_absence_table(self.class2_tab, "الصف الثاني")
        self.setup_absence_table(self.class3_tab, "الصف الثالث")
        
        right_layout.addWidget(self.tabs)
        right_panel.setLayout(right_layout)
        
        # إضافة اللوحات إلى splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([350, 650])
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
    
    def setup_absence_table(self, tab, class_name):
        layout = QVBoxLayout()
        
        table = QTableWidget()
        table.setObjectName(f"table_{class_name}")
        
        # الأعمدة الأساسية المطلوبة
        table.setColumnCount(10)
        table.setHorizontalHeaderLabels([
            "الكود", "الاسم", "العمارة", "الشارع", "الدور", "الشقة",
            "موبيل الولد", "موبايل الأب", "موبايل الأم", "تليفون"
        ])
        
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(True)
        
        # ضبط أبعاد الأعمدة
        table.setColumnWidth(0, 80)   # الكود
        table.setColumnWidth(1, 150)  # الاسم
        table.setColumnWidth(2, 80)   # العمارة
        table.setColumnWidth(3, 150)  # الشارع
        table.setColumnWidth(4, 60)   # الدور
        table.setColumnWidth(5, 60)   # الشقة
        table.setColumnWidth(6, 100)  # موبيل الولد
        table.setColumnWidth(7, 100)  # موبايل الأب
        table.setColumnWidth(8, 100)  # موبايل الأم
        table.setColumnWidth(9, 100)  # تليفون
        
        layout.addWidget(QLabel(f"قائمة الغياب - {class_name}"))
        layout.addWidget(table)
        
        tab.setLayout(layout)
    
    def load_dates(self):
        """تحميل تواريخ الحضور المسجلة فقط"""
        try:
            dates_info = self.db.get_attendance_dates_with_info()
            
            # إذا كان مختار "أيام الخدمة فقط"
            if self.service_days_only.isChecked():
                dates_info = [date for date in dates_info if date['is_service_day']]
            
            self.date_selector.clear()
            for date_info in dates_info:
                self.date_selector.addItem(date_info['display'], date_info['date'])
            
            if dates_info:
                self.date_selector.setCurrentIndex(0)
                self.update_date_info(dates_info[0])
            else:
                self.date_info_label.setText("لا توجد تواريخ مسجلة")
                
        except Exception as e:
            QMessageBox.warning(self, "تحذير", f"خطأ في تحميل التواريخ: {str(e)}")
    
    def update_date_info(self, date_info):
        """تحديث معلومات التاريخ المحدد"""
        info_text = f"التاريخ: {date_info['date']} | اليوم: {date_info['day_name']}"
        if date_info['is_service_day']:
            info_text += " | ✅ يوم الخدمة"
        else:
            info_text += " | ⚠️ ليس يوم خدمة"
        
        self.date_info_label.setText(info_text)
    
    def load_absence_data(self):
        try:
            if self.date_selector.currentIndex() < 0:
                return
                
            selected_date = self.date_selector.currentData()
            if not selected_date:
                display_text = self.date_selector.currentText()
                selected_date = display_text.split(' ')[0]
            
            self.current_date = selected_date
            
            # تحديث معلومات التاريخ
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
            
            # الحصول على الأطفال الغائبين
            self.current_absent_children = self.db.get_absent_children(selected_date)
            
            # تفعيل زر توزيع المتابعة إذا كان هناك غياب
            self.server_assignment_btn.setEnabled(len(self.current_absent_children) > 0)
            
            # فصل الأطفال حسب الصفوف
            class1_children = [child for child in self.current_absent_children if child.get('class') == 'الصف الأول']
            class2_children = [child for child in self.current_absent_children if child.get('class') == 'الصف الثاني']
            class3_children = [child for child in self.current_absent_children if child.get('class') == 'الصف الثالث']
            
            # تحديث الجداول
            self.update_absence_table('الكل', self.current_absent_children)
            self.update_absence_table('الصف الأول', class1_children)
            self.update_absence_table('الصف الثاني', class2_children)
            self.update_absence_table('الصف الثالث', class3_children)
            
            # تحديث الإحصائيات
            self.update_stats(selected_date)
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في تحميل بيانات الغياب: {str(e)}")
    
    def update_absence_table(self, class_name, children):
        try:
            table = self.findChild(QTableWidget, f"table_{class_name}")
            if table:
                table.setSortingEnabled(False)
                table.setRowCount(0)
                
                for child in children:
                    row = table.rowCount()
                    table.insertRow(row)
                    
                    table.setItem(row, 0, QTableWidgetItem(str(child.get('code', 'غير محدد'))))
                    table.setItem(row, 1, QTableWidgetItem(child.get('name', 'غير محدد')))
                    table.setItem(row, 2, QTableWidgetItem(str(child.get('عماره', 'غير محدد'))))
                    table.setItem(row, 3, QTableWidgetItem(child.get('شارع', 'غير محدد')))
                    table.setItem(row, 4, QTableWidgetItem(str(child.get('دور', 'غير محدد'))))
                    table.setItem(row, 5, QTableWidgetItem(str(child.get('شقه', 'غير محدد'))))
                    table.setItem(row, 6, QTableWidgetItem(child.get('موبيل الولد', 'غير محدد')))
                    table.setItem(row, 7, QTableWidgetItem(child.get('موبايل الاب', 'غير محدد')))
                    table.setItem(row, 8, QTableWidgetItem(child.get('موبايل الام', 'غير محدد')))
                    table.setItem(row, 9, QTableWidgetItem(child.get('تليفون', 'غير محدد')))
                
                table.setSortingEnabled(True)
                
                if len(children) == 0:
                    table.setRowCount(1)
                    table.setItem(0, 0, QTableWidgetItem("🎉 لا يوجد غياب لهذا اليوم - جميع الأطفال حاضروا"))
                    table.setSpan(0, 0, 1, 10)
                    
        except Exception as e:
            print(f"Error updating table for {class_name}: {str(e)}")
    
    def update_stats(self, date):
        try:
            stats = self.db.get_attendance_stats_by_date(date)
            if not stats:
                # إذا لم تكن هناك إحصائيات لهذا التاريخ
                self.total_label.setText("إجمالي الأطفال: 0")
                self.absent_label.setText("الغياب الكلي: 0")
                self.attendance_rate_label.setText("نسبة الحضور: 0%")
                self.class1_label.setText("الصف الأول: 0")
                self.class2_label.setText("الصف الثاني: 0")
                self.class3_label.setText("الصف الثالث: 0")
                return
            
            self.total_label.setText(f"إجمالي الأطفال: {stats['total']}")
            self.absent_label.setText(f"الغياب الكلي: {stats['absent']}")
            self.attendance_rate_label.setText(f"نسبة الحضور: {stats['attendance_rate']:.1f}%")
            
            class_stats = stats.get('classes', {})
            self.class1_label.setText(f"الصف الأول: غائب {class_stats.get('الصف الأول', {}).get('absent', 0)}")
            self.class2_label.setText(f"الصف الثاني: غائب {class_stats.get('الصف الثاني', {}).get('absent', 0)}")
            self.class3_label.setText(f"الصف الثالث: غائب {class_stats.get('الصف الثالث', {}).get('absent', 0)}")
            
        except Exception as e:
            print(f"Error updating stats: {str(e)}")
    
    def refresh_data(self):
        """تحديث البيانات"""
        self.load_dates()
        if self.date_selector.currentIndex() >= 0:
            self.load_absence_data()
        QMessageBox.information(self, "تم التحديث", "تم تحديث بيانات الغياب بنجاح")
    
    def export_all_absence(self):
        if not self.current_absent_children:
            QMessageBox.information(self, "معلومة", "لا توجد بيانات غياب للتصدير")
            return
        
        try:
            from PyQt5.QtWidgets import QFileDialog
            selected_date = self.date_selector.currentData()
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, "حفظ تقرير الغياب الكلي", 
                f"تقرير_غياب_كامل_{selected_date}.xlsx", 
                "Excel Files (*.xlsx)"
            )
            
            if file_path:
                self.excel_handler.export_absence_report(
                    self.current_absent_children, 
                    file_path, 
                    selected_date,
                    "الغياب الكلي"
                )
                QMessageBox.information(self, "تم التصدير", "تم تصدير تقرير الغياب الكلي بنجاح")
                
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في التصدير: {str(e)}")
    
    def export_class_absence(self, class_name):
        class_children = [child for child in self.current_absent_children if child.get('class') == class_name]
        
        if not class_children:
            QMessageBox.information(self, "معلومة", f"لا توجد بيانات غياب للصف {class_name}")
            return
        
        try:
            from PyQt5.QtWidgets import QFileDialog
            selected_date = self.date_selector.currentData()
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, f"حفظ تقرير غياب {class_name}", 
                f"تقرير_غياب_{class_name}_{selected_date}.xlsx", 
                "Excel Files (*.xlsx)"
            )
            
            if file_path:
                self.excel_handler.export_absence_report(
                    class_children, 
                    file_path, 
                    selected_date,
                    f"غياب {class_name}"
                )
                QMessageBox.information(self, "تم التصدير", f"تم تصدير تقرير غياب {class_name} بنجاح")
                
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في التصدير: {str(e)}")
    
    def open_server_assignment(self):
        """فتح نافذة توزيع المتابعة على الخدام"""
        if not self.current_absent_children:
            QMessageBox.information(self, "معلومة", "لا توجد أطفال غائبين لهذا اليوم.")
            return
        
        if not self.current_date:
            QMessageBox.warning(self, "تحذير", "لم يتم تحديد تاريخ.")
            return
        
        try:
            dialog = ServerAssignmentDialog(self.current_absent_children, self.current_date, self)
            dialog.exec_()
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء فتح نافذة التوزيع: {str(e)}")