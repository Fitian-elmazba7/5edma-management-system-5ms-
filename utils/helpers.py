import re

def validate_phone_number(phone):
    """التحقق من صحة رقم التليفون"""
    if not phone:
        return True
        
    # إزالة المسافات والأحرف غير الرقمية
    cleaned_phone = re.sub(r'[^\d]', '', phone)
    
    # التحقق من الطول (عادة 10-11 رقم في مصر)
    return 10 <= len(cleaned_phone) <= 11

def validate_code(code):
    """التحقق من صحة الكود"""
    return bool(code and str(code).strip())

def format_phone_number(phone):
    """تنسيق رقم التليفون"""
    if not phone:
        return ""
        
    cleaned_phone = re.sub(r'[^\d]', '', phone)
    
    if len(cleaned_phone) == 11 and cleaned_phone.startswith('0'):
        return f"+2{cleaned_phone}"  # تحويل إلى التنسيق الدولي
    elif len(cleaned_phone) == 10:
        return f"+20{cleaned_phone}"  # إضافة رمز مصر
        
    return phone