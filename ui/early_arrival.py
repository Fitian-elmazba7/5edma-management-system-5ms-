from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QComboBox, QGroupBox, QPushButton, QMessageBox,
                             QSplitter, QFrame, QRadioButton,
                             QButtonGroup, QSpinBox, QDialog, QFormLayout,
                             QDialogButtonBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from utils.database import DatabaseManager
from utils.excel_handler import ExcelHandler
from datetime import datetime

class ServiceSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("إعدادات وقت الخدمة")
        self.setModal(True)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        # يوم الخدمة
        self.day_combo = QComboBox()
        self.day_combo.addItems(["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        form_layout.addRow("يوم الخدمة:", self.day_combo)
        
        # وقت الخدمة
        time_layout = QHBoxLayout()
        
        self.hours_spin = QSpinBox()
        self.hours_spin.setRange(1, 12)
        self.hours_spin.setValue(7)
        
        self.minutes_spin = QSpinBox()
        self.minutes_spin.setRange(0, 59)
        self.minutes_spin.setValue(0)
        
        self.ampm_group = QButtonGroup()
        self.am_radio = QRadioButton("AM")
        self.pm_radio = QRadioButton("PM")
        self.pm_radio.setChecked(True)
        self.ampm_group.addButton(self.am_radio)
        self.ampm_group.addButton(self.pm_radio)
        
        time_layout.addWidget(QLabel("الساعة:"))
        time_layout.addWidget(self.hours_spin)
        time_layout.addWidget(QLabel("الدقائق:"))
        time_layout.addWidget(self.minutes_spin)
        time_layout.addWidget(self.am_radio)
        time_layout.addWidget(self.pm_radio)
        time_layout.addStretch()
        
        form_layout.addRow("وقت الخدمة:", time_layout)
        
        layout.addLayout(form_layout)
        
        # أزرار
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def get_settings(self):
        day = self.day_combo.currentText()
        hours = self.hours_spin.value()
        minutes = self.minutes_spin.value()
        is_pm = self.pm_radio.isChecked()
        
        # تحويل إلى تنسيق 24 ساعة
        if is_pm and hours < 12:
            hours += 12
        elif not is_pm and hours == 12:
            hours = 0
        
        time_24h = f"{hours:02d}:{minutes:02d}"
        return day, time_24h
    
    def set_current_settings(self, day, time_24h):
        """تعيين الإعدادات الحالية"""
        # تعيين اليوم
        index = self.day_combo.findText(day)
        if index >= 0:
            self.day_combo.setCurrentIndex(index)
        
        # تحليل الوقت
        try:
            hours, minutes = map(int, time_24h.split(':'))
            is_pm = hours >= 12
            
            # تحويل إلى 12 ساعة
            if hours > 12:
                hours -= 12
            elif hours == 0:
                hours = 12
            
            self.hours_spin.setValue(hours)
            self.minutes_spin.setValue(minutes)
            
            if is_pm:
                self.pm_radio.setChecked(True)
            else:
                self.am_radio.setChecked(True)
        except:
            pass

class EarlyArrivalTab(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.excel_handler = ExcelHandler()
        self.setup_ui()
        self.load_dates()
        
    def setup_ui(self):
        main_layout = QHBoxLayout()
        
        # Splitter لتقسيم الشاشة
        splitter = QSplitter(Qt.Horizontal)
        
        # اللوحة اليسرى: التحكم
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # عنوان القسم
        title_label = QLabel("𓃷 مكافأة الحضور المبكر")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setProperty("class", "page-title")

        
        # مجموعة الإعدادات
        settings_group = QGroupBox("🕒 إعدادات التقرير")
        settings_layout = QVBoxLayout()
        
        # اختيار التاريخ
        settings_layout.addWidget(QLabel("📅 اختر تاريخ الخدمة:"))
        self.date_selector = QComboBox()
        self.date_selector.currentTextChanged.connect(self.load_early_arrivals)
        settings_layout.addWidget(self.date_selector)
        
        # إعدادات الوقت مع AM/PM
        time_settings_frame = QFrame()
        time_settings_layout = QHBoxLayout()
        
        # الساعات
        hours_layout = QVBoxLayout()
        hours_layout.addWidget(QLabel("الساعات:"))
        self.hours_spin = QSpinBox()
        self.hours_spin.setRange(1, 12)
        self.hours_spin.setValue(6)  # قبل الخدمة بساعة
        self.hours_spin.valueChanged.connect(self.load_early_arrivals)
        hours_layout.addWidget(self.hours_spin)
        
        # الدقائق
        minutes_layout = QVBoxLayout()
        minutes_layout.addWidget(QLabel("الدقائق:"))
        self.minutes_spin = QSpinBox()
        self.minutes_spin.setRange(0, 59)
        self.minutes_spin.setValue(30)  # قبل الخدمة بنصف ساعة
        self.minutes_spin.valueChanged.connect(self.load_early_arrivals)
        minutes_layout.addWidget(self.minutes_spin)
        
        # AM/PM
        ampm_layout = QVBoxLayout()
        ampm_layout.addWidget(QLabel("الفترة:"))
        self.ampm_group = QButtonGroup()
        self.am_radio = QRadioButton("AM")
        self.pm_radio = QRadioButton("PM")
        self.pm_radio.setChecked(True)
        self.ampm_group.addButton(self.am_radio)
        self.ampm_group.addButton(self.pm_radio)
        self.am_radio.toggled.connect(self.load_early_arrivals)
        self.pm_radio.toggled.connect(self.load_early_arrivals)
        
        ampm_layout.addWidget(self.am_radio)
        ampm_layout.addWidget(self.pm_radio)
        
        time_settings_layout.addLayout(hours_layout)
        time_settings_layout.addLayout(minutes_layout)
        time_settings_layout.addLayout(ampm_layout)
        time_settings_frame.setLayout(time_settings_layout)
        
        settings_layout.addWidget(QLabel("⏰ الوقت المحدد للحضور المبكر:"))
        settings_layout.addWidget(time_settings_frame)
        
        # وقت الخدمة الرسمي
        service_time_layout = QHBoxLayout()
        service_time_layout.addWidget(QLabel("⛪ وقت الخدمة الرسمي:"))
        self.service_time_label = QLabel("07:00 PM - الخميس")
        self.service_time_label.setProperty("class", "info-label")

        
        self.change_service_btn = QPushButton("تغيير الإعدادات")
        self.change_service_btn.clicked.connect(self.change_service_settings)
        
        service_time_layout.addWidget(self.service_time_label)
        service_time_layout.addWidget(self.change_service_btn)
        service_time_layout.addStretch()
        
        settings_layout.addLayout(service_time_layout)
        
        # أزرار التحكم
        button_layout = QHBoxLayout()
        self.filter_btn = QPushButton("🔍 تصفية الحضور المبكر")
        self.filter_btn.clicked.connect(self.load_early_arrivals)
        
        self.export_btn = QPushButton("📊 تصدير التقرير")
        self.export_btn.clicked.connect(self.export_early_arrivals)
        
        self.refresh_btn = QPushButton("🔄 تحديث البيانات")
        self.refresh_btn.clicked.connect(self.refresh_data)
        
        button_layout.addWidget(self.filter_btn)
        button_layout.addWidget(self.export_btn)
        button_layout.addWidget(self.refresh_btn)
        
        settings_layout.addLayout(button_layout)
        
        settings_group.setLayout(settings_layout)
        
        # الإحصائيات
        stats_group = QGroupBox("📈 الإحصائيات")
        stats_layout = QVBoxLayout()
        
        self.total_attendance_label = QLabel("👥 إجمالي الحضور: 0")
        self.early_arrival_label = QLabel("✅ الحضور المبكر: 0")
        self.percentage_label = QLabel("📊 النسبة: 0%")
        self.avg_arrival_label = QLabel("⏱️ متوسط الوقت: --:--")
        
        for label in [self.total_attendance_label, self.early_arrival_label, 
                     self.percentage_label, self.avg_arrival_label]:
            label.setProperty("class", "info-label")

            stats_layout.addWidget(label)
        
        stats_group.setLayout(stats_layout)
        
        left_layout.addWidget(title_label)
        left_layout.addWidget(settings_group)
        left_layout.addWidget(stats_group)
        left_layout.addStretch()
        
        left_panel.setLayout(left_layout)
        
        # اللوحة اليمنى: عرض البيانات
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        # معلومات التصفية
        self.filter_info_label = QLabel("⚡ الأطفال الذين حضروا قبل الساعة: --:--")
        self.filter_info_label.setProperty("class", "info-label")

        right_layout.addWidget(self.filter_info_label)
        
        # جدول الحضور المبكر
        self.early_arrival_table = QTableWidget()
        self.early_arrival_table.setColumnCount(7)
        self.early_arrival_table.setHorizontalHeaderLabels([
            "الكود", "الاسم", "الصف", "الوقت", "نظام الوقت", "التاريخ", "الحالة"
        ])
        self.early_arrival_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.early_arrival_table.setSortingEnabled(True)
        
        # ضبط أبعاد الأعمدة
        self.early_arrival_table.setColumnWidth(0, 80)   # الكود
        self.early_arrival_table.setColumnWidth(1, 150)  # الاسم
        self.early_arrival_table.setColumnWidth(2, 100)  # الصف
        self.early_arrival_table.setColumnWidth(3, 80)   # الوقت
        self.early_arrival_table.setColumnWidth(4, 100)  # نظام الوقت
        self.early_arrival_table.setColumnWidth(5, 100)  # التاريخ
        self.early_arrival_table.setColumnWidth(6, 120)  # الحالة
        
        right_layout.addWidget(self.early_arrival_table)
        
        right_panel.setLayout(right_layout)
        
        # إضافة اللوحات إلى splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 600])
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
        
        # تحميل وقت الخدمة الرسمي
        self.load_service_time()
    
    def load_service_time(self):
        """تحميل وقت الخدمة الرسمي من الإعدادات"""
        settings = self.db.get_settings()
        service_time = settings.get('service_time', '19:00')
        service_day_english = settings.get('service_day', 'Thursday')
        service_day_arabic = self.db.arabic_days.get(service_day_english, service_day_english)
        
        # تحويل الوقت إلى 12 ساعة للعرض
        service_time_12h = self.convert_to_12h(service_time)
        self.service_time_label.setText(f"{service_time_12h} - {service_day_arabic}")
    
    def change_service_settings(self):
        """فتح نافذة تعديل إعدادات الخدمة"""
        dialog = ServiceSettingsDialog(self)
        settings = self.db.get_settings()
        
        # تعيين القيم الحالية
        current_day = settings.get('service_day', 'Thursday')
        current_time = settings.get('service_time', '19:00')
        dialog.set_current_settings(current_day, current_time)
        
        if dialog.exec_():
            new_day, new_time = dialog.get_settings()
            self.db.update_settings(new_day, new_time)
            self.load_service_time()
            QMessageBox.information(self, "تم الحفظ", "تم تحديث إعدادات الخدمة بنجاح")
    
    def get_threshold_time_24h(self):
        """الحصول على الوقت المحدد بتنسيق 24 ساعة"""
        hours = self.hours_spin.value()
        minutes = self.minutes_spin.value()
        is_pm = self.pm_radio.isChecked()
        
        # تحويل إلى تنسيق 24 ساعة
        if is_pm and hours < 12:
            hours += 12
        elif not is_pm and hours == 12:
            hours = 0
        
        return f"{hours:02d}:{minutes:02d}"
    
    def get_threshold_time_display(self):
        """الحصول على الوقت المحدد للعرض"""
        hours = self.hours_spin.value()
        minutes = self.minutes_spin.value()
        period = "PM" if self.pm_radio.isChecked() else "AM"
        return f"{hours:02d}:{minutes:02d} {period}"
    
    def load_dates(self):
        """تحميل قائمة تواريخ الخدمة فقط"""
        try:
            dates_info = self.db.get_attendance_dates_with_info()
            # تصفية فقط أيام الخدمة
            service_dates = [date for date in dates_info if date['is_service_day']]
            
            self.date_selector.clear()
            for date_info in service_dates:
                self.date_selector.addItem(date_info['display'], date_info['date'])
            
            if service_dates:
                self.date_selector.setCurrentIndex(0)
                self.load_early_arrivals()
            else:
                self.filter_info_label.setText("لا توجد تواريخ خدمة مسجلة")
        except Exception as e:
            QMessageBox.warning(self, "تحذير", f"خطأ في تحميل التواريخ: {str(e)}")
    
    def load_early_arrivals(self):
        """تحميل قائمة الحضور المبكر"""
        try:
            if self.date_selector.currentIndex() < 0:
                return
            
            selected_date = self.date_selector.currentData()
            if not selected_date:
                return
            
            # تحديث معلومات التصفية
            threshold_display = self.get_threshold_time_display()
            self.filter_info_label.setText(f"⚡ الأطفال الذين حضروا قبل الساعة: {threshold_display}")
            
            # الحصول على بيانات الحضور لهذا التاريخ
            data = self.db.load_data()
            attendance_data = data.get('attendance', {}).get(selected_date, {})
            threshold_time_24h = self.get_threshold_time_24h()
            
            # تصفية الحضور المبكر
            early_arrivals = []
            total_attendance = len(attendance_data)
            arrival_times = []
            
            for code, arrival_time in attendance_data.items():
                if self.is_early_arrival(arrival_time, threshold_time_24h):
                    child = self.db.get_child_by_code(code)
                    if child:
                        # تحويل الوقت إلى نظام 12 ساعة للعرض
                        arrival_12h = self.convert_to_12h(arrival_time)
                        early_arrivals.append({
                            'child': child,
                            'arrival_time_24h': arrival_time,
                            'arrival_time_12h': arrival_12h,
                            'date': selected_date
                        })
                        arrival_times.append(self.time_to_minutes(arrival_time))
            
            # تحديث الجدول
            self.update_early_arrival_table(early_arrivals)
            
            # تحديث الإحصائيات
            self.update_stats(total_attendance, len(early_arrivals), arrival_times)
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في تحميل بيانات الحضور المبكر: {str(e)}")
    
    def convert_to_12h(self, time_24h):
        """تحويل الوقت من 24 ساعة إلى 12 ساعة"""
        try:
            hours, minutes = map(int, time_24h.split(':'))
            period = "AM"
            
            if hours >= 12:
                period = "PM"
                if hours > 12:
                    hours -= 12
            elif hours == 0:
                hours = 12
            
            return f"{hours:02d}:{minutes:02d} {period}"
        except:
            return time_24h
    
    def is_early_arrival(self, arrival_time, threshold_time):
        """التحقق إذا كان الحضور مبكراً"""
        try:
            arrival_minutes = self.time_to_minutes(arrival_time)
            threshold_minutes = self.time_to_minutes(threshold_time)
            
            return arrival_minutes < threshold_minutes
        except:
            return False
    
    def time_to_minutes(self, time_str):
        """تحويل الوقت من نص إلى دقائق"""
        try:
            hours, minutes = map(int, time_str.split(':'))
            return hours * 60 + minutes
        except:
            return 0
    
    def minutes_to_time(self, minutes):
        """تحويل الدقائق إلى وقت"""
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"
    
    def update_early_arrival_table(self, early_arrivals):
        """تحديث جدول الحضور المبكر"""
        self.early_arrival_table.setSortingEnabled(False)
        self.early_arrival_table.setRowCount(0)
        
        for arrival in early_arrivals:
            row = self.early_arrival_table.rowCount()
            self.early_arrival_table.insertRow(row)
            
            child = arrival['child']
            self.early_arrival_table.setItem(row, 0, QTableWidgetItem(str(child.get('code', 'غير محدد'))))
            self.early_arrival_table.setItem(row, 1, QTableWidgetItem(child.get('name', 'غير محدد')))
            self.early_arrival_table.setItem(row, 2, QTableWidgetItem(child.get('class', 'غير محدد')))
            self.early_arrival_table.setItem(row, 3, QTableWidgetItem(arrival['arrival_time_24h']))
            self.early_arrival_table.setItem(row, 4, QTableWidgetItem(arrival['arrival_time_12h']))
            self.early_arrival_table.setItem(row, 5, QTableWidgetItem(arrival['date']))
            
            # تحديد حالة الحضور
            status_item = QTableWidgetItem("🟢 حضـور مبـكر")
            self.early_arrival_table.setItem(row, 6, status_item)
        
        self.early_arrival_table.setSortingEnabled(True)
        
        if len(early_arrivals) == 0:
            self.early_arrival_table.setRowCount(1)
            item = QTableWidgetItem("⚠️ لا يوجد حضور مبكر لهذا اليوم")
            item.setTextAlignment(Qt.AlignCenter)
            self.early_arrival_table.setItem(0, 0, item)
            self.early_arrival_table.setSpan(0, 0, 1, 7)
    
    def update_stats(self, total_attendance, early_arrival_count, arrival_times):
        """تحديث الإحصائيات"""
        self.total_attendance_label.setText(f"👥 إجمالي الحضور: {total_attendance}")
        self.early_arrival_label.setText(f"✅ الحضور المبكر: {early_arrival_count}")
        
        if total_attendance > 0:
            percentage = (early_arrival_count / total_attendance) * 100
            self.percentage_label.setText(f"📊 النسبة: {percentage:.1f}%")
        else:
            self.percentage_label.setText("📊 النسبة: 0%")
        
        # حساب متوسط وقت الحضور
        if arrival_times:
            avg_minutes = sum(arrival_times) // len(arrival_times)
            avg_time = self.minutes_to_time(avg_minutes)
            avg_time_12h = self.convert_to_12h(avg_time)
            self.avg_arrival_label.setText(f"⏱️ متوسط الوقت: {avg_time_12h}")
        else:
            self.avg_arrival_label.setText("⏱️ متوسط الوقت: --:--")
    
    def refresh_data(self):
        """تحديث البيانات"""
        self.load_service_time()
        self.load_dates()
        if self.date_selector.currentIndex() >= 0:
            self.load_early_arrivals()
        QMessageBox.information(self, "تم التحديث", "تم تحديث بيانات الحضور المبكر بنجاح")
    
    def export_early_arrivals(self):
        """تصدير تقرير الحضور المبكر"""
        try:
            from PyQt5.QtWidgets import QFileDialog
            
            if self.early_arrival_table.rowCount() == 0:
                QMessageBox.information(self, "معلومة", "لا توجد بيانات للتصدير")
                return
                
            selected_date = self.date_selector.currentData()
            threshold_display = self.get_threshold_time_display()
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, "حفظ تقرير الحضور المبكر", 
                f"تقرير_الحضور_المبكر_{selected_date}.xlsx", 
                "Excel Files (*.xlsx)"
            )
            
            if file_path:
                # جمع بيانات الحضور المبكر للتصدير
                early_arrivals_data = []
                for row in range(self.early_arrival_table.rowCount()):
                    # تخطى صف "لا يوجد حضور مبكر"
                    if self.early_arrival_table.item(row, 0) and self.early_arrival_table.item(row, 0).text().startswith("⚠️"):
                        continue
                        
                    early_arrivals_data.append({
                        'الكود': self.early_arrival_table.item(row, 0).text(),
                        'الاسم': self.early_arrival_table.item(row, 1).text(),
                        'الصف': self.early_arrival_table.item(row, 2).text(),
                        'الوقت (24h)': self.early_arrival_table.item(row, 3).text(),
                        'الوقت (12h)': self.early_arrival_table.item(row, 4).text(),
                        'التاريخ': self.early_arrival_table.item(row, 5).text(),
                        'الحالة': self.early_arrival_table.item(row, 6).text()
                    })
                
                if early_arrivals_data:
                    self.excel_handler.export_early_arrival_report(
                        early_arrivals_data, 
                        file_path, 
                        selected_date,
                        threshold_display
                    )
                    QMessageBox.information(self, "تم التصدير", "تم تصدير تقرير الحضور المبكر بنجاح")
                else:
                    QMessageBox.information(self, "معلومة", "لا توجد بيانات للتصدير")
                    
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في التصدير: {str(e)}")