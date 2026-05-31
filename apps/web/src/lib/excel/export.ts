import { Child, AttendanceStats } from '@5edma/shared'

/**
 * Export children to Excel file
 * NOTE: xlsx library not installed - install with: npm install xlsx
 */
export function exportChildrenToExcel(children: Child[], filename: string = 'أطفال.xlsx') {
  console.warn('Excel export not available - install xlsx library')
  return
  const data = children.map((child) => ({
    'الرقم': child.code,
    'الاسم': child.name,
    'الصف': child.class,
    'المنطقة': child.region,
    'العمارة': child.building,
    'الشارع': child.street,
    'الدور': child.floor,
    'الشقة': child.apartment,
    'موبايل الطفل': child.childMobile,
    'موبايل الأب': child.fatherMobile,
    'موبايل الأم': child.motherMobile,
    'التليفون': child.homeLine,
    'المدرسة': child.school,
    'ملاحظات': child.notes,
  }))

  const wb = XLSX.utils.book_new()
  const ws = XLSX.utils.json_to_sheet(data, { header: 1 })

  // Set column widths
  ws['!cols'] = [
    { wch: 10 }, // رقم
    { wch: 20 }, // اسم
    { wch: 15 }, // صف
    { wch: 12 }, // منطقة
    { wch: 15 }, // عمارة
    { wch: 15 }, // شارع
    { wch: 8 },  // دور
    { wch: 8 },  // شقة
    { wch: 15 }, // موبايل الطفل
    { wch: 15 }, // موبايل الأب
    { wch: 15 }, // موبايل الأم
    { wch: 15 }, // تليفون
    { wch: 15 }, // مدرسة
    { wch: 20 }, // ملاحظات
  ]

  XLSX.utils.book_append_sheet(wb, ws, 'البيانات')
  XLSX.writeFile(wb, filename)
}

/**
 * Export absence report to Excel
 */
export function exportAbsenceReportToExcel(
  absentChildren: Child[],
  date: string,
  filename: string = `غياب_${date}.xlsx`,
) {
  const data = absentChildren.map((child) => ({
    'التاريخ': date,
    'الرقم': child.code,
    'الاسم': child.name,
    'الصف': child.class,
    'المنطقة': child.region,
    'العمارة': child.building,
    'الشارع': child.street,
    'الدور': child.floor,
    'الشقة': child.apartment,
    'موبايل الطفل': child.childMobile,
    'موبايل الأب': child.fatherMobile,
    'موبايل الأم': child.motherMobile,
    'التليفون': child.homeLine,
    'الملاحظات': child.notes,
  }))

  const wb = XLSX.utils.book_new()
  const ws = XLSX.utils.json_to_sheet(data)

  ws['!cols'] = [
    { wch: 12 }, // تاريخ
    { wch: 10 }, // رقم
    { wch: 20 }, // اسم
    { wch: 15 }, // صف
    { wch: 12 }, // منطقة
    { wch: 15 }, // عمارة
    { wch: 15 }, // شارع
    { wch: 8 },  // دور
    { wch: 8 },  // شقة
    { wch: 15 }, // موبايل الطفل
    { wch: 15 }, // موبايل الأب
    { wch: 15 }, // موبايل الأم
    { wch: 15 }, // تليفون
    { wch: 20 }, // ملاحظات
  ]

  XLSX.utils.book_append_sheet(wb, ws, 'الغياب')
  XLSX.writeFile(wb, filename)
}

/**
 * Export attendance report to Excel
 */
export function exportAttendanceReportToExcel(
  presentChildren: Child[],
  date: string,
  stats: AttendanceStats,
  filename: string = `حضور_${date}.xlsx`,
) {
  // Summary sheet
  const summary = [
    ['تقرير الحضور'],
    ['التاريخ', date],
    ['إجمالي الأطفال', stats.total],
    ['الحاضرين', stats.present],
    ['الغائبين', stats.absent],
    ['نسبة الحضور', `${stats.attendanceRate}%`],
    [],
    ['الحضور حسب الصف'],
  ]

  // Add class stats
  Object.entries(stats.byClass).forEach(([className, classStats]) => {
    summary.push([
      className,
      `حاضر: ${classStats.present}`,
      `غائب: ${classStats.absent}`,
      `إجمالي: ${classStats.total}`,
    ])
  })

  // Children data sheet
  const childrenData = presentChildren.map((child) => ({
    'الرقم': child.code,
    'الاسم': child.name,
    'الصف': child.class,
    'المنطقة': child.region,
    'المدرسة': child.school,
    'موبايل الطفل': child.childMobile,
    'موبايل الأب': child.fatherMobile,
    'موبايل الأم': child.motherMobile,
  }))

  const wb = XLSX.utils.book_new()

  // Summary sheet
  const wsSummary = XLSX.utils.aoa_to_sheet(summary)
  XLSX.utils.book_append_sheet(wb, wsSummary, 'ملخص')

  // Children sheet
  const wsChildren = XLSX.utils.json_to_sheet(childrenData)
  wsChildren['!cols'] = [
    { wch: 10 },
    { wch: 20 },
    { wch: 15 },
    { wch: 12 },
    { wch: 15 },
    { wch: 15 },
    { wch: 15 },
    { wch: 15 },
    { wch: 15 },
  ]
  XLSX.utils.book_append_sheet(wb, wsChildren, 'البيانات')

  XLSX.writeFile(wb, filename)
}

/**
 * Export blank template for children data
 */
export function exportBlankTemplate(filename: string = 'نموذج_فارغ.xlsx') {
  const headerRow = {
    'الرقم': '',
    'الاسم': '',
    'الصف': '',
    'المنطقة': '',
    'العمارة': '',
    'الشارع': '',
    'الدور': '',
    'الشقة': '',
    'موبايل الطفل': '',
    'موبايل الأب': '',
    'موبايل الأم': '',
    'التليفون': '',
    'المدرسة': '',
    'ملاحظات': '',
  }

  // Create 10 empty rows
  const data = Array(10).fill(null).map(() => ({ ...headerRow }))

  const wb = XLSX.utils.book_new()
  const ws = XLSX.utils.json_to_sheet(data)

  ws['!cols'] = [
    { wch: 10 },
    { wch: 20 },
    { wch: 15 },
    { wch: 12 },
    { wch: 15 },
    { wch: 15 },
    { wch: 15 },
    { wch: 8 },
    { wch: 8 },
    { wch: 15 },
    { wch: 15 },
    { wch: 15 },
    { wch: 15 },
    { wch: 20 },
  ]

  XLSX.utils.book_append_sheet(wb, ws, 'البيانات')
  XLSX.writeFile(wb, filename)
}
