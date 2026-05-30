import os
import shutil
import datetime
from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, 
                             QWidget, QMessageBox, QToolBar, QHBoxLayout,
                             QPushButton, QLabel, QFrame, QStatusBar, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFontDatabase, QFont

# Import Tabs
from .registration_tab import RegistrationTab
from .absence import AbsenceTab
from .data_management import DataManagementTab
from .early_arrival import EarlyArrivalTab
from .attendance_report import AttendanceReportTab
from .comparison_report import ComparisonReportTab
from .dashboard_tab import DashboardTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("𓆓 نظام الحضور والغياب - الكنيسة القبطية الأرثوذكسية 𓆓")
        self.setGeometry(50, 50, 1200, 680)
        
        # تحميل الخط العربي
        self.load_arabic_font()
        
        # تعيين الأيقونة
        self.setWindowIcon(QIcon("icons/icon.ico"))
        
        self.setup_ui()
        
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
        
        # تبويب التسجيل (كان يسمى MainWindow سابقاً)
        self.registration_tab = RegistrationTab()
        self.tabs.addTab(self.registration_tab, "𓃭 التسجيل اليومي")
        
        # تبويب لوحة البيانات (Dashboard)
        self.dashboard_tab = DashboardTab()
        self.tabs.addTab(self.dashboard_tab, "📈 لوحة البيانات")
       
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
        
        # إنشاء شريط الحالة
        self.create_status_bar()

    def create_status_bar(self):
        """إنشاء شريط الحالة مع النص المطلوب"""
        status_bar = QStatusBar()
        
        credit_label = QLabel("Done by Youssef Magdy 5admet fetian el masba7")
        credit_label.setAlignment(Qt.AlignCenter)
        # Using class name for styling from main.qss if supported, or setting property
        credit_label.setProperty("class", "credit-label")
        
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
        top_layout.setContentsMargins(16, 8, 16, 8)
        top_layout.setSpacing(16)
        
        # عنوان التطبيق
        title_label = QLabel("𓆓 نظام الحضور والغياب - الكنيسة القبطية الأرثوذكسية 𓆓")
        title_label.setObjectName("appTitle")
        title_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # زر التحديث الشامل
        refresh_layout = QVBoxLayout()
        refresh_layout.setSpacing(6)
        refresh_layout.setContentsMargins(0, 0, 0, 0)
        
        self.global_refresh_btn = QPushButton("🔄 تحديث شامل للنظام")
        self.global_refresh_btn.setObjectName("globalRefreshBtn")
        self.global_refresh_btn.setProperty("class", "btn-success")
        self.global_refresh_btn.setFixedSize(180, 36)
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
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # تحديث جميع التبويبات
            refresh_operations = [
                (self.registration_tab, 'refresh_data'),
                (self.absence_tab, 'refresh_data'), 
                (self.data_tab, 'load_children_data'),
                (self.early_arrival_tab, 'refresh_data'),
                (self.attendance_report_tab, 'refresh_data'),
                (self.comparison_report_tab, 'refresh_data'),
                (self.dashboard_tab, 'load_children_data')
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
