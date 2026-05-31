// Child data model
export interface Child {
  code: string // PK
  name: string
  class: 'الصف الأول' | 'الصف الثاني' | 'الصف الثالث'
  region: string
  building: string // عماره
  street: string // شارع
  floor: string // دور
  apartment: string // شقه
  childMobile: string
  fatherMobile: string
  motherMobile: string
  homeLine: string // تليفون
  school: string
  isDeacon: boolean
  confessorFather: string
  notes: string
  attendanceClass: string
  lastConfession: string
  createdAt: number // timestamp
  updatedAt: number // timestamp
  createdBy: string // UID
}

// Attendance data model
export interface AttendanceRecord {
  date: string // YYYY-MM-DD
  records: Record<string, string> // { "101": "18:45" }
  serviceDay: boolean
  createdBy: string
  updatedAt: number
}

// Settings
export interface Settings {
  serviceDay: string // "Thursday"
  serviceTime: string // "19:00"
  orgName: string
}

// User
export type UserRole = 'admin' | 'servant' | 'viewer' | 'user'

export interface User {
  uid: string
  email: string
  displayName: string
  role: UserRole
  createdAt: number
}

// Session state
export interface AttendanceSession {
  id: string
  date: string
  startTime: number
  endTime?: number
  registeredCodes: string[] // codes registered in this session
  createdBy: string
}

// Sync queue (for offline mode)
export interface SyncQueueItem {
  id: string
  operation: 'create' | 'update' | 'delete'
  collection: 'children' | 'attendance' | 'settings'
  documentId: string
  data: Record<string, any>
  timestamp: number
  retries: number
}

// API Response types
export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  timestamp: number
}

// Attendance stats
export interface AttendanceStats {
  total: number
  present: number
  absent: number
  attendanceRate: number
  byClass: Record<string, { total: number; present: number; absent: number }>
}

// Export all types
export type * from './index'
