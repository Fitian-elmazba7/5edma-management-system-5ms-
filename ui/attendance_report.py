from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QComboBox, QGroupBox, QPushButton, QMessageBox,
                             QSplitter, QProgressBar, QCheckBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from utils.database import DatabaseManager
from utils.excel_handler import ExcelHandler
from datetime import datetime
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
import arabic_reshaper
from bidi.algorithm import get_display
import os

class AttendanceReportTab(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.excel_handler = ExcelHandler()
        self.current_attendance_data = []
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
        title_label = QLabel("𓃭 تقرير الحضور الشامل")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setProperty("class", "page-title")

        
        # مجموعة التحكم
        control_group = QGroupBox("إعدادات التقرير")
        control_layout = QVBoxLayout()
        
        control_layout.addWidget(QLabel("اختر تاريخ الخدمة:"))
        self.date_selector = QComboBox()
        self.date_selector.currentTextChanged.connect(self.load_attendance_data)
        
        # خيار عرض أيام الخدمة فقط
        self.service_days_only = QCheckBox("عرض أيام الخدمة فقط")
        self.service_days_only.stateChanged.connect(self.load_dates)
        
        # معلومات التاريخ المحدد
        self.date_info_label = QLabel("")
        self.date_info_label.setProperty("class", "info-label")

        
        self.refresh_btn = QPushButton("تحديث البيانات")
        self.refresh_btn.clicked.connect(self.refresh_data)
        
        control_layout.addWidget(self.service_days_only)
        control_layout.addWidget(self.date_selector)
        control_layout.addWidget(self.date_info_label)
        control_layout.addWidget(self.refresh_btn)
        
        control_group.setLayout(control_layout)
        
        # الإحصائيات
        stats_group = QGroupBox("الإحصائيات الفورية")
        stats_layout = QVBoxLayout()
        
        self.total_label = QLabel("إجمالي الأطفال: 0")
        self.present_label = QLabel("الحضور الكلي: 0")
        self.attendance_rate_label = QLabel("نسبة الحضور: 0%")
        self.class1_label = QLabel("الصف الأول: 0")
        self.class2_label = QLabel("الصف الثاني: 0") 
        self.class3_label = QLabel("الصف الثالث: 0")
        
        for label in [self.total_label, self.present_label, self.attendance_rate_label, 
                     self.class1_label, self.class2_label, self.class3_label]:
            label.setProperty("class", "info-label")

            stats_layout.addWidget(label)
        
        stats_group.setLayout(stats_layout)
        
        # أزرار التصدير - تم التعديل هنا
        export_group = QGroupBox("تصدير التقارير")
        export_layout = QVBoxLayout()
        
        # تصدير الكل
        all_export_layout = QHBoxLayout()
        self.export_excel_btn = QPushButton("📊 تصدير الكل إلى Excel")
        self.export_excel_btn.clicked.connect(self.export_to_excel)
        self.export_excel_btn.setProperty("class", "btn-success")

        
        self.export_pdf_btn = QPushButton("📄 تصدير الكل إلى PDF")
        self.export_pdf_btn.clicked.connect(self.export_to_pdf)
        self.export_pdf_btn.setProperty("class", "btn-danger")

        
        all_export_layout.addWidget(self.export_excel_btn)
        all_export_layout.addWidget(self.export_pdf_btn)
        
        # تصدير حسب الصف
        class_export_layout = QVBoxLayout()
        class_export_layout.addWidget(QLabel("📚 تصدير حسب الصف:"))
        
        # الصف الأول
        class1_layout = QHBoxLayout()
        self.export_class1_excel_btn = QPushButton("الصف الأول - Excel")
        self.export_class1_excel_btn.clicked.connect(lambda: self.export_class_to_excel('الصف الأول'))
        self.export_class1_excel_btn.setProperty("class", "default")

        
        self.export_class1_pdf_btn = QPushButton("الصف الأول - PDF")
        self.export_class1_pdf_btn.clicked.connect(lambda: self.export_class_to_pdf('الصف الأول'))
        self.export_class1_pdf_btn.setProperty("class", "btn-purple")

        
        class1_layout.addWidget(self.export_class1_excel_btn)
        class1_layout.addWidget(self.export_class1_pdf_btn)
        
        # الصف الثاني
        class2_layout = QHBoxLayout()
        self.export_class2_excel_btn = QPushButton("الصف الثاني - Excel")
        self.export_class2_excel_btn.clicked.connect(lambda: self.export_class_to_excel('الصف الثاني'))
        self.export_class2_excel_btn.setProperty("class", "default")

        
        self.export_class2_pdf_btn = QPushButton("الصف الثاني - PDF")
        self.export_class2_pdf_btn.clicked.connect(lambda: self.export_class_to_pdf('الصف الثاني'))
        self.export_class2_pdf_btn.setProperty("class", "btn-purple")

        
        class2_layout.addWidget(self.export_class2_excel_btn)
        class2_layout.addWidget(self.export_class2_pdf_btn)
        
        # الصف الثالث
        class3_layout = QHBoxLayout()
        self.export_class3_excel_btn = QPushButton("الصف الثالث - Excel")
        self.export_class3_excel_btn.clicked.connect(lambda: self.export_class_to_excel('الصف الثالث'))
        self.export_class3_excel_btn.setProperty("class", "default")

        
        self.export_class3_pdf_btn = QPushButton("الصف الثالث - PDF")
        self.export_class3_pdf_btn.clicked.connect(lambda: self.export_class_to_pdf('الصف الثالث'))
        self.export_class3_pdf_btn.setProperty("class", "btn-purple")

        
        class3_layout.addWidget(self.export_class3_excel_btn)
        class3_layout.addWidget(self.export_class3_pdf_btn)
        
        class_export_layout.addLayout(class1_layout)
        class_export_layout.addLayout(class2_layout)
        class_export_layout.addLayout(class3_layout)
        
        export_layout.addLayout(all_export_layout)
        export_layout.addLayout(class_export_layout)
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
        
        # معلومات التقرير
        self.report_info_label = QLabel("تقرير الحضور الشامل")
        self.report_info_label.setProperty("class", "info-label")

        right_layout.addWidget(self.report_info_label)
        
        # جدول الحضور
        self.attendance_table = QTableWidget()
        self.setup_attendance_table()
        
        right_layout.addWidget(self.attendance_table)
        right_panel.setLayout(right_layout)
        
        # إضافة اللوحات إلى splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 600])  # زيادة عرض اللوحة اليسرى قليلاً
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
    
    def setup_attendance_table(self):
        """إعداد جدول الحضور"""
        self.attendance_table.setColumnCount(8)
        self.attendance_table.setHorizontalHeaderLabels([
            "الكود", "الاسم", "الصف", "المنطقة", "العمارة", "الشارع", "وقت الحضور", "التاريخ"
        ])
        
        self.attendance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.attendance_table.setAlternatingRowColors(True)
        self.attendance_table.setSortingEnabled(True)
        
        # ضبط أبعاد الأعمدة
        self.attendance_table.setColumnWidth(0, 80)   # الكود
        self.attendance_table.setColumnWidth(1, 150)  # الاسم
        self.attendance_table.setColumnWidth(2, 100)  # الصف
        self.attendance_table.setColumnWidth(3, 100)  # المنطقة
        self.attendance_table.setColumnWidth(4, 80)   # العمارة
        self.attendance_table.setColumnWidth(5, 120)  # الشارع
        self.attendance_table.setColumnWidth(6, 100)  # وقت الحضور
        self.attendance_table.setColumnWidth(7, 100)  # التاريخ
    
    def load_dates(self):
        """تحميل تواريخ الحضور المسجلة"""
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
    
    def load_attendance_data(self):
        """تحميل بيانات الحضور للتاريخ المحدد"""
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
            
            # الحصول على بيانات الحضور
            data = self.db.load_data()
            attendance_data = data.get('attendance', {}).get(selected_date, {})
            
            # جمع بيانات الأطفال الحاضرين
            self.current_attendance_data = []
            for code, arrival_time in attendance_data.items():
                child = self.db.get_child_by_code(code)
                if child:
                    attendance_record = child.copy()
                    attendance_record['arrival_time'] = arrival_time
                    attendance_record['attendance_date'] = selected_date
                    self.current_attendance_data.append(attendance_record)
            
            # تحديث الجدول
            self.update_attendance_table()
            
            # تحديث الإحصائيات
            self.update_stats(selected_date)
            
            # تحديث معلومات التقرير
            self.report_info_label.setText(f"تقرير الحضور الشامل - {selected_date} | عدد الحاضرين: {len(self.current_attendance_data)}")
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في تحميل بيانات الحضور: {str(e)}")
    
    def update_attendance_table(self):
        """تحديث جدول الحضور"""
        try:
            self.attendance_table.setSortingEnabled(False)
            self.attendance_table.setRowCount(0)
            
            for record in self.current_attendance_data:
                row = self.attendance_table.rowCount()
                self.attendance_table.insertRow(row)
                
                self.attendance_table.setItem(row, 0, QTableWidgetItem(str(record.get('code', 'غير محدد'))))
                self.attendance_table.setItem(row, 1, QTableWidgetItem(record.get('name', 'غير محدد')))
                self.attendance_table.setItem(row, 2, QTableWidgetItem(record.get('class', 'غير محدد')))
                self.attendance_table.setItem(row, 3, QTableWidgetItem(record.get('region', 'غير محدد')))
                self.attendance_table.setItem(row, 4, QTableWidgetItem(str(record.get('عماره', 'غير محدد'))))
                self.attendance_table.setItem(row, 5, QTableWidgetItem(record.get('شارع', 'غير محدد')))
                self.attendance_table.setItem(row, 6, QTableWidgetItem(record.get('arrival_time', 'غير محدد')))
                self.attendance_table.setItem(row, 7, QTableWidgetItem(record.get('attendance_date', 'غير محدد')))
            
            self.attendance_table.setSortingEnabled(True)
            
            if len(self.current_attendance_data) == 0:
                self.attendance_table.setRowCount(1)
                item = QTableWidgetItem("⚠️ لا يوجد حضور مسجل لهذا اليوم")
                item.setTextAlignment(Qt.AlignCenter)
                self.attendance_table.setItem(0, 0, item)
                self.attendance_table.setSpan(0, 0, 1, 8)
                
        except Exception as e:
            print(f"Error updating attendance table: {str(e)}")
    
    def update_stats(self, date):
        """تحديث الإحصائيات"""
        try:
            stats = self.db.get_attendance_stats_by_date(date)
            if not stats:
                self.total_label.setText("إجمالي الأطفال: 0")
                self.present_label.setText("الحضور الكلي: 0")
                self.attendance_rate_label.setText("نسبة الحضور: 0%")
                self.class1_label.setText("الصف الأول: 0")
                self.class2_label.setText("الصف الثاني: 0")
                self.class3_label.setText("الصف الثالث: 0")
                return
            
            self.total_label.setText(f"إجمالي الأطفال: {stats['total']}")
            self.present_label.setText(f"الحضور الكلي: {stats['present']}")
            self.attendance_rate_label.setText(f"نسبة الحضور: {stats['attendance_rate']:.1f}%")
            
            class_stats = stats.get('classes', {})
            self.class1_label.setText(f"الصف الأول: حاضر {class_stats.get('الصف الأول', {}).get('present', 0)}")
            self.class2_label.setText(f"الصف الثاني: حاضر {class_stats.get('الصف الثاني', {}).get('present', 0)}")
            self.class3_label.setText(f"الصف الثالث: حاضر {class_stats.get('الصف الثالث', {}).get('present', 0)}")
            
        except Exception as e:
            print(f"Error updating stats: {str(e)}")
    
    def refresh_data(self):
        """تحديث البيانات"""
        self.load_dates()
        if self.date_selector.currentIndex() >= 0:
            self.load_attendance_data()
        QMessageBox.information(self, "تم التحديث", "تم تحديث بيانات الحضور بنجاح")
    
    def get_class_data(self, class_name):
        """الحصول على بيانات الحضور لصف معين"""
        if not self.current_attendance_data:
            return []
        
        return [record for record in self.current_attendance_data if record.get('class') == class_name]
    
    def export_class_to_excel(self, class_name):
        """تصدير تقرير الحضور لصف معين إلى Excel"""
        class_data = self.get_class_data(class_name)
        
        if not class_data:
            QMessageBox.information(self, "معلومة", f"لا توجد بيانات حضور للصف {class_name}")
            return
        
        try:
            from PyQt5.QtWidgets import QFileDialog
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, f"حفظ تقرير الحضور - {class_name}", 
                f"تقرير_الحضور_{class_name}_{self.current_date}.xlsx", 
                "Excel Files (*.xlsx)"
            )
            
            if file_path:
                # إنشاء DataFrame للبيانات
                data = []
                for record in class_data:
                    data.append({
                        'الكود': record.get('code', 'غير محدد'),
                        'الاسم': record.get('name', 'غير محدد'),
                        'الصف': record.get('class', 'غير محدد'),
                        'المنطقة': record.get('region', 'غير محدد'),
                        'العمارة': record.get('عماره', 'غير محدد'),
                        'الشارع': record.get('شارع', 'غير محدد'),
                        'الدور': record.get('دور', 'غير محدد'),
                        'الشقة': record.get('شقه', 'غير محدد'),
                        'موبيل الولد': record.get('موبيل الولد', 'غير محدد'),
                        'موبايل الأب': record.get('موبايل الاب', 'غير محدد'),
                        'موبايل الأم': record.get('موبايل الام', 'غير محدد'),
                        'تليفون': record.get('تليفون', 'غير محدد'),
                        'وقت الحضور': record.get('arrival_time', 'غير محدد'),
                        'تاريخ الحضور': record.get('attendance_date', 'غير محدد')
                    })
                
                # إنشاء ملف Excel مع تنسيق محسن
                wb = Workbook()
                ws = wb.active
                ws.title = f"تقرير الحضور - {class_name}"
                
                # إضافة العناوين
                titles = [
                    f"تقرير الحضور - {class_name}",
                    f"تاريخ التقرير: {self.current_date}",
                    f"وقت التصدير: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                    f"عدد الحاضرين: {len(class_data)}"
                ]
                
                for i, title in enumerate(titles, 1):
                    ws[f'A{i}'] = title
                    ws[f'A{i}'].font = Font(bold=True, size=14 if i == 1 else 12)
                    ws[f'A{i}'].alignment = Alignment(horizontal='center')
                
                # دمج الخلايا للعناوين
                ws.merge_cells('A1:N1')
                ws.merge_cells('A2:N2')
                ws.merge_cells('A3:N3')
                ws.merge_cells('A4:N4')
                
                # إضافة رؤوس الأعمدة
                headers = ['الكود', 'الاسم', 'الصف', 'المنطقة', 'العمارة', 'الشارع', 'الدور', 'الشقة',
                          'موبيل الولد', 'موبايل الأب', 'موبايل الأم', 'تليفون', 'وقت الحضور', 'تاريخ الحضور']
                
                for col, header in enumerate(headers, 1):
                    cell = ws.cell(row=6, column=col, value=header)
                    cell.font = Font(bold=True, color="FFFFFF", size=12)
                    cell.fill = PatternFill(start_color="2C3E50", end_color="2C3E50", fill_type="solid")
                    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
                    cell.border = Border(left=Side(style='thin'), right=Side(style='thin'),
                                       top=Side(style='thin'), bottom=Side(style='thin'))
                
                # إضافة البيانات
                for row, record in enumerate(data, 7):
                    for col, key in enumerate(headers, 1):
                        cell = ws.cell(row=row, column=col, value=record.get(key, ''))
                        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
                        cell.border = Border(left=Side(style='thin'), right=Side(style='thin'),
                                           top=Side(style='thin'), bottom=Side(style='thin'))
                
                # ضبط أبعاد الأعمدة
                column_widths = {
                    'A': 12, 'B': 25, 'C': 15, 'D': 15, 'E': 12, 'F': 20, 'G': 10, 'H': 10,
                    'I': 15, 'J': 15, 'K': 15, 'L': 15, 'M': 12, 'N': 12
                }
                
                for col, width in column_widths.items():
                    ws.column_dimensions[col].width = width
                
                # حفظ الملف
                wb.save(file_path)
                
                QMessageBox.information(self, "تم التصدير", 
                                      f"تم تصدير تقرير الحضور للصف {class_name} إلى Excel بنجاح!\n\n"
                                      f"الملف: {file_path}\n"
                                      f"عدد السجلات: {len(class_data)}")
                
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في التصدير إلى Excel: {str(e)}")
    
    def export_class_to_pdf(self, class_name):
        """تصدير تقرير الحضور لصف معين إلى PDF"""
        class_data = self.get_class_data(class_name)
        
        if not class_data:
            QMessageBox.information(self, "معلومة", f"لا توجد بيانات حضور للصف {class_name}")
            return
        
        try:
            from PyQt5.QtWidgets import QFileDialog
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, f"حفظ تقرير PDF - {class_name}", 
                f"تقرير_الحضور_{class_name}_{self.current_date}.pdf", 
                "PDF Files (*.pdf)"
            )
            
            if not file_path:
                return
            
            # البحث عن خطوط عربية
            arabic_font_paths = [
                "fonts/arial.ttf",
                "fonts/tahoma.ttf",
                "fonts/arabic_font.ttf",
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/tahoma.ttf"
            ]
            
            arabic_font_name = None
            for font_path in arabic_font_paths:
                if os.path.exists(font_path):
                    try:
                        font_name = os.path.splitext(os.path.basename(font_path))[0]
                        pdfmetrics.registerFont(TTFont(font_name, font_path))
                        arabic_font_name = font_name
                        break
                    except:
                        continue
            
            if not arabic_font_name:
                arabic_font_name = "Helvetica"
            
            # إنشاء مستند PDF
            doc = SimpleDocTemplate(file_path, pagesize=landscape(A4),
                                  rightMargin=20, leftMargin=20, topMargin=30, bottomMargin=30)
            elements = []
            styles = getSampleStyleSheet()
            
            # إضافة عنوان
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontName=arabic_font_name,
                fontSize=16,
                spaceAfter=20,
                alignment=1,
                textColor=colors.HexColor('#2C3E50')
            )
            
            title_text = self.reshape_arabic(f"تقرير الحضور - {class_name}")
            elements.append(Paragraph(title_text, title_style))
            
            # معلومات التقرير
            info_style = ParagraphStyle(
                'CustomInfo',
                parent=styles['Normal'],
                fontName=arabic_font_name,
                fontSize=10,
                spaceAfter=8,
                alignment=1
            )
            
            info_texts = [
                f"تاريخ التقرير: {self.current_date}",
                f"وقت التصدير: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                f"عدد الحاضرين: {len(class_data)}"
            ]
            
            for text in info_texts:
                elements.append(Paragraph(self.reshape_arabic(text), info_style))
            
            elements.append(Spacer(1, 20))
            
            # رؤوس الأعمدة (من اليمين لليسار)
            headers = [
                'تاريخ الحضور', 'وقت الحضور', 'تليفون', 'موبايل الأم', 'موبايل الأب', 
                'موبيل الولد', 'الشقة', 'الدور', 'الشارع', 'العمارة', 
                'المنطقة', 'الصف', 'الاسم', 'الكود'
            ]
            
            # إعداد بيانات الجدول
            table_data = [headers]
            
            for record in class_data:
                table_data.append([
                    self.reshape_arabic(record.get('attendance_date', 'غير محدد')),
                    self.reshape_arabic(record.get('arrival_time', 'غير محدد')),
                    self.reshape_arabic(record.get('تليفون', 'غير محدد')),
                    self.reshape_arabic(record.get('موبايل الام', 'غير محدد')),
                    self.reshape_arabic(record.get('موبايل الاب', 'غير محدد')),
                    self.reshape_arabic(record.get('موبيل الولد', 'غير محدد')),
                    self.reshape_arabic(record.get('شقه', 'غير محدد')),
                    self.reshape_arabic(record.get('دور', 'غير محدد')),
                    self.reshape_arabic(record.get('شارع', 'غير محدد')),
                    self.reshape_arabic(record.get('عماره', 'غير محدد')),
                    self.reshape_arabic(record.get('region', 'غير محدد')),
                    self.reshape_arabic(record.get('class', 'غير محدد')),
                    self.reshape_arabic(record.get('name', 'غير محدد')),
                    self.reshape_arabic(record.get('code', 'غير محدد'))
                ])
            
            # إنشاء الجدول
            table = Table(table_data, repeatRows=1)
            
            # تنسيق الجدول
            table.setStyle(TableStyle([
                # تنسيق رأس الجدول
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), arabic_font_name),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                
                # تنسيق بيانات الجدول
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTNAME', (0, 1), (-1, -1), arabic_font_name),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                
                # الحدود
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                
                # التفاف النص
                ('WORDWRAP', (0, 0), (-1, -1), True),
            ]))
            
            # ضبط أبعاد الأعمدة
            col_widths = [50, 50, 50, 50, 50, 50, 40, 40, 50, 40, 40, 50, 50, 40]
            table._argW = col_widths
            
            elements.append(table)
            
            # بناء PDF
            doc.build(elements)
            QMessageBox.information(self, "تم التصدير", f"تم تصدير تقرير PDF للصف {class_name} بنجاح!")
            
        except ImportError as e:
            QMessageBox.critical(self, "خطأ", 
                               f"المكتبات المطلوبة غير مثبتة!\n"
                               f"يرجى تثبيت المكتبات التالية:\n"
                               f"pip install reportlab arabic-reshaper python-bidi")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء التصدير إلى PDF: {str(e)}")
    
    # الدوال الأصلية تبقى كما هي مع تعديلات بسيطة
    def export_to_excel(self):
        """تصدير تقرير الحضور إلى Excel"""
        if not self.current_attendance_data:
            QMessageBox.information(self, "معلومة", "لا توجد بيانات حضور للتصدير")
            return
        
        try:
            from PyQt5.QtWidgets import QFileDialog
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, "حفظ تقرير الحضور", 
                f"تقرير_الحضور_{self.current_date}.xlsx", 
                "Excel Files (*.xlsx)"
            )
            
            if file_path:
                # إنشاء DataFrame للبيانات
                data = []
                for record in self.current_attendance_data:
                    data.append({
                        'الكود': record.get('code', 'غير محدد'),
                        'الاسم': record.get('name', 'غير محدد'),
                        'الصف': record.get('class', 'غير محدد'),
                        'المنطقة': record.get('region', 'غير محدد'),
                        'العمارة': record.get('عماره', 'غير محدد'),
                        'الشارع': record.get('شارع', 'غير محدد'),
                        'الدور': record.get('دور', 'غير محدد'),
                        'الشقة': record.get('شقه', 'غير محدد'),
                        'موبيل الولد': record.get('موبيل الولد', 'غير محدد'),
                        'موبايل الأب': record.get('موبايل الاب', 'غير محدد'),
                        'موبايل الأم': record.get('موبايل الام', 'غير محدد'),
                        'تليفون': record.get('تليفون', 'غير محدد'),
                        'وقت الحضور': record.get('arrival_time', 'غير محدد'),
                        'تاريخ الحضور': record.get('attendance_date', 'غير محدد')
                    })
                
                # إنشاء ملف Excel مع تنسيق محسن
                wb = Workbook()
                ws = wb.active
                ws.title = "تقرير الحضور"
                
                # إضافة العناوين
                titles = [
                    f"تقرير الحضور الشامل",
                    f"تاريخ التقرير: {self.current_date}",
                    f"وقت التصدير: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                    f"عدد الحاضرين: {len(self.current_attendance_data)}"
                ]
                
                for i, title in enumerate(titles, 1):
                    ws[f'A{i}'] = title
                    ws[f'A{i}'].font = Font(bold=True, size=14 if i == 1 else 12)
                    ws[f'A{i}'].alignment = Alignment(horizontal='center')
                
                # دمج الخلايا للعناوين
                ws.merge_cells('A1:N1')
                ws.merge_cells('A2:N2')
                ws.merge_cells('A3:N3')
                ws.merge_cells('A4:N4')
                
                # إضافة رؤوس الأعمدة
                headers = ['الكود', 'الاسم', 'الصف', 'المنطقة', 'العمارة', 'الشارع', 'الدور', 'الشقة',
                          'موبيل الولد', 'موبايل الأب', 'موبايل الأم', 'تليفون', 'وقت الحضور', 'تاريخ الحضور']
                
                for col, header in enumerate(headers, 1):
                    cell = ws.cell(row=6, column=col, value=header)
                    cell.font = Font(bold=True, color="FFFFFF", size=12)
                    cell.fill = PatternFill(start_color="2C3E50", end_color="2C3E50", fill_type="solid")
                    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
                    cell.border = Border(left=Side(style='thin'), right=Side(style='thin'),
                                       top=Side(style='thin'), bottom=Side(style='thin'))
                
                # إضافة البيانات
                for row, record in enumerate(data, 7):
                    for col, key in enumerate(headers, 1):
                        cell = ws.cell(row=row, column=col, value=record.get(key, ''))
                        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
                        cell.border = Border(left=Side(style='thin'), right=Side(style='thin'),
                                           top=Side(style='thin'), bottom=Side(style='thin'))
                
                # ضبط أبعاد الأعمدة
                column_widths = {
                    'A': 12, 'B': 25, 'C': 15, 'D': 15, 'E': 12, 'F': 20, 'G': 10, 'H': 10,
                    'I': 15, 'J': 15, 'K': 15, 'L': 15, 'M': 12, 'N': 12
                }
                
                for col, width in column_widths.items():
                    ws.column_dimensions[col].width = width
                
                # حفظ الملف
                wb.save(file_path)
                
                QMessageBox.information(self, "تم التصدير", 
                                      f"تم تصدير تقرير الحضور إلى Excel بنجاح!\n\n"
                                      f"الملف: {file_path}\n"
                                      f"عدد السجلات: {len(self.current_attendance_data)}")
                
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في التصدير إلى Excel: {str(e)}")
    
    def export_to_pdf(self):
        """تصدير تقرير الحضور إلى PDF"""
        if not self.current_attendance_data:
            QMessageBox.information(self, "معلومة", "لا توجد بيانات حضور للتصدير")
            return
        
        try:
            from PyQt5.QtWidgets import QFileDialog
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, "حفظ تقرير PDF", 
                f"تقرير_الحضور_{self.current_date}.pdf", 
                "PDF Files (*.pdf)"
            )
            
            if not file_path:
                return
            
            # البحث عن خطوط عربية
            arabic_font_paths = [
                "fonts/arial.ttf",
                "fonts/tahoma.ttf",
                "fonts/arabic_font.ttf",
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/tahoma.ttf"
            ]
            
            arabic_font_name = None
            for font_path in arabic_font_paths:
                if os.path.exists(font_path):
                    try:
                        font_name = os.path.splitext(os.path.basename(font_path))[0]
                        pdfmetrics.registerFont(TTFont(font_name, font_path))
                        arabic_font_name = font_name
                        break
                    except:
                        continue
            
            if not arabic_font_name:
                arabic_font_name = "Helvetica"
            
            # إنشاء مستند PDF
            doc = SimpleDocTemplate(file_path, pagesize=landscape(A4),
                                  rightMargin=20, leftMargin=20, topMargin=30, bottomMargin=30)
            elements = []
            styles = getSampleStyleSheet()
            
            # إضافة عنوان رئيسي
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontName=arabic_font_name,
                fontSize=16,
                spaceAfter=20,
                alignment=1,
                textColor=colors.HexColor('#2C3E50')
            )
            
            title_text = self.reshape_arabic("تقرير الحضور الشامل")
            elements.append(Paragraph(title_text, title_style))
            
            # معلومات التقرير
            info_style = ParagraphStyle(
                'CustomInfo',
                parent=styles['Normal'],
                fontName=arabic_font_name,
                fontSize=10,
                spaceAfter=8,
                alignment=1
            )
            
            info_texts = [
                f"تاريخ التقرير: {self.current_date}",
                f"وقت التصدير: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                f"عدد الحاضرين: {len(self.current_attendance_data)}"
            ]
            
            for text in info_texts:
                elements.append(Paragraph(self.reshape_arabic(text), info_style))
            
            elements.append(Spacer(1, 20))
            
            # رؤوس الأعمدة (من اليمين لليسار)
            headers = [
                'تاريخ الحضور', 'وقت الحضور', 'تليفون', 'موبايل الأم', 'موبايل الأب', 
                'موبيل الولد', 'الشقة', 'الدور', 'الشارع', 'العمارة', 
                'المنطقة', 'الصف', 'الاسم', 'الكود'
            ]
            
            # إعداد بيانات الجدول
            table_data = [headers]
            
            for record in self.current_attendance_data:
                table_data.append([
                    self.reshape_arabic(record.get('attendance_date', 'غير محدد')),
                    self.reshape_arabic(record.get('arrival_time', 'غير محدد')),
                    self.reshape_arabic(record.get('تليفون', 'غير محدد')),
                    self.reshape_arabic(record.get('موبايل الام', 'غير محدد')),
                    self.reshape_arabic(record.get('موبايل الاب', 'غير محدد')),
                    self.reshape_arabic(record.get('موبيل الولد', 'غير محدد')),
                    self.reshape_arabic(record.get('شقه', 'غير محدد')),
                    self.reshape_arabic(record.get('دور', 'غير محدد')),
                    self.reshape_arabic(record.get('شارع', 'غير محدد')),
                    self.reshape_arabic(record.get('عماره', 'غير محدد')),
                    self.reshape_arabic(record.get('region', 'غير محدد')),
                    self.reshape_arabic(record.get('class', 'غير محدد')),
                    self.reshape_arabic(record.get('name', 'غير محدد')),
                    self.reshape_arabic(record.get('code', 'غير محدد'))
                ])
            
            # إنشاء الجدول
            table = Table(table_data, repeatRows=1)
            
            # تنسيق الجدول
            table.setStyle(TableStyle([
                # تنسيق رأس الجدول
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), arabic_font_name),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                
                # تنسيق بيانات الجدول
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTNAME', (0, 1), (-1, -1), arabic_font_name),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                
                # الحدود
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                
                # التفاف النص
                ('WORDWRAP', (0, 0), (-1, -1), True),
            ]))
            
            # ضبط أبعاد الأعمدة
            col_widths = [50, 50, 50, 50, 50, 50, 40, 40, 50, 40, 40, 50, 50, 40]
            table._argW = col_widths
            
            elements.append(table)
            
            # بناء PDF
            doc.build(elements)
            QMessageBox.information(self, "تم التصدير", "تم تصدير تقرير PDF بنجاح!")
            
        except ImportError as e:
            QMessageBox.critical(self, "خطأ", 
                               f"المكتبات المطلوبة غير مثبتة!\n"
                               f"يرجى تثبيت المكتبات التالية:\n"
                               f"pip install reportlab arabic-reshaper python-bidi")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء التصدير إلى PDF: {str(e)}")
    
    def reshape_arabic(self, text):
        """إعادة تشكيل النص العربي للعرض الصحيح في PDF"""
        try:
            if not text or text == 'غير محدد':
                return 'غير محدد'
            
            # إعادة تشكيل النص العربي
            reshaped_text = arabic_reshaper.reshape(str(text))
            # تحويل النص إلى تنسيق من اليمين لليسار
            bidi_text = get_display(reshaped_text)
            return bidi_text
        except:
            # في حالة حدوث خطأ، إرجاع النص الأصلي
            return str(text)
