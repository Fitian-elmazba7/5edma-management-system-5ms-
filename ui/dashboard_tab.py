from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QLabel, QPushButton, QGroupBox, QComboBox, 
                             QCompleter, QTextEdit, QScrollArea)
from PyQt5.QtCore import Qt
from utils.database import DatabaseManager
from .modern_widget import ModernWidget

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display

class DashboardTab(ModernWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.all_children = []
        self.name_to_child_map = {}
        self.current_selected_child = None
        
        self.setup_ui()
        self.load_children_data()
        self.apply_scaled_stylesheet()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # --- Search Section ---
        search_group = QGroupBox("🔍 بحث عن طفل")
        search_layout = QHBoxLayout()
        
        # Code Input
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("كود الطفل...")
        self.code_input.setMaximumWidth(150)
        self.code_input.returnPressed.connect(self.search_by_code)
        
        self.search_code_btn = QPushButton("بحث بالكود")
        self.search_code_btn.clicked.connect(self.search_by_code)
        self.search_code_btn.setProperty("class", "btn-primary")
        
        # Name Input
        self.name_input = QComboBox()
        self.name_input.setEditable(True)
        self.name_input.setPlaceholderText("اسم الطفل...")
        self.name_input.setMinimumWidth(300)
        
        # Connect name search
        self.name_input.lineEdit().returnPressed.connect(self.search_by_name)
        
        self.search_name_btn = QPushButton("بحث بالاسم")
        self.search_name_btn.clicked.connect(self.search_by_name)
        self.search_name_btn.setProperty("class", "btn-primary")
        
        search_layout.addWidget(QLabel("الكود:"))
        search_layout.addWidget(self.code_input)
        search_layout.addWidget(self.search_code_btn)
        search_layout.addWidget(QLabel("الاسم:"))
        search_layout.addWidget(self.name_input)
        search_layout.addWidget(self.search_name_btn)
        search_layout.addStretch()
        
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)
        
        # --- Content Section ---
        content_layout = QHBoxLayout()
        
        # Left Side: Child Info
        self.info_display = QTextEdit()
        self.info_display.setReadOnly(True)
        self.info_display.setMaximumWidth(400)
        
        # Right Side: Stats & Graphs
        self.stats_container = QWidget()
        self.stats_layout = QVBoxLayout(self.stats_container)
        self.stats_layout.setAlignment(Qt.AlignTop)
        
        content_layout.addWidget(self.info_display)
        content_layout.addWidget(self.stats_container)
        content_layout.setStretch(0, 1) # Info takes 1 part
        content_layout.setStretch(1, 2) # Stats takes 2 parts
        
        layout.addLayout(content_layout)
        
        self.setLayout(layout)
        
    def load_children_data(self):
        """Load children data for autocomplete"""
        self.all_children = self.db.get_all_children()
        names = []
        self.name_to_child_map = {}
        
        for child in self.all_children:
            name = child.get('name', '')
            if name and name != 'غير محدد':
                names.append(name)
                self.name_to_child_map[name] = child
        
        completer = QCompleter(names)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        
        self.name_input.setCompleter(completer)
        self.name_input.clear()
        self.name_input.addItems(names)
        self.name_input.setCurrentIndex(-1)

    def search_by_code(self):
        code = self.code_input.text().strip()
        if not code:
            return
            
        child = self.db.get_child_by_code(code)
        if child:
            self.display_child(child)
            # Sync name input
            self.name_input.setCurrentText(child.get('name', ''))
        else:
            self.info_display.setText("⚠️ الكود غير موجود")
            self.clear_stats()

    def search_by_name(self):
        name = self.name_input.currentText().strip()
        if not name:
            return
            
        # Try exact match first
        child = self.name_to_child_map.get(name)
        
        if not child:
            # Try finding by looking up in values
            # (Simple fallback, typically the completer handles selection)
            for c_name, c_data in self.name_to_child_map.items():
                if name in c_name:
                    child = c_data
                    break
        
        if child:
            self.display_child(child)
            # Sync code input
            self.code_input.setText(str(child.get('code', '')))
        else:
            self.info_display.setText("⚠️ الاسم غير موجود")
            self.clear_stats()

    def display_child(self, child):
        self.current_selected_child = child
        self.show_child_details(child)
        self.show_child_stats(child)

    def show_child_details(self, child):
        details = f"""
<div style="font-family: Arial; font-size: 14px; line-height: 1.6;">
<div style="background: #8e44ad; color: white; padding: 10px; border-radius: 5px; margin-bottom: 10px; text-align: center; font-size: 18px;">
<strong>{child.get('name', 'غير محدد')}</strong>
</div>

<p><strong>الكود:</strong> {child.get('code', '-')}</p>
<p><strong>الصف:</strong> {child.get('class', '-')}</p>
<p><strong>المدرسة:</strong> {child.get('المدرسه', '-')}</p>
<p><strong>المنطقة:</strong> {child.get('region', '-')}</p>
<hr>
<p><strong>موبايل الولد:</strong> {child.get('موبيل الولد', '-')}</p>
<p><strong>موبايل الأب:</strong> {child.get('موبايل الاب', '-')}</p>
<p><strong>موبايل الأم:</strong> {child.get('موبايل الام', '-')}</p>
<p><strong>العنوان:</strong> {child.get('address', '-')}</p>
<hr>
<p><strong>ملاحظات:</strong><br>{child.get('ملاحظات', '-')}</p>
</div>
"""
        self.info_display.setHtml(details)

    def clear_stats(self):
        # Remove existing widgets in stats layout
        while self.stats_layout.count():
            item = self.stats_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def fix_text(self, text):
        """Reshapes Arabic text for correct display in matplotlib"""
        try:
            reshaped_text = arabic_reshaper.reshape(text)
            return get_display(reshaped_text)
        except:
            return text

    def show_child_stats(self, child):
        self.clear_stats()
        
        if not child:
            return

        # Calculate Stats (Logic from ChildDetailsDialog)
        all_dates = self.db.get_attendance_dates()
        total_days = len(all_dates)
        present_days = 0
        
        attendance_data = self.db.load_data().get('attendance', {})
        child_code = str(child.get('code', '')).strip()
        
        # Calculate Monthly Stats
        monthly_stats = {} # Format: "YYYY-MM": {'total': 0, 'present': 0}
        
        # Initialize months from all dates
        for date_str in all_dates:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                month_key = date_obj.strftime("%Y-%m")
                
                if month_key not in monthly_stats:
                    monthly_stats[month_key] = {'total': 0, 'present': 0}
                
                monthly_stats[month_key]['total'] += 1
                
                # Check attendance
                attendees = attendance_data.get(date_str, {})
                if child_code in attendees:
                    monthly_stats[month_key]['present'] += 1
                    
            except ValueError:
                continue

        # Aggregate total present days
        for date_str, attendees in attendance_data.items():
            if child_code in attendees:
                present_days += 1
                
        absent_days = total_days - present_days
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        # Summary Area
        summary_group = QGroupBox("ملخص الحضور")
        summary_layout = QHBoxLayout()
        
        lbl_style = "font-size: 16px; font-weight: bold; padding: 10px; border-radius: 5px;"
        
        lbl_total = QLabel(f"إجمالي الخدمة:\n{total_days} يوم")
        lbl_total.setStyleSheet(lbl_style + "background-color: #ecf0f1;")
        lbl_total.setAlignment(Qt.AlignCenter)
        
        lbl_present = QLabel(f"حضور:\n{present_days} يوم")
        lbl_present.setStyleSheet(lbl_style + "background-color: #d5f5e3; color: #2ecc71;")
        lbl_present.setAlignment(Qt.AlignCenter)
        
        lbl_absent = QLabel(f"غياب:\n{absent_days} يوم")
        lbl_absent.setStyleSheet(lbl_style + "background-color: #fadbd8; color: #e74c3c;")
        lbl_absent.setAlignment(Qt.AlignCenter)
        
        lbl_percent = QLabel(f"النسبة:\n{attendance_percentage:.1f}%")
        lbl_percent.setStyleSheet(lbl_style + "background-color: #d6eaf8; color: #3498db;")
        lbl_percent.setAlignment(Qt.AlignCenter)
        
        summary_layout.addWidget(lbl_total)
        summary_layout.addWidget(lbl_present)
        summary_layout.addWidget(lbl_absent)
        summary_layout.addWidget(lbl_percent)
        
        summary_group.setLayout(summary_layout)
        self.stats_layout.addWidget(summary_group)
        
        # Graphs Area
        if total_days > 0:
            graph_group = QGroupBox("الرسوم البيانية (تفاعلية)")
            graph_layout = QVBoxLayout()
            
            # Create Figure - Ensure font supports Arabic
            plt.rcParams['font.family'] = 'Arial'
            
            figure = Figure(figsize=(8, 8), dpi=100)
            canvas = FigureCanvas(figure)
            
            # Toolbar
            toolbar = NavigationToolbar(canvas, self)
            graph_layout.addWidget(toolbar)
            
            # 1. Pie Chart
            ax1 = figure.add_subplot(221) 
            labels = [self.fix_text('حضور'), self.fix_text('غياب')]
            sizes = [present_days, absent_days]
            colors = ['#2ecc71', '#e74c3c']
            explode = (0.1, 0)
            ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
                   autopct='%1.1f%%', shadow=True, startangle=90)
            ax1.set_title(self.fix_text("نسبة الحضور الإجمالية"))
            
            # 2. Bar Chart (Total vs Present)
            ax2 = figure.add_subplot(222)
            categories = [self.fix_text('إجمالي الأيام'), self.fix_text('أيام الحضور')]
            values = [total_days, present_days]
            bar_colors = ['#95a5a6', '#2ecc71']
            ax2.bar(categories, values, color=bar_colors)
            ax2.set_title(self.fix_text("مقارنة الحضور"))
            ax2.set_ylabel(self.fix_text("عدد الأيام"))
            
            # 3. Monthly Trend (Line Chart)
            ax3 = figure.add_subplot(212) # Bottom row, spanning both columns (conceptually, though subplot grid logic varies)
            # To strictly span, usually we use GridSpec, but 212 works well for "2 rows, 1 solumn, index 2" in a different grid concept.
            # But mixing 22x and 21x can be tricky in simple logic.
            # Let's use GridSpec for cleaner layout
            
            figure.clear()
            gs = figure.add_gridspec(2, 2)
            
            # Re-add Pie
            ax1 = figure.add_subplot(gs[0, 0])
            ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
                   autopct='%1.1f%%', shadow=True, startangle=90)
            ax1.set_title(self.fix_text("نسبة الحضور الإجمالية"))
            
            # Re-add Bar
            ax2 = figure.add_subplot(gs[0, 1])
            ax2.bar(categories, values, color=bar_colors)
            ax2.set_title(self.fix_text("مقارنة الحضور"))
            
            # Monthly Trend
            ax3 = figure.add_subplot(gs[1, :]) # Span entire bottom row
            
            # Prepare data for line chart
            sorted_months = sorted(monthly_stats.keys())
            x_months = []
            y_percents = []
            
            for m in sorted_months:
                stats = monthly_stats[m]
                pct = (stats['present'] / stats['total'] * 100) if stats['total'] > 0 else 0
                x_months.append(m)
                y_percents.append(pct)
            
            if x_months:
                ax3.plot(x_months, y_percents, marker='o', linestyle='-', color='#3498db', linewidth=2)
                ax3.set_title(self.fix_text("تطور نسبة الحضور شهرياً"))
                ax3.set_ylabel(self.fix_text("نسبة الحضور %"))
                ax3.set_xlabel(self.fix_text("الشهر"))
                ax3.grid(True, linestyle='--', alpha=0.7)
                
                # Rotate x labels if many
                plt.setp(ax3.get_xticklabels(), rotation=45, ha="right")
            else:
                ax3.text(0.5, 0.5, self.fix_text("لا توجد بيانات شهرية كافية"), 
                        horizontalalignment='center', verticalalignment='center', transform=ax3.transAxes)

            figure.tight_layout()
            
            graph_layout.addWidget(canvas)
            graph_group.setLayout(graph_layout)
            self.stats_layout.addWidget(graph_group)
        else:
            self.stats_layout.addWidget(QLabel("لا توجد بيانات كافية لعرض الرسوم البيانية"))
            
        self.stats_layout.addStretch()

    def apply_scaled_stylesheet(self):
        pass
