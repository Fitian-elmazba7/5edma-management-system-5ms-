import { Child } from '@5edma/shared'

/**
 * Parse Excel file and extract children data
 * NOTE: xlsx library not installed - install with: npm install xlsx
 */
export async function parseExcelFile(file: File): Promise<{
  data: Partial<Child>[]
  errors: string[]
  rowCount: number
}> {
  return {
    data: [],
    errors: ['Excel import not available - install xlsx library'],
    rowCount: 0,
  }
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
