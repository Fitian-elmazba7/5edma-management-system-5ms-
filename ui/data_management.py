from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QFileDialog, QGroupBox, QLabel,
                             QTextEdit, QProgressBar, QSplitter, QTabWidget,
                             QMenu, QAction, QLineEdit, QDialog, QFormLayout,
                             QDialogButtonBox, QComboBox, QCheckBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from utils.database import DatabaseManager
from utils.excel_handler import ExcelHandler
from .add_child_dialog import AddChildDialog
from .modern_widget import ModernWidget
import pandas as pd
from datetime import datetime

class EditChildDialog(QDialog):
    def __init__(self, child_data, parent=None):
        super().__init__(parent)
        self.child_data = child_data
        self.setWindowTitle("تعديل بيانات الطفل")
        self.setModal(True)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        # الحقول القابلة للتعديل
        self.code_input = QLineEdit()
        self.code_input.setText(self.child_data.get('code', ''))
        self.code_input.setReadOnly(True)  # الكود غير قابل للتعديل
        
        self.name_input = QLineEdit()
        self.name_input.setText(self.child_data.get('name', ''))
        
        self.class_input = QComboBox()
        self.class_input.addItems(["الصف الأول", "الصف الثاني", "الصف الثالث"])
        current_class = self.child_data.get('class', 'الصف الأول')
        index = self.class_input.findText(current_class)
        if index >= 0:
            self.class_input.setCurrentIndex(index)
        
        self.region_input = QLineEdit()
        self.region_input.setText(self.child_data.get('region', ''))
        
        # تفاصيل العنوان
        self.building_input = QLineEdit()
        self.building_input.setText(self.child_data.get('عماره', ''))
        
        self.street_input = QLineEdit()
        self.street_input.setText(self.child_data.get('شارع', ''))
        
        self.floor_input = QLineEdit()
        self.floor_input.setText(self.child_data.get('دور', ''))
        
        self.apartment_input = QLineEdit()
        self.apartment_input.setText(self.child_data.get('شقه', ''))
        
        # أرقام الهواتف
        self.child_phone_input = QLineEdit()
        self.child_phone_input.setText(self.child_data.get('موبيل الولد', ''))
        
        self.father_phone_input = QLineEdit()
        self.father_phone_input.setText(self.child_data.get('موبايل الاب', ''))
        
        self.mother_phone_input = QLineEdit()
        self.mother_phone_input.setText(self.child_data.get('موبايل الام', ''))
        
        self.home_phone_input = QLineEdit()
        self.home_phone_input.setText(self.child_data.get('تليفون', ''))
        
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(80)
        self.notes_input.setPlainText(self.child_data.get('ملاحظات', ''))
        
        # إضافة الحقول إلى النموذج
        form_layout.addRow("الكود:", self.code_input)
        form_layout.addRow("الاسم:", self.name_input)
        form_layout.addRow("الصف:", self.class_input)
        form_layout.addRow("المنطقة:", self.region_input)
        form_layout.addRow("العمارة:", self.building_input)
        form_layout.addRow("الشارع:", self.street_input)
        form_layout.addRow("الدور:", self.floor_input)
        form_layout.addRow("الشقة:", self.apartment_input)
        form_layout.addRow("موبيل الولد:", self.child_phone_input)
        form_layout.addRow("موبايل الأب:", self.father_phone_input)
        form_layout.addRow("موبايل الأم:", self.mother_phone_input)
        form_layout.addRow("تليفون المنزل:", self.home_phone_input)
        form_layout.addRow("ملاحظات:", self.notes_input)
        
        # أزرار
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_and_save)
        button_box.rejected.connect(self.reject)
        
        layout.addLayout(form_layout)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def validate_and_save(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "تحذير", "يرجى إدخال اسم الطفل")
            return
            
        self.accept()
    
    def get_updated_data(self):
        return {
            'code': self.code_input.text().strip(),
            'name': self.name_input.text().strip(),
            'class': self.class_input.currentText(),
            'region': self.region_input.text().strip(),
            'عماره': self.building_input.text().strip(),
            'شارع': self.street_input.text().strip(),
            'دور': self.floor_input.text().strip(),
            'شقه': self.apartment_input.text().strip(),
            'موبيل الولد': self.child_phone_input.text().strip(),
            'موبايل الاب': self.father_phone_input.text().strip(),
            'موبايل الام': self.mother_phone_input.text().strip(),
            'تليفون': self.home_phone_input.text().strip(),
            'ملاحظات': self.notes_input.toPlainText().strip(),
            'address': f"{self.building_input.text().strip()} - {self.street_input.text().strip()} - {self.floor_input.text().strip()} - {self.apartment_input.text().strip()}",
            'last_modified': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

class ExcelInstructionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("تعليمات ملف Excel")
        self.setModal(True)
        self.setFixedSize(800, 600)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # عنوان
        title_label = QLabel("📋 الحد الأدنى المطلوب لملف Excel")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                background-color: #3498db;
                border-radius: 5px;
                margin: 5px;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        
        # التعليمات - تم إصلاح الألوان هنا
        instructions_text = QTextEdit()
        instructions_text.setReadOnly(True)
        instructions_text.setStyleSheet("""
            QTextEdit {
                background-color: #ecf0f1;
                color: #2c3e50;
                font-size: 12px;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        
        instructions_html = """
        <div dir="rtl" style="font-family: Arial; font-size: 12pt; line-height: 1.6;">
        <h2 style="color: #e74c3c;">🎯 المتطلبات الأساسية لملف Excel</h2>
        
        <h3 style="color: #3498db;">📊 الأعمدة الإلزامية (يجب وجودها):</h3>
        <ul>
            <li><strong style="color: #2c3e50;">الاسم</strong> - اسم الطفل (مطلوب)</li>
            <li><strong style="color: #2c3e50;">Code</strong> - كود الطفل (مطلوب)</li>
            <li><strong style="color: #2c3e50;">عماره</strong> - اسم أو رقم العمارة</li>
            <li><strong style="color: #2c3e50;">شارع</strong> - اسم الشارع</li>
            <li><strong style="color: #2c3e50;">دور</strong> - رقم الدور</li>
            <li><strong style="color: #2c3e50;">شقه</strong> - رقم الشقة</li>
        </ul>
        
        <h3 style="color: #27ae60;">📞 الأعمدة الاختيارية (يمكن إضافتها):</h3>
        <ul>
            <li><strong style="color: #2c3e50;">موبيل الولد</strong> - رقم تليفون الطفل</li>
            <li><strong style="color: #2c3e50;">موبايل الاب</strong> - رقم تليفون الأب</li>
            <li><strong style="color: #2c3e50;">موبايل الام</strong> - رقم تليفون الأم</li>
            <li><strong style="color: #2c3e50;">تليفون</strong> - تليفون المنزل</li>
            <li><strong style="color: #2c3e50;">منطقه</strong> - المنطقة</li>
            <li><strong style="color: #2c3e50;">المدرسه</strong> - المدرسة</li>
            <li><strong style="color: #2c3e50;">ملاحظات</strong> - أي ملاحظات إضافية</li>
        </ul>
        
        <h3 style="color: #9b59b6;">💡 ملاحظات هامة:</h3>
        <ul>
            <li>يجب أن يكون الكود فريداً لكل طفل</li>
            <li>يمكن ترك الحقول الاختيارية فارغة</li>
            <li>يجب حفظ الملف بصيغة .xlsx أو .xls</li>
            <li>يفضل استخدام النموذج المرفق للتحميل</li>
        </ul>
        </div>
        """
        
        instructions_text.setHtml(instructions_html)
        
        # أزرار
        button_layout = QHBoxLayout()
        download_template_btn = QPushButton("📥 تحميل نموذج Excel")
        download_template_btn.clicked.connect(self.download_template)
        download_template_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #27ae60, stop: 1 #2ecc71);
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2ecc71, stop: 1 #27ae60);
            }
        """)
        
        close_btn = QPushButton("إغلاق")
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #e74c3c, stop: 1 #c0392b);
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #c0392b, stop: 1 #e74c3c);
            }
        """)
        
        button_layout.addWidget(download_template_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        
        layout.addWidget(title_label)
        layout.addWidget(instructions_text)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def download_template(self):
        """تحميل نموذج Excel فارغ"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "حفظ نموذج Excel", 
                "نموذج_بيانات_الاطفال.xlsx", 
                "Excel Files (*.xlsx)"
            )
            
            if file_path:
                # إنشاء نموذج Excel بالحد الأدنى المطلوب
                template_data = {
                    'Code': ['1001', '1002', '1003'],
                    'الاسم': ['اسم الطفل الأول', 'اسم الطفل الثاني', 'اسم الطفل الثالث'],
                    'عماره': ['1', '2', '3'],
                    'شارع': ['شارع النيل', 'شارع المعادي', 'شارع المدينة'],
                    'دور': ['1', '2', '3'],
                    'شقه': ['1', '2', '3'],
                    'موبيل الولد': ['01000000001', '01000000002', '01000000003'],
                    'موبايل الاب': ['01000000004', '01000000005', '01000000006'],
                    'موبايل الام': ['01000000007', '01000000008', '01000000009'],
                    'تليفون': ['0223456789', '0223456790', '0223456791'],
                    'منطقه': ['المعادي', 'المقطم', 'مصر الجديدة'],
                    'المدرسه': ['المدرسة النموذجية', 'مدرسة الأمل', 'مدرسة المستقبل'],
                    'ملاحظات': ['ملاحظات على الطفل الأول', 'ملاحظات على الطفل الثاني', 'ملاحظات على الطفل الثالث']
                }
                
                df = pd.DataFrame(template_data)
                df.to_excel(file_path, index=False)
                
                QMessageBox.information(self, "تم التحميل", 
                                      f"تم حفظ النموذج في:\\n{file_path}\\n\\nيمكنك الآن فتح الملف وإضافة بيانات الأطفال الفعلية.")
                
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء إنشاء النموذج: {str(e)}")

