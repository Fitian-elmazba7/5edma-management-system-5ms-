from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QComboBox, QTextEdit, QPushButton, 
                             QFormLayout, QMessageBox, QTabWidget, QWidget,
                             QGroupBox, QScrollArea)
from PyQt5.QtCore import Qt
from utils.database import DatabaseManager

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class ChildDetailsDialog(QDialog):
    def __init__(self, child_data, parent=None):
        super().__init__(parent)
        self.child_data = child_data
        self.db = DatabaseManager()
        self.setWindowTitle("𓃰 تفاصيل الطفل")
        self.setModal(True)
        self.setMinimumSize(800, 600)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Create tab widget for better organization
        self.tabs = QTabWidget()
        
        # Basic Info Tab
        self.basic_info_tab = QWidget()
        self.setup_basic_info_tab()
        
        # Contact Info Tab
        self.contact_info_tab = QWidget()
        self.setup_contact_info_tab()
        
        # Address Info Tab
        self.address_info_tab = QWidget()
        self.setup_address_info_tab()
        
        # Notes Tab
        self.notes_tab = QWidget()
        self.setup_notes_tab()
        
        # Stats Tab
        self.stats_tab = QWidget()
        self.setup_stats_tab()
        
        self.tabs.addTab(self.basic_info_tab, "المعلومات الأساسية")
        self.tabs.addTab(self.contact_info_tab, "معلومات الاتصال")
        self.tabs.addTab(self.address_info_tab, "العنوان")
        self.tabs.addTab(self.notes_tab, "ملاحظات")
        self.tabs.addTab(self.stats_tab, "إحصائيات")
        
        layout.addWidget(self.tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("💾 حفظ التعديلات")
        self.save_btn.setProperty("class", "btn-success")

        self.save_btn.clicked.connect(self.save_changes)
        
        self.close_btn = QPushButton("إغلاق")
        self.close_btn.setProperty("class", "btn-danger")

        self.close_btn.clicked.connect(self.close)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Load child data into fields
        self.load_child_data()
    
    def setup_basic_info_tab(self):
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        # Code (read-only)
        self.code_input = QLineEdit()
        self.code_input.setReadOnly(True)
        self.code_input.setReadOnly(True)

        
        # Name
        self.name_input = QLineEdit()
        
        # Class
        self.class_input = QComboBox()
        self.class_input.addItems(["الصف الأول", "الصف الثاني", "الصف الثالث"])
        
        # Region
        self.region_input = QLineEdit()
        
        # School
        self.school_input = QLineEdit()
        
        form_layout.addRow("الكود:", self.code_input)
        form_layout.addRow("الاسم:", self.name_input)
        form_layout.addRow("الصف:", self.class_input)
        form_layout.addRow("المنطقة:", self.region_input)
        form_layout.addRow("المدرسة:", self.school_input)
        
        layout.addLayout(form_layout)
        layout.addStretch()
        
        self.basic_info_tab.setLayout(layout)
    
    def setup_contact_info_tab(self):
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        # Phone numbers
        self.child_phone_input = QLineEdit()
        self.father_phone_input = QLineEdit()
        self.mother_phone_input = QLineEdit()
        self.home_phone_input = QLineEdit()
        
        form_layout.addRow("موبيل الولد:", self.child_phone_input)
        form_layout.addRow("موبايل الأب:", self.father_phone_input)
        form_layout.addRow("موبايل الأم:", self.mother_phone_input)
        form_layout.addRow("تليفون المنزل:", self.home_phone_input)
        
        layout.addLayout(form_layout)
        layout.addStretch()
        
        self.contact_info_tab.setLayout(layout)
    
    def setup_address_info_tab(self):
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        # Address details
        self.building_input = QLineEdit()
        self.street_input = QLineEdit()
        self.floor_input = QLineEdit()
        self.apartment_input = QLineEdit()
        
        form_layout.addRow("العمارة:", self.building_input)
        form_layout.addRow("الشارع:", self.street_input)
        form_layout.addRow("الدور:", self.floor_input)
        form_layout.addRow("الشقة:", self.apartment_input)
        
        layout.addLayout(form_layout)
        layout.addStretch()
        
        self.address_info_tab.setLayout(layout)
    
    def setup_notes_tab(self):
        layout = QVBoxLayout()
        
        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(200)
        
        layout.addWidget(QLabel("ملاحظات:"))
        layout.addWidget(self.notes_input)
        layout.addStretch()
        
        self.notes_tab.setLayout(layout)
    
    def setup_stats_tab(self):
        layout = QVBoxLayout()
        
        if not self.child_data:
            layout.addWidget(QLabel("لا توجد بيانات متاحة"))
            self.stats_tab.setLayout(layout)
            return

        # Calculate Stats
        all_dates = self.db.get_attendance_dates()
        total_days = len(all_dates)
        present_days = 0
        
        attendance_data = self.db.load_data().get('attendance', {})
        child_code = str(self.child_data.get('code', '')).strip()
        
        for date_str, attendees in attendance_data.items():
            if child_code in attendees:
                present_days += 1
                
        absent_days = total_days - present_days
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        # Summary Labels
        info_layout = QHBoxLayout()
        total_label = QLabel(f"إجمالي أيام الخدمة: {total_days}")
        present_label = QLabel(f"أيام الحضور: {present_days}")
        absent_label = QLabel(f"أيام الغياب: {absent_days}")
        percent_label = QLabel(f"نسبة الحضور: {attendance_percentage:.1f}%")
        
        # Style labels for emphasis
        for lbl in [total_label, present_label, absent_label, percent_label]:
            lbl.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
            
        info_layout.addWidget(total_label)
        info_layout.addWidget(present_label)
        info_layout.addWidget(absent_label)
        info_layout.addWidget(percent_label)
        
        layout.addLayout(info_layout)
        
        # Graph
        if total_days > 0:
            self.figure = Figure(figsize=(5, 4), dpi=100)
            self.canvas = FigureCanvas(self.figure)
            
            ax = self.figure.add_subplot(111)
            
            # Pie Chart Data
            labels = ['حضور', 'غياب']
            sizes = [present_days, absent_days]
            colors = ['#2ecc71', '#e74c3c']  # Green, Red
            explode = (0.1, 0)  # offset the 1st slice (Present)
            
            patches, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=90)
            
            # Enhance font for Arabic support if needed (matplotlib might need font config, but basic labels often work)
            # For now relying on default font or system fallback
            
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            ax.set_title("نسبة الحضور والغياب")
            
            layout.addWidget(self.canvas)
        else:
            layout.addWidget(QLabel("لا توجد بيانات حضور مسجلة في النظام لعرض الرسم البياني"))
            
        self.stats_tab.setLayout(layout)

    def load_child_data(self):
        """Load child data into form fields"""
        if not self.child_data:
            return
            
        # Basic Info
        self.code_input.setText(str(self.child_data.get('code', '')))
        self.name_input.setText(self.child_data.get('name', ''))
        
        # Set class
        class_name = self.child_data.get('class', 'الصف الأول')
        index = self.class_input.findText(class_name)
        if index >= 0:
            self.class_input.setCurrentIndex(index)
            
        self.region_input.setText(self.child_data.get('region', ''))
        self.school_input.setText(self.child_data.get('المدرسه', ''))
        
        # Contact Info
        self.child_phone_input.setText(self.child_data.get('موبيل الولد', ''))
        self.father_phone_input.setText(self.child_data.get('موبايل الاب', ''))
        self.mother_phone_input.setText(self.child_data.get('موبايل الام', ''))
        self.home_phone_input.setText(self.child_data.get('تليفون', ''))
        
        # Address Info
        self.building_input.setText(str(self.child_data.get('عماره', '')))
        self.street_input.setText(self.child_data.get('شارع', ''))
        self.floor_input.setText(str(self.child_data.get('دور', '')))
        self.apartment_input.setText(str(self.child_data.get('شقه', '')))
        
        # Notes
        self.notes_input.setPlainText(self.child_data.get('ملاحظات', ''))
    
    def get_updated_data(self):
        """Get updated data from form fields"""
        return {
            'code': self.code_input.text().strip(),
            'name': self.name_input.text().strip(),
            'class': self.class_input.currentText(),
            'region': self.region_input.text().strip(),
            'المدرسه': self.school_input.text().strip(),
            'موبيل الولد': self.child_phone_input.text().strip(),
            'موبايل الاب': self.father_phone_input.text().strip(),
            'موبايل الام': self.mother_phone_input.text().strip(),
            'تليفون': self.home_phone_input.text().strip(),
            'عماره': self.building_input.text().strip(),
            'شارع': self.street_input.text().strip(),
            'دور': self.floor_input.text().strip(),
            'شقه': self.apartment_input.text().strip(),
            'ملاحظات': self.notes_input.toPlainText().strip(),
            'address': f"{self.building_input.text().strip()} - {self.street_input.text().strip()} - {self.floor_input.text().strip()} - {self.apartment_input.text().strip()}",
            'is_modified': True
        }
    
    def save_changes(self):
        """Save changes to database"""
        try:
            updated_data = self.get_updated_data()
            
            # Validate required fields
            if not updated_data['name'].strip():
                QMessageBox.warning(self, "تحذير", "يرجى إدخال اسم الطفل")
                return
                
            if not updated_data['code'].strip():
                QMessageBox.warning(self, "تحذير", "يرجى إدخال كود الطفل")
                return
            
            # Update in database
            success = self.db.update_child(self.child_data['code'], updated_data)
            
            if success:
                QMessageBox.information(self, "تم الحفظ", "تم حفظ التعديلات بنجاح")
                self.child_data = updated_data  # Update local data
                self.accept()
            else:
                QMessageBox.critical(self, "خطأ", "حدث خطأ أثناء حفظ التعديلات")
                
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ: {str(e)}")