from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QHeaderView
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QFontDatabase
import os
from datetime import datetime

class ModernWidget(QWidget):
    """
    فئة أساسية حديثة لجميع مكونات الواجهة
    توفر دعم التكبير والأنماط الموحدة
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("ChurchApp", "AttendanceSystem")
        self.zoom_level = self.settings.value("zoom_level", 100, type=int)
        
    def get_scaled_size(self, base_size):
        """الحصول على حجم معدل بناءً على مستوى التكبير"""
        return base_size * (self.zoom_level / 100.0)
    
    def update_zoom_level(self, zoom_level):
        """تحديث مستوى التكبير للعنصر"""
        self.zoom_level = zoom_level
        self.apply_scaled_stylesheet()
        
    def apply_scaled_stylesheet(self):
        """
        تطبيق الأنماط المعدلة حسب التكبير
        يجب تنفيذ هذه الدالة في الفئات الفرعية
        """
        pass
    
    def get_scaled_stylesheet(self, base_stylesheet):
        """
        تحويل الأنماط الأساسية إلى أنماط معدلة حسب التكبير
        """
        base_size = self.zoom_level / 100.0
        
        # استبدال جميع أحجام الخطوط والحقول بناءً على عامل التكبير
        import re
        scaled_stylesheet = base_stylesheet
        
        # استبدال جميع القيم الرقمية في الأنماط
        def scale_match(match):
            value = float(match.group(1))
            return f"{value * base_size}px"
        
        scaled_stylesheet = re.sub(r'(\d+(?:\.\d+)?)px', scale_match, scaled_stylesheet)
            
        return scaled_stylesheet

    def load_arabic_font(self):
        """تحميل الخط العربي"""
        font_paths = [
            "fonts/arial.ttf",
            "fonts/tahoma.ttf", 
            "fonts/arabic_font.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/tahoma.ttf"
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    QFontDatabase.addApplicationFont(font_path)
                except:
                    continue

    def show_success_message(self, title, message):
        """عرض رسالة نجاح"""
        QMessageBox.information(self, title, message)

    def show_error_message(self, title, message):
        """عرض رسالة خطأ"""
        QMessageBox.critical(self, title, message)

    def show_warning_message(self, title, message):
        """عرض رسالة تحذير"""
        QMessageBox.warning(self, title, message)

    def confirm_action(self, title, message):
        """طلب تأكيد الإجراء"""
        reply = QMessageBox.question(self, title, message, 
                                   QMessageBox.Yes | QMessageBox.No, 
                                   QMessageBox.No)
        return reply == QMessageBox.Yes

    def get_save_filename(self, title, default_name, file_filter):
        """الحصول على اسم ملف للحفظ"""
        return QFileDialog.getSaveFileName(self, title, default_name, file_filter)

    def get_open_filename(self, title, file_filter):
        """الحصول على اسم ملف للفتح"""
        return QFileDialog.getOpenFileName(self, title, "", file_filter)

    def export_to_excel(self, data, default_filename, worksheet_name="Data"):
        """تصدير البيانات إلى Excel"""
        try:
            import pandas as pd
            
            file_path, _ = self.get_save_filename(
                "حفظ ملف Excel", 
                default_filename, 
                "Excel Files (*.xlsx)"
            )
            
            if file_path:
                df = pd.DataFrame(data)
                df.to_excel(file_path, index=False, sheet_name=worksheet_name)
                self.show_success_message("تم التصدير", f"تم تصدير البيانات إلى {file_path}")
                return True
            return False
            
        except ImportError:
            self.show_error_message("خطأ", "مكتبة pandas غير مثبتة. يرجى تثبيتها باستخدام: pip install pandas")
            return False
        except Exception as e:
            self.show_error_message("خطأ", f"حدث خطأ أثناء التصدير: {str(e)}")
            return False

    def import_from_excel(self, file_filter="Excel Files (*.xlsx *.xls)"):
        """استيراد البيانات من Excel"""
        try:
            file_path, _ = self.get_open_filename("اختر ملف Excel", file_filter)
            if file_path:
                import pandas as pd
                df = pd.read_excel(file_path)
                return df.to_dict('records')
            return []
            
        except ImportError:
            self.show_error_message("خطأ", "مكتبة pandas غير مثبتة. يرجى تثبيتها باستخدام: pip install pandas")
            return []
        except Exception as e:
            self.show_error_message("خطأ", f"حدث خطأ أثناء الاستيراد: {str(e)}")
            return []

    def get_current_timestamp(self):
        """الحصول على الطابع الزمني الحالي"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_current_date(self):
        """الحصول على التاريخ الحالي"""
        return datetime.now().strftime("%Y-%m-%d")

    def normalize_arabic_text(self, text):
        """تقوم بتطبيع النص العربي لمعالجة الأحرف المتشابهة في البحث"""
        if not text:
            return text
            
        # استبدال الأحرف المتشابهة
        replacements = {
            'أ': 'ا',  # الألف بأشكالها المختلفة
            'إ': 'ا',
            'آ': 'ا',
            'ى': 'ي',  # الياء بأشكالها المختلفة
            'ئ': 'ي',
            'ة': 'ه',  # التاء المربوطة بالهاء
        }
        
        normalized_text = str(text)
        for old_char, new_char in replacements.items():
            normalized_text = normalized_text.replace(old_char, new_char)
        
        return normalized_text

    def validate_phone_number(self, phone):
        """التحقق من صحة رقم التليفون"""
        if not phone or phone == 'غير محدد':
            return True
            
        # إزالة المسافات والأحرف غير الرقمية
        import re
        cleaned_phone = re.sub(r'[^\d]', '', phone)
        
        # التحقق من الطول (عادة 10-11 رقم في مصر)
        return 10 <= len(cleaned_phone) <= 11

    def clean_phone_number(self, phone):
        """تنظيف رقم الهاتف"""
        if not phone or phone == 'غير محدد':
            return 'غير محدد'
        
        import re
        # إزالة أي أحرف غير رقمية
        cleaned = re.sub(r'[^\d]', '', str(phone))
        
        # إذا كان الرقم يبدأ بـ 1 وطوله 10، نضيف 0
        if cleaned.startswith('1') and len(cleaned) == 10:
            cleaned = '0' + cleaned
        
        return cleaned if len(cleaned) >= 10 else 'غير محدد'

    def format_phone_number(self, phone):
        """تنسيق رقم التليفون"""
        if not phone or phone == 'غير محدد':
            return ""
            
        cleaned_phone = self.clean_phone_number(phone)
        
        if len(cleaned_phone) == 11 and cleaned_phone.startswith('0'):
            return f"+2{cleaned_phone}"  # تحويل إلى التنسيق الدولي
        elif len(cleaned_phone) == 10:
            return f"+20{cleaned_phone}"  # إضافة رمز مصر
            
        return phone

    def validate_code(self, code):
        """التحقق من صحة الكود"""
        return bool(code and str(code).strip())

    def create_backup(self, data, backup_type="manual"):
        """إنشاء نسخة احتياطية من البيانات"""
        try:
            import json
            backup_dir = "backups"
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"{backup_type}_backup_{timestamp}.json")
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return backup_file
            
        except Exception as e:
            print(f"Backup error: {e}")
            return None

    def restore_backup(self, backup_file):
        """استعادة البيانات من نسخة احتياطية"""
        try:
            import json
            with open(backup_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.show_error_message("خطأ", f"حدث خطأ أثناء استعادة النسخة الاحتياطية: {str(e)}")
            return None

    def get_backup_files(self):
        """الحصول على قائمة ملفات النسخ الاحتياطية"""
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            return []
        
        backup_files = []
        for file in os.listdir(backup_dir):
            if file.endswith('.json'):
                file_path = os.path.join(backup_dir, file)
                file_time = os.path.getmtime(file_path)
                backup_files.append({
                    'name': file,
                    'path': file_path,
                    'time': datetime.fromtimestamp(file_time).strftime("%Y-%m-%d %H:%M:%S")
                })
        
        # ترتيب من الأحدث إلى الأقدم
        backup_files.sort(key=lambda x: x['path'], reverse=True)
        return backup_files

    def apply_modern_stylesheet(self, widget=None):
        """تطبيق الأنماط الحديثة على الودجة"""
        base_size = self.zoom_level / 100.0
        
        stylesheet = f"""
        /* التنسيقات الرئيسية - تصميم حديث */
        QMainWindow, QWidget {{
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 #0c0c0c, stop: 0.5 #1a1a2e, stop: 1 #16213e);
            font-family: "Segoe UI", "Arial", "Tahoma";
            color: #ffffff;
        }}
        
        /* الأزرار العامة المحدثة */
        QPushButton {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #3498db, stop: 0.7 #2980b9, stop: 1 #3498db);
            border: 1px solid #2574a9;
            border-radius: {6*base_size}px;
            color: white;
            font-weight: bold;
            font-size: {11*base_size}px;
            padding: {8*base_size}px {15*base_size}px;
            min-width: {90*base_size}px;
            min-height: {30*base_size}px;
        }}
        
        QPushButton:hover {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #5dade2, stop: 0.7 #3498db, stop: 1 #5dade2);
            transform: translateY(-1px);
        }}
        
        QPushButton:pressed {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #2471a3, stop: 1 #1b4f72);
            transform: translateY(0px);
        }}
        
        /* أزرار النجاح */
        QPushButton.success {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #27ae60, stop: 0.7 #2ecc71, stop: 1 #27ae60);
            border: 1px solid #219653;
        }}
        
        QPushButton.success:hover {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #2ecc71, stop: 0.7 #27ae60, stop: 1 #2ecc71);
        }}
        
        /* أزرار التحذير */
        QPushButton.warning {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #e74c3c, stop: 0.7 #c0392b, stop: 1 #e74c3c);
            border: 1px solid #c0392b;
        }}
        
        QPushButton.warning:hover {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #c0392b, stop: 0.7 #e74c3c, stop: 1 #c0392b);
        }}
        
        /* أزرار المعلومات */
        QPushButton.info {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #9b59b6, stop: 0.7 #8e44ad, stop: 1 #9b59b6);
            border: 1px solid #8e44ad;
        }}
        
        QPushButton.info:hover {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #8e44ad, stop: 0.7 #9b59b6, stop: 1 #8e44ad);
        }}
        
        /* حقول الإدخال المحدثة */
        QLineEdit, QComboBox, QTextEdit {{
            border: 2px solid #34495e;
            border-radius: {6*base_size}px;
            padding: {8*base_size}px;
            font-size: {12*base_size}px;
            background-color: #2c3e50;
            color: #ecf0f1;
            selection-background-color: #3498db;
        }}
        
        QLineEdit:focus, QComboBox:focus, QTextEdit:focus {{
            border-color: #3498db;
            background-color: #34495e;
        }}
        
        /* الجداول المحدثة */
        QTableWidget {{
            background-color: #2c3e50;
            alternate-background-color: #34495e;
            selection-background-color: #3498db;
            border: 1px solid #34495e;
            border-radius: {6*base_size}px;
            gridline-color: #34495e;
            font-size: {11*base_size}px;
            color: #ecf0f1;
        }}
        
        QTableWidget::item {{
            padding: {8*base_size}px;
            border-bottom: 1px solid #34495e;
            color: #ecf0f1;
        }}
        
        QTableWidget::item:selected {{
            background-color: #3498db;
            color: white;
        }}
        
        /* رؤوس الجداول المحدثة */
        QHeaderView::section {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #1a1a2e, stop: 1 #16213e);
            color: white;
            padding: {10*base_size}px;
            border: 1px solid #0f3460;
            font-weight: bold;
            font-size: {11*base_size}px;
        }}
        
        /* المجموعات المحدثة */
        QGroupBox {{
            font-weight: bold;
            font-size: {13*base_size}px;
            border: 2px solid #34495e;
            border-radius: {8*base_size}px;
            margin-top: {10*base_size}px;
            padding-top: {10*base_size}px;
            background-color: #2c3e50;
            color: #ecf0f1;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: {5*base_size}px {15*base_size}px;
            background-color: #e74c3c;
            color: white;
            border-radius: {5*base_size}px;
        }}
        
        /* التسميات المحدثة */
        QLabel {{
            color: #ecf0f1;
            font-size: {11*base_size}px;
        }}
        
        /* شريط التقدم المحدث */
        QProgressBar {{
            border: 2px solid #34495e;
            border-radius: {5*base_size}px;
            background-color: #2c3e50;
            text-align: center;
            color: white;
            font-size: {10*base_size}px;
        }}
        
        QProgressBar::chunk {{
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #27ae60, stop: 1 #2ecc71);
            border-radius: {3*base_size}px;
        }}
        
        /* Splitter المحدث */
        QSplitter::handle {{
            background: #34495e;
            border: 1px solid #2c3e50;
        }}
        
        QSplitter::handle:hover {{
            background: #3498db;
        }}
        
        /* تبويبات محدثة */
        QTabWidget::pane {{
            border: 2px solid #34495e;
            background-color: #2c3e50;
            border-radius: {8*base_size}px;
            margin-top: {5*base_size}px;
        }}
        
        QTabWidget::tab-bar {{
            alignment: center;
        }}
        
        QTabBar::tab {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #34495e, stop: 0.4 #2c3e50,
                stop: 0.5 #273c51, stop: 1.0 #2c3e50);
            border: 2px solid #1a252f;
            border-bottom-color: #2c3e50;
            border-top-left-radius: {8*base_size}px;
            border-top-right-radius: {8*base_size}px;
            min-width: {180*base_size}px;
            padding: {12*base_size}px {16*base_size}px;
            margin: {2*base_size}px;
            font-size: {13*base_size}px;
            font-weight: bold;
            color: #ecf0f1;
        }}
        
        QTabBar::tab:selected {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #e74c3c, stop: 0.7 #c0392b, stop: 1 #e74c3c);
            color: white;
            border-bottom: 2px solid #e74c3c;
        }}
        
        QTabBar::tab:hover:!selected {{
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #5dade2, stop: 0.7 #3498db, stop: 1 #5dade2);
            color: white;
        }}
        """
        
        if widget:
            widget.setStyleSheet(stylesheet)
        else:
            self.setStyleSheet(stylesheet)

    def create_modern_button(self, text, button_type="default", tooltip=""):
        """إنشاء زر حديث"""
        from PyQt5.QtWidgets import QPushButton
        
        button = QPushButton(text)
        
        if button_type == "success":
            button.setProperty("class", "success")
        elif button_type == "warning":
            button.setProperty("class", "warning")
        elif button_type == "info":
            button.setProperty("class", "info")
        
        if tooltip:
            button.setToolTip(tooltip)
            
        return button

    def setup_modern_table(self, table, headers, column_widths=None):
        """إعداد جدول حديث"""
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(True)
        
        if column_widths:
            for col, width in enumerate(column_widths):
                table.setColumnWidth(col, width)
        
        return table

    def add_table_context_menu(self, table, menu_actions):
        """إضافة قائمة منبثقة للجدول"""
        from PyQt5.QtWidgets import QMenu, QAction
        from PyQt5.QtCore import Qt
        
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        
        def show_context_menu(position):
            menu = QMenu()
            for action_text, callback in menu_actions:
                action = QAction(action_text, table)
                action.triggered.connect(callback)
                menu.addAction(action)
            menu.exec_(table.viewport().mapToGlobal(position))
        
        table.customContextMenuRequested.connect(show_context_menu)