class DataManagementTab(ModernWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.excel_handler = ExcelHandler()
        self.setup_ui()
        self.load_children_data()
        self.apply_scaled_stylesheet()
        
    def setup_ui(self):
        main_layout = QHBoxLayout()
        
        # Splitter لتقسيم الشاشة
        splitter = QSplitter(Qt.Horizontal)
        
        # اللوحة اليسرى: التحكم والإحصائيات
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # مجموعة الاستيراد
        import_group = QGroupBox("𓃍 استيراد البيانات من Excel")
        import_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                border: 2px solid #34495e;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 8px;
                background-color: #e74c3c;
                color: white;
                border-radius: 3px;
            }
        """)
        import_layout = QVBoxLayout()
        
        self.import_btn = QPushButton("📥 استيراد بيانات الكنيسة")
        self.analyze_btn = QPushButton("🔍 تحليل ملف Excel")
        
        # إضافة خيار الاستيراد التزايدي
        self.incremental_import = QCheckBox("استيراد تزايدي (إضافة بيانات جديدة فقط)")
        self.incremental_import.setChecked(True)
        self.incremental_import.setStyleSheet("QCheckBox { color: #ecf0f1; padding: 8px; }")
        
        # زر تعليمات Excel الجديد
        self.instructions_btn = QPushButton("📋 تعليمات ملف Excel")
        self.instructions_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #9b59b6, stop: 1 #8e44ad);
                color: white;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #8e44ad, stop: 1 #7d3c98);
            }
        """)
        
        for btn in [self.import_btn, self.analyze_btn, self.instructions_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #3498db, stop: 0.7 #2980b9, stop: 1 #3498db);
                    border: 1px solid #2574a9;
                    border-radius: 6px;
                    color: white;
                    font-weight: bold;
                    font-size: 11px;
                    padding: 8px 15px;
                    min-width: 90px;
                    min-height: 30px;
                    margin: 2px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #5dade2, stop: 0.7 #3498db, stop: 1 #5dade2);
                }
            """)
        
        self.import_btn.clicked.connect(self.import_from_excel)
        self.analyze_btn.clicked.connect(self.analyze_excel)
        self.instructions_btn.clicked.connect(self.show_excel_instructions)
        
        import_layout.addWidget(self.import_btn)
        import_layout.addWidget(self.analyze_btn)
        import_layout.addWidget(self.incremental_import)
        import_layout.addWidget(self.instructions_btn)
        import_group.setLayout(import_layout)
        
        # شريط التقدم
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #34495e;
                border-radius: 5px;
                background-color: #2c3e50;
                text-align: center;
                color: white;
                font-size: 10px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #27ae60, stop: 1 #2ecc71);
                border-radius: 3px;
            }
        """)
        
        # مجموعة الإحصائيات
        stats_group = QGroupBox("𓃎 الإحصائيات")
        stats_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                border: 2px solid #34495e;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 8px;
                background-color: #3498db;
                color: white;
                border-radius: 3px;
            }
        """)
        stats_layout = QVBoxLayout()
        
        self.total_label = QLabel("👥 إجمالي الأطفال: 0")
        self.class1_label = QLabel("📚 الصف الأول: 0 طفل")
        self.class2_label = QLabel("📚 الصف الثاني: 0 طفل") 
        self.class3_label = QLabel("📚 الصف الثالث: 0 طفل")
        
        for label in [self.total_label, self.class1_label, self.class2_label, self.class3_label]:
            label.setStyleSheet("""
                QLabel { 
                    font-weight: bold; 
                    padding: 8px; 
                    background-color: #34495e;
                    border-radius: 5px;
                    margin: 2px;
                    color: #ecf0f1;
                }
            """)
            stats_layout.addWidget(label)
        
        stats_group.setLayout(stats_layout)
        
        # مجموعة الإجراءات
        actions_group = QGroupBox("𓃰 الإجراءات")
        actions_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                border: 2px solid #34495e;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 8px;
                background-color: #27ae60;
                color: white;
                border-radius: 3px;
            }
        """)
        actions_layout = QVBoxLayout()
        
        self.add_btn = QPushButton("➕ إضافة طفل جديد")
        self.export_btn = QPushButton("📤 تصدير البيانات")
        self.export_modified_btn = QPushButton("📥 تصدير البيانات المعدلة")  # زر جديد
        self.refresh_btn = QPushButton("🔄 تحديث البيانات")
        
        for btn in [self.add_btn, self.export_btn, self.export_modified_btn, self.refresh_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #3498db, stop: 0.7 #2980b9, stop: 1 #3498db);
                    border: 1px solid #2574a9;
                    border-radius: 6px;
                    color: white;
                    font-weight: bold;
                    font-size: 11px;
                    padding: 8px 15px;
                    min-width: 90px;
                    min-height: 30px;
                    margin: 2px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #5dade2, stop: 0.7 #3498db, stop: 1 #5dade2);
                }
            """)
        
        self.add_btn.clicked.connect(self.add_child)
        self.export_btn.clicked.connect(self.export_to_excel)
        self.export_modified_btn.clicked.connect(self.export_modified_data)  # ربط الزر الجديد
        self.refresh_btn.clicked.connect(self.load_children_data)
        
        actions_layout.addWidget(self.add_btn)
        actions_layout.addWidget(self.export_btn)
        actions_layout.addWidget(self.export_modified_btn)  # إضافة الزر الجديد
        actions_layout.addWidget(self.refresh_btn)
        actions_group.setLayout(actions_layout)
        
        left_layout.addWidget(import_group)
        left_layout.addWidget(self.progress_bar)
        left_layout.addWidget(stats_group)
        left_layout.addWidget(actions_group)
        left_layout.addStretch()
        
        left_panel.setLayout(left_layout)
        
        # اللوحة اليمنى: عرض البيانات
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        # تبويبات لعرض البيانات
        self.tabs = QTabWidget()
        
        # تبويب جميع الأطفال
        self.all_children_tab = QWidget()
        self.setup_children_table(self.all_children_tab)
        
        # تبويب حسب الصفوف
        self.class1_tab = QWidget()
        self.class2_tab = QWidget()
        self.class3_tab = QWidget()
        
        # إعداد الجداول لكل تبويب
        self.setup_children_table(self.class1_tab)
        self.setup_children_table(self.class2_tab)
        self.setup_children_table(self.class3_tab)
        
        self.tabs.addTab(self.all_children_tab, "👥 جميع الأطفال")
        self.tabs.addTab(self.class1_tab, "📚 الصف الأول")
        self.tabs.addTab(self.class2_tab, "📚 الصف الثاني")
        self.tabs.addTab(self.class3_tab, "📚 الصف الثالث")
        
        right_layout.addWidget(self.tabs)
        right_panel.setLayout(right_layout)
        
        # إضافة اللوحات إلى splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([350, 650])
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
    
    def apply_scaled_stylesheet(self):
        """تطبيق الأنماط المعدلة حسب التكبير"""
        base_stylesheet = """
        QGroupBox {
            font-size: 13px;
        }
        QPushButton {
            font-size: 11px;
            padding: 8px 15px;
            min-height: 30px;
        }
        QLabel {
            font-size: 11px;
        }
        QTableWidget {
            font-size: 11px;
        }
        QHeaderView::section {
            font-size: 11px;
            padding: 10px;
        }
        QTabWidget::pane {
            border-radius: 8px;
            margin-top: 5px;
        }
        QTabBar::tab {
            min-width: 180px;
            padding: 12px 16px;
            font-size: 13px;
        }
        QProgressBar {
            font-size: 10px;
        }
        """
        
        scaled_stylesheet = self.get_scaled_stylesheet(base_stylesheet)
        self.setStyleSheet(scaled_stylesheet)
    
    def show_excel_instructions(self):
        """عرض تعليمات ملف Excel"""
        dialog = ExcelInstructionsDialog(self)
        dialog.exec_()
    
    def setup_children_table(self, tab):
        layout = QVBoxLayout()
        
        # إنشاء جدول جديد للتبويب
        children_table = QTableWidget()
        children_table.setColumnCount(13)
        children_table.setHorizontalHeaderLabels([
            "الكود", "الاسم", "الصف", "المنطقة", 
            "العمارة", "الشارع", "الدور", "الشقة",
            "موبيل الولد", "موبايل الأب", "موبايل الأم", "تليفون", "إجراءات"
        ])
        children_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        children_table.setSortingEnabled(True)
        children_table.setContextMenuPolicy(Qt.CustomContextMenu)
        children_table.customContextMenuRequested.connect(self.show_context_menu)
        children_table.setStyleSheet("""
            QTableWidget {
                background-color: #2c3e50;
                alternate-background-color: #34495e;
                selection-background-color: #3498db;
                border: 1px solid #34495e;
                border-radius: 6px;
                gridline-color: #34495e;
                font-size: 11px;
                color: #ecf0f1;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #34495e;
                color: #ecf0f1;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #1a1a2e, stop: 1 #16213e);
                color: white;
                padding: 10px;
                border: 1px solid #0f3460;
                font-weight: bold;
                font-size: 11px;
            }
        """)
        
        # ضبط أبعاد الأعمدة
        children_table.setColumnWidth(0, 80)   # الكود
        children_table.setColumnWidth(1, 150)  # الاسم
        children_table.setColumnWidth(2, 80)   # الصف
        children_table.setColumnWidth(3, 100)  # المنطقة
        children_table.setColumnWidth(4, 80)   # العمارة
        children_table.setColumnWidth(5, 150)  # الشارع
        children_table.setColumnWidth(6, 60)   # الدور
        children_table.setColumnWidth(7, 60)   # الشقة
        children_table.setColumnWidth(8, 120)  # موبيل الولد
        children_table.setColumnWidth(9, 120)  # موبايل الأب
        children_table.setColumnWidth(10, 120) # موبايل الأم
        children_table.setColumnWidth(11, 100) # تليفون
        children_table.setColumnWidth(12, 100) # إجراءات
        
        layout.addWidget(children_table)
        tab.setLayout(layout)
        
        # حفظ المرجع للجدول حسب التبويب
        if tab == self.all_children_tab:
            self.all_children_table = children_table
        elif tab == self.class1_tab:
            self.class1_table = children_table
        elif tab == self.class2_tab:
            self.class2_table = children_table
        elif tab == self.class3_tab:
            self.class3_table = children_table
    
    def show_context_menu(self, position):
        """عرض القائمة المنبثقة للتحرير والحذف"""
        for table in [self.all_children_table, self.class1_table, self.class2_table, self.class3_table]:
            if table.underMouse():
                current_table = table
                break
        else:
            return
        
        row = current_table.rowAt(position.y())
        if row >= 0:
            menu = QMenu()
            
            edit_action = QAction("✏️ تعديل البيانات", self)
            edit_action.triggered.connect(lambda: self.edit_child(current_table, row))
            menu.addAction(edit_action)
            
            delete_action = QAction("🗑️ حذف", self)
            delete_action.triggered.connect(lambda: self.delete_child(current_table, row))
            menu.addAction(delete_action)
            
            menu.exec_(current_table.viewport().mapToGlobal(position))
    
    def edit_child(self, table, row):
        """تعديل بيانات الطفل"""
        try:
            code = table.item(row, 0).text()
            child = self.db.get_child_by_code(code)
            if child:
                dialog = EditChildDialog(child, self)
                if dialog.exec_():
                    updated_data = dialog.get_updated_data()
                    self.update_child_in_database(code, updated_data)
                    self.load_children_data()
                    QMessageBox.information(self, "تم التعديل", "تم تعديل بيانات الطفل بنجاح")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء التعديل: {str(e)}")
    
    def update_child_in_database(self, old_code, new_data):
        """تحديث بيانات الطفل في قاعدة البيانات"""
        data = self.db.load_data()
        for i, child in enumerate(data['children']):
            if str(child.get('code', '')).strip() == str(old_code).strip():
                # تحديث البيانات مع الحفاظ على الكود القديم إذا لم يتغير
                data['children'][i] = {**child, **new_data}
                # تأكد من أن الكود يبقى كما هو
                data['children'][i]['code'] = old_code
                # وضع علامة على البيانات المعدلة
                data['children'][i]['is_modified'] = True
                data['children'][i]['last_modified'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        
        self.db.save_data(data)
    
    def delete_child(self, table, row):
        """حذف طفل من قاعدة البيانات"""
        try:
            code = table.item(row, 0).text()
            name = table.item(row, 1).text()
            
            reply = QMessageBox.question(self, "تأكيد الحذف", 
                                       f"هل أنت متأكد من حذف الطفل {name}؟\nهذا الإجراء لا يمكن التراجع عنه.",
                                       QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.remove_child_from_database(code)
                self.load_children_data()
                QMessageBox.information(self, "تم الحذف", "تم حذف الطفل بنجاح")
                
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الحذف: {str(e)}")
    
    def remove_child_from_database(self, code):
        """إزالة الطفل من قاعدة البيانات"""
        data = self.db.load_data()
        data['children'] = [child for child in data['children'] 
                          if str(child.get('code', '')).strip() != str(code).strip()]
        self.db.save_data(data)
    
    def load_children_data(self):
        children = self.db.get_all_children()
        
        # تحديث جدول جميع الأطفال
        self.populate_table(self.all_children_table, children)
        
        # تحديث الجداول حسب الصفوف
        class1_children = [c for c in children if c.get('class') == 'الصف الأول']
        class2_children = [c for c in children if c.get('class') == 'الصف الثاني']
        class3_children = [c for c in children if c.get('class') == 'الصف الثالث']
        
        self.populate_table(self.class1_table, class1_children)
        self.populate_table(self.class2_table, class2_children)
        self.populate_table(self.class3_table, class3_children)
        
        self.update_stats(children)
    
    def populate_table(self, table, children):
        table.setSortingEnabled(False)
        table.setRowCount(0)
        
        for child in children:
            row = table.rowCount()
            table.insertRow(row)
            
            # إضافة البيانات مع إمكانية التعديل على "غير محدد"
            self.add_table_item(table, row, 0, str(child.get('code', 'غير محدد')))
            self.add_table_item(table, row, 1, child.get('name', 'غير محدد'))
            self.add_table_item(table, row, 2, child.get('class', 'غير محدد'))
            self.add_table_item(table, row, 3, str(child.get('region', 'غير محدد')))
            self.add_table_item(table, row, 4, str(child.get('عماره', 'غير محدد')))
            self.add_table_item(table, row, 5, child.get('شارع', 'غير محدد'))
            self.add_table_item(table, row, 6, str(child.get('دور', 'غير محدد')))
            self.add_table_item(table, row, 7, str(child.get('شقه', 'غير محدد')))
            self.add_table_item(table, row, 8, child.get('موبيل الولد', 'غير محدد'))
            self.add_table_item(table, row, 9, child.get('موبايل الاب', 'غير محدد'))
            self.add_table_item(table, row, 10, child.get('موبايل الام', 'غير محدد'))
            self.add_table_item(table, row, 11, child.get('تليفون', 'غير محدد'))
            
            # إضافة أزرار الإجراءات
            
            
        
        table.setSortingEnabled(True)
    
    def add_table_item(self, table, row, col, text):
        """إضافة عنصر إلى الجدول مع تمييز القيم غير المحددة"""
        item = QTableWidgetItem(text)
        if text == 'غير محدد':
            item.setBackground(Qt.yellow)
            item.setForeground(Qt.red)
            item.setToolTip("قيمة غير محددة - انقر بزر الماوس الأيمن لتعديلها")
        table.setItem(row, col, item)
    
    def show_actions_menu(self, row, table):
        """عرض قائمة الإجراءات"""
        menu = QMenu()
        
        edit_action = QAction("✏️ تعديل", self)
        edit_action.triggered.connect(lambda: self.edit_child(table, row))
        menu.addAction(edit_action)
        
        delete_action = QAction("🗑️ حذف", self)
        delete_action.triggered.connect(lambda: self.delete_child(table, row))
        menu.addAction(delete_action)
        
        button = table.cellWidget(row, 12)
        menu.exec_(button.mapToGlobal(button.rect().bottomLeft()))
    
    def update_stats(self, children):
        total = len(children)
        class1 = len([c for c in children if c.get('class') == 'الصف الأول'])
        class2 = len([c for c in children if c.get('class') == 'الصف الثاني'])
        class3 = len([c for c in children if c.get('class') == 'الصف الثالث'])
        
        self.total_label.setText(f"👥 إجمالي الأطفال: {total}")
        self.class1_label.setText(f"📚 الصف الأول: {class1} طفل")
        self.class2_label.setText(f"📚 الصف الثاني: {class2} طفل")
        self.class3_label.setText(f"📚 الصف الثالث: {class3} طفل")
    
    def import_from_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "اختر ملف Excel الخاص بالكنيسة", "", "Excel Files (*.xlsx *.xls)"
        )
        
        if file_path:
            try:
                self.progress_bar.setVisible(True)
                self.progress_bar.setRange(0, 0)
                
                # تمرير خيار الاستيراد التزايدي
                incremental = self.incremental_import.isChecked()
                QTimer.singleShot(1000, lambda: self.process_import(file_path, incremental))
                
            except Exception as e:
                self.progress_bar.setVisible(False)
                QMessageBox.critical(self, "خطأ", f"حدث خطأ: {str(e)}")
    
    def process_import(self, file_path, incremental=False):
        try:
            imported_count, result = self.excel_handler.import_from_excel(file_path, self.db, incremental)
            
            self.load_children_data()
            self.progress_bar.setVisible(False)
            
            message = f"تم استيراد {imported_count} طفل بنجاح!\n"
            if incremental:
                message += "(الاستيراد التزايدي: تمت إضافة البيانات الجديدة فقط)"
            
            if result['issues']:
                message += f"\n\nملاحظات:\n" + "\n".join(result['issues'][:5])
                if len(result['issues']) > 5:
                    message += f"\n...و {len(result['issues']) - 5} ملاحظة أخرى"
            
            QMessageBox.information(self, "تم الاستيراد", message)
            
        except Exception as e:
            self.progress_bar.setVisible(False)
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الاستيراد: {str(e)}")
    
    def analyze_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "اختر ملف Excel للتحليل", "", "Excel Files (*.xlsx *.xls)"
        )
        
        if file_path:
            try:
                analysis = self.excel_handler.analyze_excel_file(file_path)
                self.show_analysis_report(analysis)
                
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء التحليل: {str(e)}")
    
    def show_analysis_report(self, analysis):
        report_text = f"تقرير تحليل ملف: {analysis['file_info']['file_name']}\n"
        report_text += f"عدد الصفوف: {analysis['file_info']['total_rows']}\n"
        report_text += f"عدد الأعمدة: {analysis['file_info']['total_columns']}\n"
        report_text += f"الأعمدة المطابقة: {analysis['file_info']['required_columns_found']}\n\n"
        
        report_text += "عينة من البيانات:\n"
        for col, value in analysis['sample_data'].items():
            report_text += f"{col}: {value}\n"
        
        QMessageBox.information(self, "تقرير التحليل", report_text)
    
    def add_child(self):
        dialog = AddChildDialog(self)
        if dialog.exec_():
            child_data = dialog.get_child_data()
            try:
                self.db.add_child(child_data)
                self.load_children_data()
                QMessageBox.information(self, "تم الإضافة", "تم إضافة الطفل بنجاح")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", str(e))
    
    def export_to_excel(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "حفظ ملف Excel", "children_data.xlsx", "Excel Files (*.xlsx)"
        )
        
        if file_path:
            try:
                children = self.db.get_all_children()
                self.excel_handler.export_to_excel(children, file_path)
                QMessageBox.information(self, "تم التصدير", "تم تصدير البيانات بنجاح")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء التصدير: {str(e)}")

    def export_modified_data(self):
        """تصدير البيانات المعدلة فقط"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "حفظ البيانات المعدلة", 
                f"البيانات_المعدلة_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx", 
                "Excel Files (*.xlsx)"
            )
            
            if file_path:
                children = self.db.get_all_children()
                
                # تصفية الأطفال المعدلين فقط
                modified_children = [child for child in children if child.get('is_modified')]
                
                if not modified_children:
                    QMessageBox.information(self, "معلومة", "لا توجد بيانات معدلة للتصدير")
                    return
                
                # إنشاء DataFrame للبيانات المعدلة
                data = []
                for child in modified_children:
                    data.append({
                        'الكود': child.get('code', 'غير محدد'),
                        'الاسم': child.get('name', 'غير محدد'),
                        'الصف': child.get('class', 'غير محدد'),
                        'المنطقة': child.get('region', 'غير محدد'),
                        'العمارة': child.get('عماره', 'غير محدد'),
                        'الشارع': child.get('شارع', 'غير محدد'),
                        'الدور': child.get('دور', 'غير محدد'),
                        'الشقة': child.get('شقه', 'غير محدد'),
                        'موبيل الولد': child.get('موبيل الولد', 'غير محدد'),
                        'موبايل الأب': child.get('موبايل الاب', 'غير محدد'),
                        'موبايل الأم': child.get('موبايل الام', 'غير محدد'),
                        'تليفون': child.get('تليفون', 'غير محدد'),
                        'المدرسة': child.get('المدرسه', 'غير محدد'),
                        'ملاحظات': child.get('ملاحظات', 'غير محدد'),
                        'آخر تعديل': child.get('last_modified', 'غير محدد')
                    })
                
                df = pd.DataFrame(data)
                df.to_excel(file_path, index=False)
                
                QMessageBox.information(self, "تم التصدير", 
                                      f"تم تصدير البيانات المعدلة بنجاح!\n\n"
                                      f"الملف: {file_path}\n"
                                      f"عدد الأطفال المعدلين: {len(modified_children)}")
                
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تصدير البيانات المعدلة: {str(e)}")