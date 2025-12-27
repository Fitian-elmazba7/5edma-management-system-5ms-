# dashboard_tab.py - Dashboard Grid Layout with Stats and Charts
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QLabel, QPushButton, QGroupBox, QComboBox, 
                             QCompleter, QTextEdit, QScrollArea, QFrame)
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
        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(24, 24, 24, 24)
        
        # ═══════════════════════════════════════════════════════════════
        # ROW 1: SEARCH CARD (Full Width)
        # ═══════════════════════════════════════════════════════════════
        search_card = QFrame()
        search_card.setProperty("class", "dashboard-card")
        search_card_layout = QVBoxLayout(search_card)
        search_card_layout.setSpacing(16)
        search_card_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_row = QHBoxLayout()
        header_icon = QLabel("🔍")
        header_icon.setProperty("class", "card-icon")
        header_title = QLabel("بحث عن طفل")
        header_title.setProperty("class", "card-title")
        header_row.addWidget(header_icon)
        header_row.addWidget(header_title)
        header_row.addStretch()
        search_card_layout.addLayout(header_row)
        
        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setProperty("class", "card-separator")
        search_card_layout.addWidget(sep)
        
        # Search Inputs Row
        search_row = QHBoxLayout()
        search_row.setSpacing(16)
        
        # Code Input
        code_label = QLabel("الكود:")
        code_label.setProperty("class", "input-label")
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("كود الطفل...")
        self.code_input.setProperty("class", "dashboard-input")
        self.code_input.setMinimumHeight(44)
        self.code_input.setMaximumWidth(180)
        self.code_input.returnPressed.connect(self.search_by_code)
        
        self.search_code_btn = QPushButton("بحث")
        self.search_code_btn.clicked.connect(self.search_by_code)
        self.search_code_btn.setProperty("class", "btn-success")
        self.search_code_btn.setMinimumHeight(44)
        
        # Name Input
        name_label = QLabel("الاسم:")
        name_label.setProperty("class", "input-label")
        self.name_input = QComboBox()
        self.name_input.setEditable(True)
        self.name_input.setPlaceholderText("اسم الطفل...")
        self.name_input.setProperty("class", "dashboard-combo")
        self.name_input.setMinimumHeight(44)
        self.name_input.setMinimumWidth(300)
        self.name_input.lineEdit().returnPressed.connect(self.search_by_name)
        
        self.search_name_btn = QPushButton("بحث")
        self.search_name_btn.clicked.connect(self.search_by_name)
        self.search_name_btn.setProperty("class", "btn-secondary")
        self.search_name_btn.setMinimumHeight(44)
        
        search_row.addWidget(code_label)
        search_row.addWidget(self.code_input)
        search_row.addWidget(self.search_code_btn)
        search_row.addSpacing(20)
        search_row.addWidget(name_label)
        search_row.addWidget(self.name_input, 1)
        search_row.addWidget(self.search_name_btn)
        
        search_card_layout.addLayout(search_row)
        main_layout.addWidget(search_card)
        
        # ═══════════════════════════════════════════════════════════════
        # ROW 2: INFO CARD + STATS CARD (2 columns)
        # ═══════════════════════════════════════════════════════════════
        content_row = QHBoxLayout()
        content_row.setSpacing(16)
        
        # LEFT: Child Info Card
        info_card = QFrame()
        info_card.setProperty("class", "dashboard-card")
        info_card_layout = QVBoxLayout(info_card)
        info_card_layout.setSpacing(12)
        info_card_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        info_header = QHBoxLayout()
        info_icon = QLabel("📋")
        info_icon.setProperty("class", "card-icon")
        info_title = QLabel("بيانات الطفل")
        info_title.setProperty("class", "card-title")
        info_header.addWidget(info_icon)
        info_header.addWidget(info_title)
        info_header.addStretch()
        info_card_layout.addLayout(info_header)
        
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        sep2.setProperty("class", "card-separator")
        info_card_layout.addWidget(sep2)
        
        self.info_display = QTextEdit()
        self.info_display.setReadOnly(True)
        self.info_display.setProperty("class", "info-display")
        info_card_layout.addWidget(self.info_display, 1)
        
        content_row.addWidget(info_card, 1)
        
        # RIGHT: Stats & Graphs Container
        self.stats_card = QFrame()
        self.stats_card.setProperty("class", "dashboard-card")
        stats_card_layout = QVBoxLayout(self.stats_card)
        stats_card_layout.setSpacing(12)
        stats_card_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        stats_header = QHBoxLayout()
        stats_icon = QLabel("📊")
        stats_icon.setProperty("class", "card-icon")
        stats_title = QLabel("إحصائيات الحضور")
        stats_title.setProperty("class", "card-title")
        stats_header.addWidget(stats_icon)
        stats_header.addWidget(stats_title)
        stats_header.addStretch()
        stats_card_layout.addLayout(stats_header)
        
        sep3 = QFrame()
        sep3.setFrameShape(QFrame.HLine)
        sep3.setProperty("class", "card-separator")
        stats_card_layout.addWidget(sep3)
        
        # Stats Container (will be populated dynamically)
        self.stats_container = QWidget()
        self.stats_layout = QVBoxLayout(self.stats_container)
        self.stats_layout.setAlignment(Qt.AlignTop)
        self.stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_card_layout.addWidget(self.stats_container, 1)
        
        content_row.addWidget(self.stats_card, 2)
        
        main_layout.addLayout(content_row, 1)
        
        self.setLayout(main_layout)
        
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
            self.name_input.setCurrentText(child.get('name', ''))
        else:
            self.info_display.setHtml("<div dir='rtl' style='color: #f59e0b; text-align: center; padding: 30px;'>⚠️ الكود غير موجود</div>")
            self.clear_stats()

    def search_by_name(self):
        name = self.name_input.currentText().strip()
        if not name:
            return
            
        child = self.name_to_child_map.get(name)
        
        if not child:
            for c_name, c_data in self.name_to_child_map.items():
                if name in c_name:
                    child = c_data
                    break
        
        if child:
            self.display_child(child)
            self.code_input.setText(str(child.get('code', '')))
        else:
            self.info_display.setHtml("<div dir='rtl' style='color: #f59e0b; text-align: center; padding: 30px;'>⚠️ الاسم غير موجود</div>")
            self.clear_stats()

    def display_child(self, child):
        self.current_selected_child = child
        self.show_child_details(child)
        self.show_child_stats(child)

    def show_child_details(self, child):
        details = f"""
<div dir="rtl" style="font-family: 'Segoe UI'; color: #e2e8f0; line-height: 1.8; text-align: right;">
<div style="background: linear-gradient(135deg, #22c55e, #16a34a); color: white; padding: 14px; border-radius: 10px; text-align: center; font-size: 16px; font-weight: 600; margin-bottom: 16px;">
{child.get('name', 'غير محدد')}
</div>
<table style="width: 100%; font-size: 13px; text-align: right;">
<tr><td style="font-weight: 500;">{child.get('code', '-')}</td><td style="color: #94a3b8; padding: 6px 0; width: 100px;">الكود:</td></tr>
<tr><td>{child.get('class', '-')}</td><td style="color: #94a3b8; padding: 6px 0;">الصف:</td></tr>
<tr><td>{child.get('المدرسه', '-')}</td><td style="color: #94a3b8; padding: 6px 0;">المدرسة:</td></tr>
<tr><td>{child.get('region', '-')}</td><td style="color: #94a3b8; padding: 6px 0;">المنطقة:</td></tr>
<tr><td colspan="2" style="border-top: 1px solid #1e1e2e; padding-top: 10px;"></td></tr>
<tr><td>{child.get('موبيل الولد', '-')}</td><td style="color: #94a3b8; padding: 6px 0;">موبايل الولد:</td></tr>
<tr><td>{child.get('موبايل الاب', '-')}</td><td style="color: #94a3b8; padding: 6px 0;">موبايل الأب:</td></tr>
<tr><td>{child.get('موبايل الام', '-')}</td><td style="color: #94a3b8; padding: 6px 0;">موبايل الأم:</td></tr>
<tr><td>{child.get('address', '-')}</td><td style="color: #94a3b8; padding: 6px 0;">العنوان:</td></tr>
</table>
<div style="margin-top: 12px; padding: 10px; background: #1e1e2e; border-radius: 8px; text-align: right;">
<span style="color: #94a3b8;">ملاحظات:</span><br>
<span style="color: #e2e8f0;">{child.get('ملاحظات', '-')}</span>
</div>
</div>
"""
        self.info_display.setHtml(details)

    def clear_stats(self):
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

        # Calculate Stats
        all_dates = self.db.get_attendance_dates()
        total_days = len(all_dates)
        present_days = 0
        
        attendance_data = self.db.load_data().get('attendance', {})
        child_code = str(child.get('code', '')).strip()
        
        # Calculate Monthly Stats
        monthly_stats = {}
        
        for date_str in all_dates:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                month_key = date_obj.strftime("%Y-%m")
                
                if month_key not in monthly_stats:
                    monthly_stats[month_key] = {'total': 0, 'present': 0}
                
                monthly_stats[month_key]['total'] += 1
                
                attendees = attendance_data.get(date_str, {})
                if child_code in attendees:
                    monthly_stats[month_key]['present'] += 1
                    
            except ValueError:
                continue

        for date_str, attendees in attendance_data.items():
            if child_code in attendees:
                present_days += 1
                
        absent_days = total_days - present_days
        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
        
        # Stats Cards Row
        stats_row = QHBoxLayout()
        stats_row.setSpacing(12)
        
        self.stats_layout.addLayout(stats_row)
        
        # Create mini stat cards
        stats_row.addWidget(self.create_mini_stat("إجمالي", str(total_days), "#64748b"))
        stats_row.addWidget(self.create_mini_stat("حضور", str(present_days), "#22c55e"))
        stats_row.addWidget(self.create_mini_stat("غياب", str(absent_days), "#ef4444"))
        stats_row.addWidget(self.create_mini_stat("النسبة", f"{attendance_percentage:.0f}%", "#3b82f6"))
        
        # Graphs Area
        if total_days > 0:
            plt.rcParams['font.family'] = 'Arial'
            plt.rcParams['axes.facecolor'] = '#141420'
            plt.rcParams['figure.facecolor'] = '#141420'
            plt.rcParams['text.color'] = '#e2e8f0'
            plt.rcParams['axes.labelcolor'] = '#94a3b8'
            plt.rcParams['xtick.color'] = '#64748b'
            plt.rcParams['ytick.color'] = '#64748b'
            
            figure = Figure(figsize=(8, 6), dpi=100, facecolor='#141420')
            canvas = FigureCanvas(figure)
            
            gs = figure.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
            
            # Pie Chart
            ax1 = figure.add_subplot(gs[0, 0])
            ax1.set_facecolor('#141420')
            labels = [self.fix_text('حضور'), self.fix_text('غياب')]
            sizes = [present_days, absent_days]
            colors = ['#22c55e', '#ef4444']
            ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%', startangle=90,
                   textprops={'color': '#e2e8f0'})
            ax1.set_title(self.fix_text("نسبة الحضور"), color='#e2e8f0')
            
            # Bar Chart
            ax2 = figure.add_subplot(gs[0, 1])
            ax2.set_facecolor('#141420')
            categories = [self.fix_text('إجمالي'), self.fix_text('حضور')]
            values = [total_days, present_days]
            bar_colors = ['#64748b', '#22c55e']
            ax2.bar(categories, values, color=bar_colors)
            ax2.set_title(self.fix_text("مقارنة"), color='#e2e8f0')
            
            # Monthly Trend
            ax3 = figure.add_subplot(gs[1, :])
            ax3.set_facecolor('#141420')
            
            sorted_months = sorted(monthly_stats.keys())
            x_months = []
            y_percents = []
            
            for m in sorted_months:
                stats = monthly_stats[m]
                pct = (stats['present'] / stats['total'] * 100) if stats['total'] > 0 else 0
                x_months.append(m)
                y_percents.append(pct)
            
            if x_months:
                ax3.plot(x_months, y_percents, marker='o', linestyle='-', color='#3b82f6', linewidth=2)
                ax3.fill_between(x_months, y_percents, alpha=0.2, color='#3b82f6')
                ax3.set_title(self.fix_text("تطور الحضور شهرياً"), color='#e2e8f0')
                ax3.grid(True, linestyle='--', alpha=0.3, color='#334155')
                plt.setp(ax3.get_xticklabels(), rotation=45, ha="right")
            
            self.stats_layout.addWidget(canvas)
        else:
            no_data = QLabel("لا توجد بيانات كافية")
            no_data.setProperty("class", "stat-subtitle")
            no_data.setAlignment(Qt.AlignCenter)
            self.stats_layout.addWidget(no_data)
            
        self.stats_layout.addStretch()

    def create_mini_stat(self, title, value, color):
        """Create a mini stat card"""
        card = QFrame()
        card.setProperty("class", "stat-card")
        layout = QVBoxLayout(card)
        layout.setSpacing(4)
        layout.setContentsMargins(16, 12, 16, 12)
        
        value_lbl = QLabel(value)
        value_lbl.setStyleSheet(f"font-size: 24px; font-weight: 700; color: {color};")
        value_lbl.setAlignment(Qt.AlignCenter)
        
        title_lbl = QLabel(title)
        title_lbl.setProperty("class", "stat-subtitle")
        title_lbl.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(value_lbl)
        layout.addWidget(title_lbl)
        
        return card

    def apply_scaled_stylesheet(self):
        pass
