import {
  collection,
  doc,
  getDoc,
  getDocs,
  setDoc,
  updateDoc,
  deleteDoc,
  query,
  where,
  orderBy,
} from 'firebase/firestore'
import { db } from '../firebase'
import { AttendanceRecord, AttendanceStats } from '@5edma/shared'
import { formatDate } from '../utils'
import { getAllChildren, getChildrenByClass } from './children'

const COLLECTION = 'attendance'

// Record attendance for a child on a date
export async function recordAttendance(
  code: string,
  date: string,
  time: string,
  userId: string,
): Promise<void> {
  const docRef = doc(db, COLLECTION, date)
  const docSnap = await getDoc(docRef)

  if (docSnap.exists()) {
    // Update existing attendance record
    await updateDoc(docRef, {
      [`records.${code}`]: time,
      updatedAt: Date.now(),
    })
  } else {
    // Create new attendance record for the date
    await setDoc(docRef, {
      date,
      records: { [code]: time },
      serviceDay: isServiceDay(date),
      createdBy: userId,
      updatedAt: Date.now(),
    })
  }
}

// Remove attendance for a child on a date
export async function removeAttendance(code: string, date: string): Promise<void> {
  const docRef = doc(db, COLLECTION, date)
  const docSnap = await getDoc(docRef)

  if (docSnap.exists()) {
    const records = docSnap.data().records
    delete records[code]

    if (Object.keys(records).length === 0) {
      // Delete the entire date record if no more attendance
      await deleteDoc(docRef)
    } else {
      // Update with remaining records
      await updateDoc(docRef, {
        records,
        updatedAt: Date.now(),
      })
    }
  }
}

// Get attendance for a specific date
export async function getAttendanceForDate(date: string): Promise<Record<string, string>> {
  const docRef = doc(db, COLLECTION, date)
  const docSnap = await getDoc(docRef)

  if (!docSnap.exists()) return {}

  return docSnap.data().records || {}
}

// Get all attendance dates
export async function getAttendanceDates(): Promise<string[]> {
  const querySnapshot = await getDocs(
    query(collection(db, COLLECTION), orderBy('date', 'desc')),
  )

  return querySnapshot.docs.map((doc) => doc.data().date)
}

// Get attendance for today
export async function getTodayAttendance(): Promise<Record<string, string>> {
  const today = formatDate(new Date())
  return getAttendanceForDate(today)
}

// Get absent children for a date
export async function getAbsentChildren(date: string): Promise<any[]> {
  const allChildren = await getAllChildren()
  const attendance = await getAttendanceForDate(date)
  const presentCodes = Object.keys(attendance)

  return allChildren.filter((child) => !presentCodes.includes(child.code))
}

// Get absent children by class for a date
export async function getAbsentChildrenByClass(
  date: string,
  className: string,
): Promise<any[]> {
  const classChildren = await getChildrenByClass(className)
  const attendance = await getAttendanceForDate(date)
  const presentCodes = Object.keys(attendance)

  return classChildren.filter((child) => !presentCodes.includes(child.code))
}

// Get attendance stats for a date
export async function getAttendanceStats(date: string): Promise<AttendanceStats> {
  const allChildren = await getAllChildren()
  const attendance = await getAttendanceForDate(date)
  const presentCodes = Object.keys(attendance)

  const total = allChildren.length
  const present = presentCodes.length
  const absent = total - present
  const attendanceRate = total > 0 ? Math.round((present / total) * 100) : 0

  // Calculate by class
  const byClass: Record<
    string,
    { total: number; present: number; absent: number }
  > = {}

  for (const className of ['الصف الأول', 'الصف الثاني', 'الصف الثالث']) {
    const classChildren = allChildren.filter((c) => c.class === className)
    const classPresent = classChildren.filter((c) =>
      presentCodes.includes(c.code),
    ).length

    byClass[className] = {
      total: classChildren.length,
      present: classPresent,
      absent: classChildren.length - classPresent,
    }
  }

  return {
    total,
    present,
    absent,
    attendanceRate,
    byClass,
  }
}

// Helper: check if a date is a service day (default: Thursday)
function isServiceDay(date: string): boolean {
  const d = new Date(date)
  // Thursday = 4
  return d.getDay() === 4
}
