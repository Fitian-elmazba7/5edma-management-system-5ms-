import sys
import os
import shutil
import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, 
                             QWidget, QMessageBox, QToolBar, QAction, QHBoxLayout,
                             QPushButton, QLabel, QFrame, QStatusBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFontDatabase, QFont
from ui.comparison_report import ComparisonReportTab
from ui.main_window import MainWindow
from ui.absence import AbsenceTab
from ui.data_management import DataManagementTab
from ui.early_arrival import EarlyArrivalTab
from ui.attendance_report import AttendanceReportTab

class ChurchAttendanceSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("𓆓 نظام الحضور والغياب - الكنيسة القبطية الأرثوذكسية 𓆓")
        self.setGeometry(100, 100, 1400, 900)
        
        # تحميل الخط العربي
        self.load_arabic_font()
        
        # تعيين الأيقونة
        self.setWindowIcon(QIcon("icons/icon.ico"))
        
        self.setup_ui()
        self.apply_stylesheet()
        
    def load_arabic_font(self):
        """تحميل الخط العربي"""
        font_paths = [
            "fonts/arial.ttf",
            "fonts/tahoma.ttf", 
            "fonts/arabic_font.ttf"
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                QFontDatabase.addApplicationFont(font_path)
        
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        # إنشاء الشريط العلوي
        self.create_top_toolbar()
        
        # إنشاء التبويبات الرئيسية
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabPosition(QTabWidget.North)
        
        # تبويب التسجيل
        self.registration_tab = MainWindow()
        self.tabs.addTab(self.registration_tab, "𓃭 التسجيل اليومي")
       
        # تبويب الغياب
        self.absence_tab = AbsenceTab()
        self.tabs.addTab(self.absence_tab, "𓃻 تقرير الغياب")
        
        # تبويب إدارة البيانات
        self.data_tab = DataManagementTab()
        self.tabs.addTab(self.data_tab, "𓃰 إدارة البيانات")
        
        # تبويب الحضور المبكر
        self.early_arrival_tab = EarlyArrivalTab()
        self.tabs.addTab(self.early_arrival_tab, "𓃷 الحضور المبكر")
        
        # تبويب تقرير الحضور
        self.attendance_report_tab = AttendanceReportTab()
        self.tabs.addTab(self.attendance_report_tab, "𓃭 تقرير الحضور")

         #التقارير
        self.comparison_report_tab = ComparisonReportTab()
        self.tabs.addTab(self.comparison_report_tab, "📊 تقارير المقارنة")
        # ربط الإشارات
        self.registration_tab.registration_finished.connect(self.absence_tab.load_absence_data)
        self.registration_tab.registration_finished.connect(self.early_arrival_tab.load_dates)
        
        self.setCentralWidget(self.tabs)
        
        # إنشاء شريط الحالة مع النص المطلوب
        self.create_status_bar()

    def create_status_bar(self):
        """إنشاء شريط الحالة مع النص المطلوب"""
        status_bar = QStatusBar()
        
        # النص باللغة الإنجليزية كما طلبت
        credit_label = QLabel("Done by Youssef Magdy 5admet fetian el masba7")
        credit_label.setAlignment(Qt.AlignCenter)
        credit_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-weight: bold;
                font-size: 12px;
                padding: 5px;
                background-color: #ecf0f1;
                border-radius: 3px;
            }
        """)
        
        # إضافة التسمية إلى شريط الحالة
        status_bar.addPermanentWidget(credit_label)
        
        # تعيين شريط الحالة للنافذة الرئيسية
        self.setStatusBar(status_bar)
        
        # عرض رسالة ترحيب في شريط الحالة
        status_bar.showMessage("مرحباً بك في نظام الحضور والغياب - الكنيسة القبطية الأرثوذكسية", 5000)

    def create_top_toolbar(self):
        """إنشاء الشريط العلوي مع زر التحديث الشامل"""
        # إنشاء إطار علوي
        top_frame = QFrame()
        top_frame.setObjectName("topFrame")
        top_frame.setFixedHeight(70)
        
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(15, 5, 15, 5)
        
        # عنوان التطبيق
        title_label = QLabel("𓆓 نظام الحضور والغياب - الكنيسة القبطية الأرثوذكسية 𓆓")
        title_label.setObjectName("appTitle")
        title_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # زر التحديث الشامل
        refresh_layout = QVBoxLayout()
        refresh_layout.setSpacing(2)
        
        self.global_refresh_btn = QPushButton("🔄 تحديث شامل للنظام")
        self.global_refresh_btn.setObjectName("globalRefreshBtn")
        self.global_refresh_btn.setFixedSize(200, 35)
        self.global_refresh_btn.setToolTip("تحديث جميع البيانات في جميع أقسام النظام")
        self.global_refresh_btn.clicked.connect(self.refresh_all_tabs)
        
        # تعيين خط واضح للنص
        font = self.global_refresh_btn.font()
        font.setPointSize(10)
        font.setBold(True)
        self.global_refresh_btn.setFont(font)
        
        self.refresh_info = QLabel("آخر تحديث: لم يتم التحديث بعد")
        self.refresh_info.setObjectName("refreshInfo")
        self.refresh_info.setAlignment(Qt.AlignCenter)
        
        refresh_layout.addWidget(self.global_refresh_btn)
        refresh_layout.addWidget(self.refresh_info)
        
        # إضافة العناصر إلى التخطيط
        top_layout.addWidget(title_label)
        top_layout.addStretch()
        top_layout.addLayout(refresh_layout)
        
        top_frame.setLayout(top_layout)
        
        # إضافة الإطار كشريط أدوات
        toolbar = QToolBar("الشريط العلوي")
        toolbar.setMovable(False)
        toolbar.addWidget(top_frame)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

    def refresh_all_tabs(self):
        """تحديث جميع التبويبات بشكل شامل"""
        try:
            from datetime import datetime
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # تحديث جميع التبويبات
            refresh_operations = [
                (self.registration_tab, 'refresh_data'),
                (self.absence_tab, 'refresh_data'), 
                (self.data_tab, 'load_children_data'),
                (self.early_arrival_tab, 'refresh_data'),
                (self.attendance_report_tab, 'refresh_data'),
                (self.comparison_report_tab, 'refresh_data')
            ]
            
            for tab, method_name in refresh_operations:
                if hasattr(tab, method_name):
                    method = getattr(tab, method_name)
                    method()
            
            # تحديث معلومات التحديث
            self.refresh_info.setText(f"آخر تحديث: {current_time}")
            
            # تحديث شريط الحالة
            self.statusBar().showMessage(f"تم التحديث الشامل للنظام - {current_time}", 3000)
            
            QMessageBox.information(self, "✅ تم التحديث الشامل", 
                                  f"تم تحديث جميع البيانات في النظام بنجاح\nوقت التحديث: {current_time}")
            
        except Exception as e:
            QMessageBox.critical(self, "❌ خطأ", f"حدث خطأ أثناء التحديث الشامل: {str(e)}")

    def apply_stylesheet(self):
        """تطبيق التنسيقات على الواجهة"""
        stylesheet = """
        /* التنسيقات الرئيسية */
        QMainWindow {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 #f8f9fa, stop: 1 #e9ecef);
            font-family: "Segoe UI", "Arial", "Tahoma";
        }
        
        /* شريط الحالة */
        QStatusBar {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #34495e, stop: 1 #2c3e50);
            color: white;
            font-size: 11px;
            padding: 5px;
        }
        
        QStatusBar::item {
            border: none;
        }
        
        /* الإطار العلوي */
        #topFrame {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #2c3e50, stop:0.5 #34495e, stop:1 #2c3e50);
            border-bottom: 3px solid #3498db;
        }
        
        /* عنوان التطبيق */
        #appTitle {
            font-size: 18px;
            font-weight: bold;
            color: white;
            padding: 8px 15px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #e74c3c, stop:0.5 #c0392b, stop:1 #e74c3c);
            border-radius: 8px;
            border: 2px solid #c0392b;
            min-height: 20px;
        }
        
        /* زر التحديث الشامل - إصلاح مشكلة النص */
        #globalRefreshBtn {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #27ae60, stop: 0.5 #2ecc71, stop: 1 #27ae60);
            border: 2px solid #219653;
            border-radius: 6px;
            color: #ffffff;
            font-weight: bold;
            font-size: 11px;
            padding: 5px;
            min-width: 180px;
            min-height: 30px;
        }
        
        #globalRefreshBtn:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #2ecc71, stop: 0.5 #27ae60, stop: 1 #2ecc71);
            border: 2px solid #27ae60;
            color: #ffffff;
        }
        
        #globalRefreshBtn:pressed {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #219653, stop: 1 #1e8449);
            color: #ffffff;
        }
        
        /* معلومات التحديث */
        #refreshInfo {
            font-size: 10px;
            color: #bdc3c7;
            font-weight: bold;
            background-color: rgba(0, 0, 0, 0.3);
            padding: 2px 6px;
            border-radius: 3px;
        }
        
        /* تبويبات */
        QTabWidget::pane {
            border: 2px solid #C2C7CB;
            background-color: white;
            border-radius: 8px;
            margin-top: 5px;
        }
        
        QTabWidget::tab-bar {
            alignment: center;
        }
        
        QTabBar::tab {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
            border: 2px solid #C4C4C3;
            border-bottom-color: #C2C7CB;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            min-width: 180px;
            padding: 10px;
            margin: 2px;
            font-size: 13px;
            font-weight: bold;
            color: #2c3e50;
        }
        
        QTabBar::tab:selected {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #3498db, stop: 1 #2980b9);
            color: white;
        }
        
        QTabBar::tab:hover:!selected {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #5dade2, stop: 1 #3498db);
            color: white;
        }
        
        /* شريط الأدوات */
        QToolBar {
            background: transparent;
            border: none;
            spacing: 0px;
            padding: 0px;
        }
        
        /* الأزرار العامة */
        QPushButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #3498db, stop: 1 #2980b9);
            border: 1px solid #2574a9;
            border-radius: 5px;
            color: white;
            font-weight: bold;
            font-size: 11px;
            padding: 6px 12px;
            min-width: 80px;
            min-height: 25px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #5dade2, stop: 1 #3498db);
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #2471a3, stop: 1 #1b4f72);
        }
        
        /* حقول الإدخال */
        QLineEdit, QComboBox, QTextEdit {
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            padding: 6px;
            font-size: 12px;
            background-color: white;
            color: #2c3e50;
            selection-background-color: #3498db;
        }
        
        QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
            border-color: #3498db;
        }
        
        /* الجداول */
        QTableWidget {
            background-color: white;
            alternate-background-color: #f8f9fa;
            selection-background-color: #3498db;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            gridline-color: #dee2e6;
            font-size: 11px;
        }
        
        QTableWidget::item {
            padding: 6px;
            border-bottom: 1px solid #dee2e6;
            color: #2c3e50;
        }
        
        QTableWidget::item:selected {
            background-color: #3498db;
            color: white;
        }
        
        /* رؤوس الجداول */
        QHeaderView::section {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #34495e, stop: 1 #2c3e50);
            color: white;
            padding: 8px;
            border: 1px solid #1a252f;
            font-weight: bold;
            font-size: 11px;
        }
        
        /* المجموعات */
        QGroupBox {
            font-weight: bold;
            font-size: 13px;
            border: 2px solid #bdc3c7;
            border-radius: 6px;
            margin-top: 8px;
            padding-top: 8px;
            background-color: #ecf0f1;
            color: #2c3e50;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 8px;
            background-color: #3498db;
            color: white;
            border-radius: 3px;
        }
        
        /* التسميات */
        QLabel {
            color: #2c3e50;
            font-size: 11px;
        }
        """
        self.setStyleSheet(stylesheet)

    def closeEvent(self, event):
        """تنفيذ إجراءات عند إغلاق التطبيق مع حفظ النسخ الاحتياطية"""
        try:
            # حفظ أي بيانات مؤقتة قبل الإغلاق
            if hasattr(self.registration_tab, 'save_current_session'):
                self.registration_tab.save_current_session()
            
            # إنشاء نسخة احتياطية من قاعدة البيانات
            backup_dir = "backups"
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"database_backup_{timestamp}.json")
            
            if os.path.exists("data/database.json"):
                shutil.copy2("data/database.json", backup_file)
                
        except Exception as e:
            print(f"Backup error: {e}")
        
        # المتابعة بالإغلاق العادي
        reply = QMessageBox.question(self, "تأكيد الخروج",
                                   "هل أنت متأكد من رغبتك في إغلاق النظام؟\nسيتم حفظ جميع البيانات تلقائياً.",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

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
    os.makedirs("backups", exist_ok=True)  # إنشاء مجلد النسخ الاحتياطية
    
    # تعيين خط افتراضي
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    window = ChurchAttendanceSystem()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()