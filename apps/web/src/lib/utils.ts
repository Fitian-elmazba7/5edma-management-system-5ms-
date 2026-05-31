import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Format time to HH:MM
export function formatTime(hours: number, minutes: number): string {
  return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`
}

// Parse HH:MM to { hours, minutes }
export function parseTime(timeStr: string): { hours: number; minutes: number } {
  const [hours, minutes] = timeStr.split(':').map(Number)
  return { hours, minutes }
}

// Format date to YYYY-MM-DD
export function formatDate(date: Date | number): string {
  const d = new Date(date)
  return d.toISOString().split('T')[0]
}

// Get Arabic weekday name
export function getArabicWeekday(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date
  const days = [
    'الأحد',
    'الاثنين',
    'الثلاثاء',
    'الأربعاء',
    'الخميس',
    'الجمعة',
    'السبت',
  ]
  return days[d.getDay()]
}

// Get Arabic month name
export function getArabicMonth(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date
  const months = [
    'يناير',
    'فبراير',
    'مارس',
    'أبريل',
    'مايو',
    'يونيو',
    'يوليو',
    'أغسطس',
    'سبتمبر',
    'أكتوبر',
    'نوفمبر',
    'ديسمبر',
  ]
  return months[d.getMonth()]
}

// Normalize Arabic text (handle different forms of alef, taa marbuta, etc.)
export function normalizeArabic(text: string): string {
  return text
    .replace(/ا|أ|إ/g, 'ا') // Normalize alef
    .replace(/ة/g, 'ه') // Normalize taa marbuta
    .replace(/ي/g, 'ي') // Normalize yaa
    .trim()
}
