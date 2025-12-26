from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QComboBox, QTextEdit, QPushButton, 
                             QFormLayout, QMessageBox)
from PyQt5.QtCore import Qt

class AddChildDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("إضافة طفل جديد")
        self.setModal(True)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        self.code_input = QLineEdit()
        self.name_input = QLineEdit()
        self.class_input = QComboBox()
        # استخدام الأسماء العربية للصفوف
        self.class_input.addItems(["الصف الأول", "الصف الثاني", "الصف الثالث"])
        
        self.region_input = QLineEdit()
        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(80)
        
        self.phone_input = QLineEdit()
        self.father_phone_input = QLineEdit()
        self.mother_phone_input = QLineEdit()
        self.home_phone_input = QLineEdit()
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(80)
        
        form_layout.addRow("الكود:", self.code_input)
        form_layout.addRow("الاسم:", self.name_input)
        form_layout.addRow("الصف:", self.class_input)
        form_layout.addRow("المنطقة:", self.region_input)
        form_layout.addRow("العنوان:", self.address_input)
        form_layout.addRow("موبيل الولد:", self.phone_input)
        form_layout.addRow("موبايل الأب:", self.father_phone_input)
        form_layout.addRow("موبايل الأم:", self.mother_phone_input)
        form_layout.addRow("تليفون المنزل:", self.home_phone_input)
        form_layout.addRow("ملاحظات:", self.notes_input)
        
        # أزرار
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("حفظ")
        self.cancel_btn = QPushButton("إلغاء")
        
        self.save_btn.clicked.connect(self.validate_and_save)
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def validate_and_save(self):
        if not self.code_input.text().strip():
            QMessageBox.warning(self, "تحذير", "يرجى إدخال كود الطفل")
            return
            
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "تحذير", "يرجى إدخال اسم الطفل")
            return
            
        self.accept()
    
    def get_child_data(self):
        return {
            'code': self.code_input.text().strip(),
            'name': self.name_input.text().strip(),
            'class': self.class_input.currentText(),
            'region': self.region_input.text().strip(),
            'address': self.address_input.toPlainText().strip(),
            'موبيل الولد': self.phone_input.text().strip(),
            'موبايل الاب': self.father_phone_input.text().strip(),
            'موبايل الام': self.mother_phone_input.text().strip(),
            'تليفون': self.home_phone_input.text().strip(),
            'ملاحظات': self.notes_input.toPlainText().strip()
        }