# main_window.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QLabel, QPushButton, QGroupBox, QTextEdit, 
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QCompleter, QComboBox, QMenu, QAction, QDialog)
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
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # مجموعة إدخال الكود أو الاسم
        input_group = QGroupBox("🎯 إدخال كود أو اسم الطفل")
        input_layout = QVBoxLayout()
        input_layout.setSpacing(10)
        input_layout.setContentsMargins(12, 16, 12, 12)
        
        # إدخال الكود
        code_layout = QHBoxLayout()
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("أدخل كود الطفل ثم اضغط Enter")
        self.code_input.setStyleSheet("")

        self.code_input.returnPressed.connect(self.register_by_code)
        self.code_input.textChanged.connect(self.on_code_changed)
        
        self.register_btn = QPushButton("📝 تسجيل بالكود")
        self.register_btn.setProperty("class", "btn-success")

        self.register_btn.clicked.connect(self.register_by_code)
        
        code_layout.addWidget(QLabel("الكود:"))
        code_layout.addWidget(self.code_input)
        code_layout.addWidget(self.register_btn)
        
        # إدخال الاسم مع البحث
        name_layout = QHBoxLayout()
        self.name_input = QComboBox()
        self.name_input.setEditable(True)
        self.name_input.setPlaceholderText("ابحث باسم الطفل ثم اضغط Enter للتسجيل")
        self.name_input.setStyleSheet("")

        
        # Connect text changes to show details automatically
        self.name_input.lineEdit().textChanged.connect(self.on_name_changed)
        # Connect Enter key to register immediately
        self.name_input.lineEdit().returnPressed.connect(self.register_by_name_enter)
        
        self.search_btn = QPushButton("🔍 بحث بالاسم")
        self.search_btn.setProperty("class", "default")

        self.search_btn.clicked.connect(self.search_by_name)
        
        name_layout.addWidget(QLabel("الاسم:"))
        name_layout.addWidget(self.name_input)
        name_layout.addWidget(self.search_btn)
        
        input_layout.addLayout(code_layout)
        input_layout.addLayout(name_layout)
        input_group.setLayout(input_layout)
        
        # مجموعة البحث في الجلسة الحالية
        search_group = QGroupBox("🔍 بحث في الجلسة الحالية")
        search_layout = QVBoxLayout()
        search_layout.setSpacing(8)
        search_layout.setContentsMargins(12, 16, 12, 12)

        search_input_layout = QHBoxLayout()
        self.session_search_input = QLineEdit()
        self.session_search_input.setPlaceholderText("ابحث عن طفل في الجلسة الحالية (بالاسم أو الكود)...")
        self.session_search_input.setStyleSheet("")

        self.session_search_input.textChanged.connect(self.search_in_current_session)

        self.clear_search_btn = QPushButton("مسح")
        self.clear_search_btn.setProperty("class", "btn-danger")

        self.clear_search_btn.clicked.connect(self.clear_session_search)

        search_input_layout.addWidget(self.session_search_input)
        search_input_layout.addWidget(self.clear_search_btn)

        self.search_results_display = QTextEdit()
        self.search_results_display.setReadOnly(True)
        self.search_results_display.setMaximumHeight(120)
        self.search_results_display.setStyleSheet("")


        search_layout.addLayout(search_input_layout)
        search_layout.addWidget(self.search_results_display)
        search_group.setLayout(search_layout)
        
        # عرض بيانات الطفل
        self.info_display = QTextEdit()
        self.info_display.setReadOnly(True)
        self.info_display.setMaximumHeight(140)
        self.info_display.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.info_display.setStyleSheet("")

        
        # جدول الحضور
        self.attendance_table = QTableWidget()
        self.attendance_table.setColumnCount(5)
        self.attendance_table.setHorizontalHeaderLabels(["الكود", "الاسم", "الصف", "الوقت", "التاريخ"])
        self.attendance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.attendance_table.setSortingEnabled(True)
        self.attendance_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.attendance_table.customContextMenuRequested.connect(self.show_attendance_context_menu)
        self.attendance_table.setStyleSheet("")

        
        # أزرار التحكم
        control_layout = QHBoxLayout()
        control_layout.setSpacing(8)
        control_layout.setContentsMargins(0, 8, 0, 0)
        self.finish_btn = QPushButton("✅ إنهاء الجلسة ومسح البيانات")
        self.finish_btn.setProperty("class", "btn-success")

        self.finish_btn.clicked.connect(self.finish_session)
        
        self.clear_btn = QPushButton("🗑️ مسح الكل")
        self.clear_btn.setProperty("class", "btn-danger")

        self.clear_btn.clicked.connect(self.clear_session)
        
        self.refresh_btn = QPushButton("🔄 تحديث البيانات")
        self.refresh_btn.setProperty("class", "default")

        self.refresh_btn.clicked.connect(self.refresh_data)
        
        control_layout.addWidget(self.finish_btn)
        control_layout.addWidget(self.clear_btn)
        control_layout.addWidget(self.refresh_btn)
        control_layout.addStretch()
        
        layout.addWidget(input_group)
        layout.addWidget(search_group)  # أضفنا مجموعة البحث هنا
        layout.addWidget(QLabel("📋 بيانات الطفل:"))
        layout.addWidget(self.info_display)
        layout.addWidget(QLabel("📊 قائمة الحضور الحالية:"))
        layout.addWidget(self.attendance_table)
        layout.addLayout(control_layout)
        
        self.setLayout(layout)
    
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
                
                # تحميل الأطفال المسجلين في الجلسة السابقة
                for code in session_data.get('registered_codes', []):
                    child = self.db.get_child_by_code(code)
                    if child and code not in self.registered_codes:
                        self.add_to_attendance_table(child)
                        self.registered_codes.add(code)
                
                if self.registered_codes:
                    self.update_buttons_state()
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
        """تقوم بتطبيع النص العربي لمعالجة الأحرف المتشابهة في البحث"""
        if not text:
            return text
            
        # استبدال الأحرف المتشابهة
        replacements = {
            'أ': 'ا',
            'إ': 'ا',
            'آ': 'ا',
            'ى': 'ي',
            'ئ': 'ي',
            'ة': 'ه',
        }
        
        normalized_text = str(text)
        for old_char, new_char in replacements.items():
            normalized_text = normalized_text.replace(old_char, new_char)
        
        return normalized_text
    
    def load_children_data(self):
        """تحميل بيانات الأطفال لتعبئة قائمة البحث"""
        self.all_children = self.db.get_all_children()
        names = []
        self.name_to_child_map = {}
        
        for child in self.all_children:
            name = child.get('name', '')
            if name and name != 'غير محدد':
                names.append(name)
                self.name_to_child_map[name] = child
        
        # إعداد الاكتمال التلقائي
        completer = QCompleter(names)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        
        self.name_input.setCompleter(completer)
        self.name_input.clear()
        self.name_input.addItems(names)
    
    def on_name_changed(self, text):
        """عرض تفاصيل الطفل تلقائياً عند كتابة الاسم"""
        name = text.strip()
        if not name:
            self.info_display.clear()
            self.current_selected_child = None
            return
        
        # البحث عن الطفل بالاسم المطابق تماماً أولاً
        child = self.name_to_child_map.get(name)
        if child:
            self.current_selected_child = child
            self.show_child_details(child)
            self.code_input.setText(child.get('code', ''))
            return
        
        # إذا لم يتم العثور على تطابق تام، البحث بالتطبيع
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
            # تحديث نص الاسم في الحقل ليظهر الاسم الصحيح
            self.name_input.lineEdit().setText(found_child.get('name', ''))
        else:
            # إذا لم يتم العثور على أي طفل، مسح التفاصيل
            self.info_display.clear()
            self.current_selected_child = None
    
    def search_by_name(self):
        """البحث عن الطفل بالاسم وعرض تفاصيله"""
        name = self.name_input.currentText().strip()
        if not name:
            return
        
        self.on_name_changed(name)
    
    def register_by_name_enter(self):
        """التسجيل المباشر عند الضغط على Enter في حقل الاسم"""
        # If we already have a selected child from typing, register them
        if self.current_selected_child:
            self.register_child(self.current_selected_child)
        else:
            # If no child is selected yet, try to find one first
            name = self.name_input.currentText().strip()
            if name:
                self.on_name_changed(name)
                if self.current_selected_child:
                    self.register_child(self.current_selected_child)
                else:
                    QMessageBox.warning(self, "تحذير", "لم يتم العثور على الطفل. يرجى التأكد من الاسم والمحاولة مرة أخرى.")
    
    def on_code_changed(self, text):
        """عرض تفاصيل الطفل تلقائياً عند كتابة الكود"""
        if text.strip():
            child = self.db.get_child_by_code(text.strip())
            if child:
                self.current_selected_child = child
                self.show_child_details(child)
                self.name_input.setCurrentText(child.get('name', ''))
            else:
                self.info_display.setText("⚠️ الكود غير موجود في قاعدة البيانات")
                self.current_selected_child = None
        else:
            self.info_display.clear()
            self.current_selected_child = None
    
    def show_child_details(self, child):
        """عرض تفاصيل الطفل بالتنسيق المطلوب"""
        details = f"""
<div style="font-family: Arial; font-size: 14px; line-height: 1.6;">
<div style="background: #e74c3c; color: white; padding: 8px; border-radius: 5px; margin-bottom: 8px; text-align: center; font-size: 16px;">
<strong>𓃰 {child.get('name', 'غير محدد')} - الكود: {child.get('code', 'غير محدد')}</strong>
</div>

<div style="font-size: 13px;">
<div style="margin-bottom: 3px;"><span style="color: #3498db;">● الاسم:</span> {child.get('name', 'غير محدد')}</div>
<div style="margin-bottom: 3px;"><span style="color: #3498db;">● الكود:</span> {child.get('code', 'غير محدد')}</div>
<div style="margin-bottom: 3px;"><span style="color: #27ae60;">● الصف:</span> {child.get('class', 'غير محدد')}</div>
<div style="margin-bottom: 3px;"><span style="color: #9b59b6;">● المنطقة:</span> {child.get('region', 'غير محدد')}</div>
<div style="margin-bottom: 3px;"><span style="color: #e67e22;">● موبيل الولد:</span> {child.get('موبيل الولد', 'غير محدد')}</div>
<div style="margin-bottom: 3px;"><span style="color: #34495e;">● موبايل الأب:</span> {child.get('موبايل الاب', 'غير محدد')}</div>
<div style="margin-bottom: 3px;"><span style="color: #16a085;">● العنوان:</span> {child.get('عماره', 'غير محدد')} - {child.get('شارع', 'غير محدد')}</div>
<div style="margin-bottom: 3px;"><span style="color: #f1c40f;">● المدرسة:</span> {child.get('المدرسه', 'غير محدد')}</div>
<div style="margin-bottom: 3px;"><span style="color: #7f8c8d;">● موبايل الأم:</span> {child.get('موبايل الام', 'غير محدد')}</div>
<div style="margin-bottom: 3px;"><span style="color: #95a5a6;">● تليفون:</span> {child.get('تليفون', 'غير محدد')}</div>
<div style="margin-bottom: 3px;"><span style="color: #c0392b;">● ملاحظات:</span> {child.get('ملاحظات', 'غير محدد')}</div>
</div>
</div>
    """
        self.info_display.setHtml(details)
    
    def register_child(self, child):
        """تسجيل الطفل في الحضور"""
        code = child.get('code', '')
        if not code:
            return
        
        # منع التسجيل المكرر
        if code in self.registered_codes:
            QMessageBox.warning(self, "تحذير", "تم تسجيل هذا الطفل مسبقاً!")
            return
        
        # حفظ الحضور فوراً في قاعدة البيانات
        success = self.db.save_immediate_attendance(code)
        
        if success:
            self.show_child_details(child)
            self.add_to_attendance_table(child)
            self.registered_codes.add(code)
            
            # حفظ الجلسة الحالية
            self.save_current_session()
            
            self.code_input.clear()
            self.name_input.setCurrentIndex(-1)
            self.name_input.setCurrentText("")
            self.current_selected_child = None
            self.code_input.setFocus()
            
            # تحديث حالة الأزرار
            self.update_buttons_state()
            
            QMessageBox.information(self, "تم التسجيل", f"تم تسجيل الطفل {child.get('name', '')} بنجاح!")
        else:
            QMessageBox.critical(self, "خطأ", "حدث خطأ أثناء حفظ البيانات!")
    
    def register_by_code(self):
        """تسجيل الحضور باستخدام الكود"""
        code = self.code_input.text().strip()
        if not code:
            return
        
        # منع التسجيل المكرر
        if code in self.registered_codes:
            QMessageBox.warning(self, "تحذير", "تم تسجيل هذا الطفل مسبقاً!")
            return
            
        child = self.db.get_child_by_code(code)
        if child:
            self.current_selected_child = child
            self.register_child(child)
        else:
            self.info_display.setText("⚠️ الكود غير موجود في قاعدة البيانات")
    
    def add_to_attendance_table(self, child):
        """إضافة الطفل إلى جدول الحضور"""
        from datetime import datetime
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%Y-%m-%d")
        
        # تعطيل الترتيب مؤقتاً أثناء الإضافة
        self.attendance_table.setSortingEnabled(False)
        
        row = self.attendance_table.rowCount()
        self.attendance_table.insertRow(row)
        
        self.attendance_table.setItem(row, 0, QTableWidgetItem(child.get('code', '')))
        self.attendance_table.setItem(row, 1, QTableWidgetItem(child.get('name', '')))
        self.attendance_table.setItem(row, 2, QTableWidgetItem(child.get('class', '')))
        self.attendance_table.setItem(row, 3, QTableWidgetItem(time_str))
        self.attendance_table.setItem(row, 4, QTableWidgetItem(date_str))
        
        # إعادة تمكين الترتيب
        self.attendance_table.setSortingEnabled(True)
    
    def show_attendance_context_menu(self, position):
        """عرض القائمة المنبثقة مع خيار التفاصيل"""
        row = self.attendance_table.rowAt(position.y())
        if row >= 0:
            menu = QMenu()
            
            # إضافة إجراء التفاصيل
            details_action = QAction("𓃰 عرض التفاصيل", self)
            details_action.triggered.connect(lambda: self.show_child_details_dialog(row))
            menu.addAction(details_action)
            
            delete_action = QAction("🗑️ حذف التسجيل", self)
            delete_action.triggered.connect(lambda: self.delete_attendance_row(row))
            menu.addAction(delete_action)
            
            menu.exec_(self.attendance_table.viewport().mapToGlobal(position))
    
    def show_child_details_dialog(self, row):
        """عرض نافذة تفاصيل الطفل"""
        try:
            code = self.attendance_table.item(row, 0).text()
            child = self.db.get_child_by_code(code)
            if child:
                dialog = ChildDetailsDialog(child, self)
                dialog.exec_()
                # تحديث العرض بعد إغلاق النافذة
                if dialog.result() == QDialog.Accepted:
                    # إعادة تحميل بيانات الطفل لعرض أي تحديثات
                    updated_child = self.db.get_child_by_code(code)
                    if updated_child:
                        self.show_child_details(updated_child)
            else:
                QMessageBox.warning(self, "تحذير", "لم يتم العثور على بيانات الطفل")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء فتح التفاصيل: {str(e)}")
    
    def delete_attendance_row(self, row):
        """حذف طفل من جدول الحضور عبر القائمة المنبثقة"""
        try:
            code = self.attendance_table.item(row, 0).text()
            name = self.attendance_table.item(row, 1).text()
            
            reply = QMessageBox.question(self, "تأكيد الحذف", 
                                       f"هل أنت متأكد من حذف تسجيل الطفل {name}؟",
                                       QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                # إزالة من قاعدة البيانات
                self.db.remove_attendance(code)
                
                # تعطيل الترتيب مؤقتاً
                self.attendance_table.setSortingEnabled(False)
                
                # إزالة من الجدول
                self.attendance_table.removeRow(row)
                
                # إزالة من مجموعة التسجيلات
                if code in self.registered_codes:
                    self.registered_codes.remove(code)
                
                # حفظ الجلسة المحدثة
                self.save_current_session()
                
                # إعادة تمكين الترتيب
                self.attendance_table.setSortingEnabled(True)
                
                QMessageBox.information(self, "تم الحذف", "تم حذف التسجيل بنجاح")
                
                # تحديث حالة الأزرار
                self.update_buttons_state()
                
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الحذف: {str(e)}")
    
    def update_buttons_state(self):
        """تحديث حالة الأزرار بناءً على عدد التسجيلات"""
        has_records = self.attendance_table.rowCount() > 0
        self.finish_btn.setEnabled(has_records)
        self.clear_btn.setEnabled(has_records)
    
    def finish_session(self):
        """إنهاء الجلسة ومسح البيانات المؤقتة"""
        if not self.registered_codes:
            QMessageBox.information(self, "معلومة", "لم يتم تسجيل أي أطفال في هذه الجلسة")
            return
        
        # إرسال إشارة أن التسجيل انتهى (للتحديث في الأقسام الأخرى)
        self.registration_finished.emit()
        
        QMessageBox.information(self, "تم إنهاء الجلسة", 
                               f"تم تسجيل {len(self.registered_codes)} طفل بنجاح\nتم مسح البيانات المؤقتة")
        
        # مسح البيانات بعد إنهاء الجلسة
        self.clear_session()
    
    def clear_session(self):
        """مسح الجلسة الحالية"""
        self.attendance_table.setRowCount(0)
        self.registered_codes.clear()
        self.info_display.clear()
        self.code_input.clear()
        self.name_input.setCurrentIndex(-1)
        self.name_input.setCurrentText("")
        self.current_selected_child = None
        self.code_input.setFocus()
        self.update_buttons_state()
        
        # مسح ملف الجلسة
        self.clear_session_file()
    
    def refresh_data(self):
        """تحديث البيانات وإعادة تحميل قائمة الأطفال"""
        try:
            self.load_children_data()
            QMessageBox.information(self, "تم التحديث", "تم تحديث بيانات الأطفال بنجاح")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء التحديث: {str(e)}")

    # الدوال الجديدة للميزة 2: البحث في الجلسة الحالية
    def search_in_current_session(self, search_text):
        """البحث في الجلسة الحالية"""
        search_text = search_text.strip()
        
        if not search_text:
            self.search_results_display.clear()
            return
        
        # تطبيع نص البحث
        normalized_search = self.normalize_arabic_text(search_text).lower()
        
        # البحث في الأطفال المسجلين في الجلسة الحالية
        found_children = []
        
        for code in self.registered_codes:
            child = self.db.get_child_by_code(code)
            if child:
                # تطبيع بيانات الطفل
                child_name = self.normalize_arabic_text(child.get('name', '')).lower()
                child_code = str(child.get('code', '')).lower()
                
                # البحث بالاسم أو الكود
                name_match = normalized_search in child_name
                code_match = normalized_search in child_code
                partial_match = any(normalized_search in self.normalize_arabic_text(str(value)).lower() 
                                  for value in child.values() if value)
                
                if name_match or code_match or partial_match:
                    found_children.append(child)
        
        # عرض النتائج
        if found_children:
            results_html = f"""
            <div style="font-family: Arial; font-size: 12px; line-height: 1.5;">
            <div style="background: #27ae60; color: white; padding: 8px; border-radius: 5px; margin-bottom: 8px;">
            <strong>🔍 تم العثور على {len(found_children)} طفل في الجلسة الحالية:</strong>
            </div>
            """
            
            for child in found_children:
                # العثور على وقت التسجيل من جدول الحضور
                arrival_time = "غير محدد"
                for row in range(self.attendance_table.rowCount()):
                    if self.attendance_table.item(row, 0) and self.attendance_table.item(row, 0).text() == str(child.get('code', '')):
                        arrival_time = self.attendance_table.item(row, 3).text()
                        break
                
                results_html += f"""
                <div style="margin-bottom: 10px; padding: 8px; background: #34495e; border-radius: 5px;">
                <div style="color: #3498db; font-weight: bold;">{child.get('name', 'غير محدد')} - الكود: {child.get('code', 'غير محدد')}</div>
                <div style="font-size: 11px;">
                <span style="color: #ecf0f1;">الصف: {child.get('class', 'غير محدد')}</span> | 
                <span style="color: #ecf0f1;">المنطقة: {child.get('region', 'غير محدد')}</span> | 
                <span style="color: #2ecc71;">وقت التسجيل: {arrival_time}</span>
                </div>
                <div style="font-size: 11px; color: #bdc3c7;">
                هاتف: {child.get('موبيل الولد', 'غير محدد')} | العنوان: {child.get('عماره', 'غير محدد')} - {child.get('شارع', 'غير محدد')}
                </div>
                </div>
                """
            
            results_html += "</div>"
            self.search_results_display.setHtml(results_html)
            
            # إذا كان هناك طفل واحد فقط، عرض تفاصيله الكاملة
            if len(found_children) == 1:
                self.show_child_details(found_children[0])
                self.code_input.setText(found_children[0].get('code', ''))
                self.name_input.setCurrentText(found_children[0].get('name', ''))
        else:
            self.search_results_display.setHtml(f"""
            <div style="font-family: Arial; font-size: 14px; text-align: center; padding: 20px;">
            <div style="color: #e74c3c; font-weight: bold;">⚠️ لم يتم العثور على الطفل في الجلسة الحالية</div>
            <div style="color: #7f8c8d; font-size: 12px; margin-top: 10px;">
            الطفل لم يسجل حضوره بعد في هذه الجلسة
            </div>
            </div>
            """)

    def clear_session_search(self):
        """مسح البحث"""
        self.session_search_input.clear()
        self.search_results_display.clear()