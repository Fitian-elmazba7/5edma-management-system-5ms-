import * as XLSX from 'xlsx'
import { Child } from '@5edma/shared'

/**
 * Parse Excel file and extract children data
 */
export async function parseExcelFile(file: File): Promise<{
  data: Partial<Child>[]
  errors: string[]
  rowCount: number
}> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()

    reader.onload = (e) => {
      try {
        const data = e.target?.result
        const workbook = XLSX.read(data, { type: 'array' })
        const sheetName = workbook.SheetNames[0]
        const worksheet = workbook.Sheets[sheetName]
        const rows = XLSX.utils.sheet_to_json(worksheet)

        const parsed: Partial<Child>[] = []
        const errors: string[] = []

        rows.forEach((row: any, index: number) => {
          try {
            const child: Partial<Child> = {
              code: String(row['الرقم'] || row['code'] || '').trim(),
              name: String(row['الاسم'] || row['name'] || '').trim(),
              class: String(row['الصف'] || row['class'] || 'الصف الأول').trim() as any,
              region: String(row['المنطقة'] || row['region'] || '').trim(),
              building: String(row['العمارة'] || row['building'] || '').trim(),
              street: String(row['الشارع'] || row['street'] || '').trim(),
              floor: String(row['الدور'] || row['floor'] || '').trim(),
              apartment: String(row['الشقة'] || row['apartment'] || '').trim(),
              childMobile: String(row['موبايل الطفل'] || row['childMobile'] || '').trim(),
              fatherMobile: String(row['موبايل الأب'] || row['fatherMobile'] || '').trim(),
              motherMobile: String(row['موبايل الأم'] || row['motherMobile'] || '').trim(),
              homeLine: String(row['التليفون'] || row['homeLine'] || '').trim(),
              school: String(row['المدرسة'] || row['school'] || '').trim(),
              notes: String(row['ملاحظات'] || row['notes'] || '').trim(),
            }

            // Validate required fields
            if (!child.code) {
              errors.push(`صف رقم ${index + 2}: الرقم مطلوب`)
              return
            }

            if (!child.name) {
              errors.push(`صف رقم ${index + 2}: الاسم مطلوب`)
              return
            }

            // Validate code is numeric
            if (!/^\d+$/.test(child.code)) {
              errors.push(`صف رقم ${index + 2}: الرقم يجب أن يكون أرقام فقط`)
              return
            }

            parsed.push(child)
          } catch (err) {
            errors.push(
              `صف رقم ${index + 2}: خطأ في معالجة البيانات - ${err instanceof Error ? err.message : 'خطأ غير معروف'}`,
            )
          }
        })

        resolve({
          data: parsed,
          errors,
          rowCount: rows.length,
        })
      } catch (err) {
        reject(new Error(`فشل في قراءة ملف Excel: ${err instanceof Error ? err.message : 'خطأ غير معروف'}`))
      }
    }

    reader.onerror = () => {
      reject(new Error('فشل في قراءة الملف'))
    }

    reader.readAsArrayBuffer(file)
  })
}

/**
 * Validate children data before import
 */
export function validateChildrenData(children: Partial<Child>[]): {
  valid: Child[]
  invalid: Array<{ data: Partial<Child>; error: string }>
} {
  const valid: Child[] = []
  const invalid: Array<{ data: Partial<Child>; error: string }> = []

  const validClasses = ['الصف الأول', 'الصف الثاني', 'الصف الثالث']

  children.forEach((child) => {
    // Check required fields
    if (!child.code || !child.name) {
      invalid.push({
        data: child,
        error: 'الرقم والاسم مطلوبان',
      })
      return
    }

    // Check class validity
    if (!validClasses.includes(child.class || '')) {
      invalid.push({
        data: child,
        error: `الصف غير صحيح: ${child.class}`,
      })
      return
    }

    // Add default values for missing fields
    const validChild: Child = {
      code: child.code,
      name: child.name,
      class: child.class as any,
      region: child.region || 'غير محدد',
      building: child.building || 'غير محدد',
      street: child.street || 'غير محدد',
      floor: child.floor || 'غير محدد',
      apartment: child.apartment || 'غير محدد',
      childMobile: child.childMobile || 'غير محدد',
      fatherMobile: child.fatherMobile || 'غير محدد',
      motherMobile: child.motherMobile || 'غير محدد',
      homeLine: child.homeLine || 'غير محدد',
      school: child.school || 'غير محدد',
      isDeacon: false,
      confessorFather: 'غير محدد',
      notes: child.notes || '',
      attendanceClass: 'اساسي',
      lastConfession: 'غير محدد',
      createdAt: Date.now(),
      updatedAt: Date.now(),
      createdBy: '', // Will be set by the store
    }

    valid.push(validChild)
  })

  return { valid, invalid }
}
