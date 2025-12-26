import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Import UI
from ui.main_window import MainWindow

# Import Utils
from utils.style_manager import StyleManager

def main():
    """الدالة الرئيسية لتشغيل التطبيق"""
    app = QApplication(sys.argv)
    
    # دعم اللغة العربية
    app.setLayoutDirection(Qt.RightToLeft)
    app.setApplicationName("نظام الكنيسة - الحضور والغياب")
    app.setApplicationVersion("3.0")
    
    # إنشاء مجلدات إذا لم تكن موجودة
    os.makedirs("data", exist_ok=True)
    os.makedirs("icons", exist_ok=True) 
    os.makedirs("fonts", exist_ok=True)
    os.makedirs("backups", exist_ok=True)
    
    # تطبيق التنسيقات
    StyleManager.apply_styles(app)
    
    # تعيين خط افتراضي
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()