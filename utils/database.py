import json
import os
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, db_file="data/database.json"):
        self.db_file = db_file
        self.arabic_classes = ['الصف الأول', 'الصف الثاني', 'الصف الثالث']
        self.arabic_days = {
            'Saturday': 'السبت',
            'Sunday': 'الأحد', 
            'Monday': 'الاثنين',
            'Tuesday': 'الثلاثاء',
            'Wednesday': 'الأربعاء',
            'Thursday': 'الخميس',
            'Friday': 'الجمعة'
        }
        self.ensure_database_exists()
    
    def ensure_database_exists(self):
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
        
        if not os.path.exists(self.db_file):
            initial_data = {
                "children": [],
                "attendance": {},
                "settings": {
                    "service_day": "Thursday",  # Default to Thursday
                    "service_time": "19:00"     # Default to 7 PM
                },
                "modification_tracking": {
                    "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "modification_count": 0
                }
            }
            self.save_data(initial_data)
    
    def load_data(self):
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                "children": [], 
                "attendance": {}, 
                "settings": {
                    "service_day": "Thursday", 
                    "service_time": "19:00"
                },
                "modification_tracking": {
                    "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "modification_count": 0
                }
            }
    
    def save_data(self, data):
        # Update modification tracking
        if "modification_tracking" not in data:
            data["modification_tracking"] = {
                "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "modification_count": 0
            }
        else:
            data["modification_tracking"]["last_modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data["modification_tracking"]["modification_count"] += 1
        
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def save_immediate_attendance(self, code, date=None, time=None):
        """حفظ الحضور فوراً عند التسجيل"""
        data = self.load_data()
        
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        if time is None:
            time = datetime.now().strftime("%H:%M")
        
        if date not in data['attendance']:
            data['attendance'][date] = {}
        
        data['attendance'][date][code] = time
        self.save_data(data)
        return True

    def remove_attendance(self, code, date=None):
        """إزالة تسجيل حضور"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        data = self.load_data()
        if date in data['attendance'] and code in data['attendance'][date]:
            del data['attendance'][date][code]
            self.save_data(data)
            return True
        return False

    def get_today_attendance(self):
        """الحصول على الحضور ليوم اليوم"""
        today = datetime.now().strftime("%Y-%m-%d")
        data = self.load_data()
        return data['attendance'].get(today, {})
    
    def get_attendance_dates_with_info(self):
        """الحصول على تواريخ الحضور مع معلومات اليوم والخدمة"""
        data = self.load_data()
        dates_info = []
        
        for date_str in data.get('attendance', {}).keys():
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                day_name = date_obj.strftime("%A")
                arabic_day = self.arabic_days.get(day_name, day_name)
                
                # التحقق إذا كان يوم الخدمة
                service_day = data.get('settings', {}).get('service_day', 'Thursday')
                is_service_day = (day_name == service_day)
                
                dates_info.append({
                    'date': date_str,
                    'day_name': arabic_day,
                    'is_service_day': is_service_day,
                    'display': f"{date_str} ({arabic_day}){' - يوم الخدمة' if is_service_day else ''}"
                })
            except:
                continue
        
        # ترتيب التواريخ من الأحدث إلى الأقدم
        dates_info.sort(key=lambda x: x['date'], reverse=True)
        return dates_info
    
    def get_service_day_attendance(self):
        """الحصول على الحضور في أيام الخدمة فقط"""
        data = self.load_data()
        service_day = data.get('settings', {}).get('service_day', 'Thursday')
        service_attendance = {}
        
        for date_str, attendance_data in data.get('attendance', {}).items():
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                if date_obj.strftime("%A") == service_day:
                    service_attendance[date_str] = attendance_data
            except:
                continue
        
        return service_attendance
    
    def get_attendance_stats_by_date(self, date):
        """إحصائيات الحضور لتاريخ معين"""
        data = self.load_data()
        all_children = self.get_all_children()
        
        if date not in data['attendance']:
            return None
        
        present_codes = set(data['attendance'][date].keys())
        absent_children = [child for child in all_children if str(child.get('code', '')).strip() not in present_codes]
        
        # إحصائيات حسب الصف
        class_stats = {}
        for class_name in self.arabic_classes:
            class_children = self.get_children_by_class(class_name)
            class_absent = [child for child in class_children if str(child.get('code', '')).strip() not in present_codes]
            
            class_stats[class_name] = {
                'total': len(class_children),
                'present': len(class_children) - len(class_absent),
                'absent': len(class_absent)
            }
        
        return {
            'date': date,
            'total': len(all_children),
            'present': len(present_codes),
            'absent': len(absent_children),
            'classes': class_stats,
            'attendance_rate': (len(present_codes) / len(all_children) * 100) if all_children else 0
        }
    
    def update_settings(self, service_day, service_time):
        """تحديث إعدادات النظام"""
        data = self.load_data()
        if 'settings' not in data:
            data['settings'] = {}
        
        data['settings']['service_day'] = service_day
        data['settings']['service_time'] = service_time
        
        self.save_data(data)
    
    def get_settings(self):
        """الحصول على إعدادات النظام"""
        data = self.load_data()
        return data.get('settings', {'service_day': 'Thursday', 'service_time': '19:00'})
    
    def get_modification_tracking(self):
        """الحصول على معلومات التعديل"""
        data = self.load_data()
        return data.get('modification_tracking', {
            'last_modified': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'modification_count': 0
        })
    
    def get_child_by_code(self, code):
        data = self.load_data()
        for child in data['children']:
            if str(child.get('code', '')).strip() == str(code).strip():
                return child
        return None
    
    def get_all_children(self):
        data = self.load_data()
        return data.get('children', [])
    
    def get_children_by_class(self, class_name):
        children = self.get_all_children()
        return [child for child in children if child.get('class') == class_name]
    
    def save_attendance(self, present_codes):
        data = self.load_data()
        today = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M")
        
        if today not in data['attendance']:
            data['attendance'][today] = {}
        
        for code in present_codes:
            if code not in data['attendance'][today]:
                data['attendance'][today][code] = current_time
        
        self.save_data(data)
        return len(present_codes)
    
    def get_attendance_dates(self):
        data = self.load_data()
        dates = list(data.get('attendance', {}).keys())
        dates.sort(reverse=True)
        return dates if dates else [datetime.now().strftime("%Y-%m-%d")]
    
    def get_absent_children(self, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        data = self.load_data()
        all_children = self.get_all_children()
        
        if date not in data['attendance']:
            return all_children
        
        present_codes = set(data['attendance'][date].keys())
        absent_children = []
        
        for child in all_children:
            if str(child.get('code', '')).strip() not in present_codes:
                absent_children.append(child)
        
        return absent_children
    
    def get_absent_children_by_class(self, date=None, class_name=None):
        absent_children = self.get_absent_children(date)
        if class_name:
            return [child for child in absent_children if child.get('class') == class_name]
        return absent_children
    
    def add_child(self, child_data):
        data = self.load_data()
        
        for child in data['children']:
            if str(child.get('code', '')).strip() == str(child_data['code']).strip():
                raise ValueError("كود الطفل موجود مسبقاً")
        
        # إضافة حقول التعديل
        child_data['is_modified'] = True
        child_data['last_modified'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        data['children'].append(child_data)
        self.save_data(data)
    
    def update_child(self, old_code, new_data):
        """تحديث بيانات الطفل في قاعدة البيانات"""
        data = self.load_data()
        for i, child in enumerate(data['children']):
            if str(child.get('code', '')).strip() == str(old_code).strip():
                # تحديث البيانات مع الحفاظ على الكود القديم إذا لم يتغير
                data['children'][i] = {**child, **new_data}
                # تأكد من أن الكود يبقى كما هو
                data['children'][i]['code'] = old_code
                # وضع علامة على البيانات المعدلة
                data['children'][i]['is_modified'] = True
                data['children'][i]['last_modified'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        
        self.save_data(data)
        return True
    
    def delete_child(self, child_code):
        """حذف طفل"""
        data = self.load_data()
        
        for i, child in enumerate(data['children']):
            if str(child.get('code', '')).strip() == str(child_code).strip():
                del data['children'][i]
                self.save_data(data)
                return True
        
        return False
    
    def import_children(self, children_data):
        data = self.load_data()
        
        imported_count = 0
        for child in children_data:
            existing_codes = [str(c.get('code', '')).strip() for c in data['children']]
            if str(child.get('code', '')).strip() not in existing_codes:
                # تعيين البيانات المستوردة كغير معدلة
                child['is_modified'] = False
                child['last_modified'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data['children'].append(child)
                imported_count += 1
        
        self.save_data(data)
        return imported_count
    
    def get_attendance_stats(self, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        all_children = self.get_all_children()
        absent_children = self.get_absent_children(date)
        present_count = len(all_children) - len(absent_children)
        
        class_stats = {}
        for class_name in self.arabic_classes:
            class_children = self.get_children_by_class(class_name)
            class_absent = self.get_absent_children_by_class(date, class_name)
            class_present = len(class_children) - len(class_absent)
            
            class_stats[class_name] = {
                'total': len(class_children),
                'present': class_present,
                'absent': len(class_absent)
            }
        
        return {
            'total': len(all_children),
            'present': present_count,
            'absent': len(absent_children),
            'classes': class_stats,
            'attendance_rate': (present_count / len(all_children) * 100) if all_children else 0
        }
    
    def get_modification_history(self):
        """الحصول على سجل التعديلات"""
        data = self.load_data()
        
        # جمع معلومات التعديل من الأطفال
        children_modifications = []
        for child in data.get('children', []):
            if child.get('is_modified'):
                children_modifications.append({
                    'type': 'child_modification',
                    'code': child.get('code'),
                    'name': child.get('name', 'غير معروف'),
                    'last_modified': child.get('last_modified'),
                    'class': child.get('class', 'غير محدد')
                })
        
        return {
            'database_tracking': data.get('modification_tracking', {}),
            'children_modifications': children_modifications,
            'total_modified_children': len([c for c in data.get('children', []) if c.get('is_modified', False)]),
            'total_children': len(data.get('children', []))
        }