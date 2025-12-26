# coptic_excel_parser.py
import pandas as pd
import re
from datetime import datetime

class CopticExcelParser:
    def __init__(self):
        # الأعمدة الأساسية المطلوبة
        self.primary_columns = [
            'الاسم', 'عماره', 'شارع', 'دور', 'شقه', 'موبيل الولد', 
            'موبايل الاب', 'موبايل الام', 'تليفون'
        ]
        
        # الأعمدة الإضافية
        self.secondary_columns = [
            'منطقه', 'يوم', 'شهر', 'سنه', 'المدرسه', 'شماس', 'اب الاعتراف',
            'ملاحظات', 'تصنيف المواظبة', 'اخوة رب', 'خادم المتابعة', 'Code',
            'حضور القداس', 'اخر اعتراف'
        ]
    
    def parse_excel_file(self, file_path, existing_codes=None):
        """تحليل ملف Excel الخاص بالكنيسة بالتنسيق المحدد مع دعم الاستيراد التزايدي"""
        try:
            # قراءة ملف Excel
            df = pd.read_excel(file_path)
            
            # البحث عن الأعمدة المطلوبة بمرونة
            column_mapping = self.map_columns(df.columns)
            
            children_data = []
            skipped_count = 0
            
            for index, row in df.iterrows():
                # تجاهل الصفوف الفارغة (بدون اسم أو كود)
                if self.is_row_empty(row, column_mapping):
                    continue
                
                child_data = self.extract_child_data(row, column_mapping)
                if child_data:
                    # التحقق إذا كان الكود موجوداً مسبقاً (للاستيراد التزايدي)
                    if existing_codes and child_data['code'] in existing_codes:
                        skipped_count += 1
                        continue
                    children_data.append(child_data)
            
            print(f"تم تحليل {len(children_data)} طفل، تم تخطي {skipped_count} طفل موجود مسبقاً")
            return children_data
            
        except Exception as e:
            raise Exception(f"خطأ في تحليل ملف Excel: {str(e)}")
    
    def map_columns(self, excel_columns):
        """تعيين أعمدة Excel إلى الأعمدة المطلوبة"""
        mapping = {}
        
        # قائمة بجميع الأعمدة المحتملة
        all_columns = self.primary_columns + self.secondary_columns
        
        for required_col in all_columns:
            for excel_col in excel_columns:
                if required_col in str(excel_col):
                    mapping[required_col] = excel_col
                    break
            # إذا لم يتم العثور على العمود، نضيفه كمفتاح بقيمة فارغة
            if required_col not in mapping:
                mapping[required_col] = None
        
        return mapping
    
    def is_row_empty(self, row, column_mapping):
        """التحقق إذا كان الصف فارغاً"""
        name_col = column_mapping.get('الاسم')
        code_col = column_mapping.get('Code')
        
        # إذا كان هناك عمود اسم، نتحقق منه
        if name_col and pd.notna(row.get(name_col)):
            return False
        
        # إذا كان هناك عمود كود، نتحقق منه  
        if code_col and pd.notna(row.get(code_col)):
            return False
            
        return True
    
    def extract_child_data(self, row, column_mapping):
        """استخراج بيانات الطفل من الصف"""
        try:
            # استخراج الكود وتحديد الصف الدراسي
            code = self.extract_value(row, column_mapping, 'Code')
            
            # إذا لم يكن هناك كود، نستخدم الفهرس
            if not code or code == 'غير محدد':
                code = f"TEMP_{len(row)}"
            
            # تحديد الصف الدراسي بناءً على أول digit من الكود
            class_name = self.determine_class(code)
            
            # استخراج البيانات الأساسية
            child_data = {
                'code': code,
                'name': self.extract_value(row, column_mapping, 'الاسم'),
                'class': class_name,
                'region': self.extract_value(row, column_mapping, 'منطقه'),
                
                # البيانات الأساسية المطلوبة
                'عماره': self.extract_value(row, column_mapping, 'عماره'),
                'شارع': self.extract_value(row, column_mapping, 'شارع'),
                'دور': self.extract_value(row, column_mapping, 'دور'),
                'شقه': self.extract_value(row, column_mapping, 'شقه'),
                'موبيل الولد': self.extract_phone(row, column_mapping, 'موبيل الولد'),
                'موبايل الاب': self.extract_phone(row, column_mapping, 'موبايل الاب'),
                'موبايل الام': self.extract_phone(row, column_mapping, 'موبايل الام'),
                'تليفون': self.extract_phone(row, column_mapping, 'تليفون'),
                
                # البيانات الإضافية
                'المدرسه': self.extract_value(row, column_mapping, 'المدرسه'),
                'شماس': self.extract_value(row, column_mapping, 'شماس'),
                'اب الاعتراف': self.extract_value(row, column_mapping, 'اب الاعتراف'),
                'ملاحظات': self.extract_value(row, column_mapping, 'ملاحظات'),
                'تصنيف المواظبة': self.extract_value(row, column_mapping, 'تصنيف المواظبة'),
                'اخوة رب': self.extract_value(row, column_mapping, 'اخوة رب'),
                'حضور القداس': self.extract_value(row, column_mapping, 'حضور القداس'),
                'اخر اعتراف': self.extract_value(row, column_mapping, 'اخر اعتراف'),
                
                # عنوان مدمج للعرض
                'address': self.build_address(row, column_mapping)
            }
            
            return child_data
            
        except Exception as e:
            print(f"خطأ في استخراج بيانات الطفل: {str(e)}")
            return None
    
    def extract_value(self, row, column_mapping, column_name):
        """استخراج قيمة عمود مع التعامل مع القيم الفارغة"""
        excel_col = column_mapping.get(column_name)
        if excel_col and pd.notna(row.get(excel_col)):
            value = str(row[excel_col])
            # تنظيف القيمة من .0 في الأرقام
            if value.endswith('.0'):
                value = value[:-2]
            return value.strip()
        return 'غير محدد'
    
    def extract_phone(self, row, column_mapping, column_name):
        """استخراج وتنظيف رقم الهاتف"""
        value = self.extract_value(row, column_mapping, column_name)
        if value != 'غير محدد':
            return self.clean_phone_number(value)
        return 'غير محدد'
    
    def clean_phone_number(self, phone):
        """تنظيف رقم الهاتف"""
        if pd.isna(phone) or phone == '' or phone == 'غير محدد':
            return 'غير محدد'
        
        # إزالة أي أحرف غير رقمية
        cleaned = re.sub(r'[^\d]', '', str(phone))
        
        # إذا كان الرقم يبدأ بـ 1 وطوله 10، نضيف 0
        if cleaned.startswith('1') and len(cleaned) == 10:
            cleaned = '0' + cleaned
        
        return cleaned if len(cleaned) >= 10 else 'غير محدد'
    
    def determine_class(self, code):
        """تحديد الصف الدراسي بناءً على الكود"""
        if not code or code == 'غير محدد':
            return 'الصف الأول'
        
        # تنظيف الكود من أي أحرف غير رقمية
        clean_code = re.sub(r'[^\d]', '', str(code))
        
        if clean_code.startswith('1'):
            return 'الصف الأول'
        elif clean_code.startswith('2'):
            return 'الصف الثاني'
        elif clean_code.startswith('3'):
            return 'الصف الثالث'
        else:
            return 'الصف الأول'  # قيمة افتراضية
    
    def build_address(self, row, column_mapping):
        """بناء العنوان من الأعمدة المختلفة"""
        address_parts = []
        
        for col in ['عماره', 'شارع', 'دور', 'شقه']:
            value = self.extract_value(row, column_mapping, col)
            if value != 'غير محدد':
                address_parts.append(value)
        
        return " - ".join(address_parts) if address_parts else 'غير محدد'
    
    def validate_data(self, children_data):
        """التحقق من صحة البيانات"""
        valid_children = []
        issues = []
        
        for i, child in enumerate(children_data):
            issues_for_child = []
            
            # التحقق من الاسم (مطلوب)
            if not child.get('name') or child['name'] == 'غير محدد':
                issues_for_child.append("الاسم مفقود")
            
            if not issues_for_child:
                valid_children.append(child)
            else:
                issues.append(f"الصف {i+2}: {', '.join(issues_for_child)}")
        
        return valid_children, issues