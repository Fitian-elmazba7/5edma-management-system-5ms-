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
    
    # تحميل الخطوط المخصصة من مجلد fonts (اختياري)
    from PyQt5.QtGui import QFontDatabase
    font_files = [
        "fonts/TufuliArabicDEMO-Regular.otf",
        "fonts/TufuliArabicDEMO-Bold.otf",
        "fonts/TufuliArabicDEMO-Light.otf"
    ]
    for font_file in font_files:
        if os.path.exists(font_file):
            QFontDatabase.addApplicationFont(font_file)
    
    # استخدام Segoe UI لأنه يدعم الأرقام الغربية بشكل صحيح
    font = QFont("Segoe UI", 10)
    font.setStyleStrategy(QFont.PreferAntialias)
    app.setFont(font)
    
    window = MainWindow()
    window.showMaximized()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()