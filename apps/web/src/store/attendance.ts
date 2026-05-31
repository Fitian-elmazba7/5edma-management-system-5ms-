import { create } from 'zustand'
import { AttendanceStats } from '@5edma/shared'
import * as attendanceDB from '../lib/firestore/attendance'
import { useAuthStore } from './auth'
import { formatDate } from '../lib/utils'

interface AttendanceState {
  // Current session
  currentSessionDate: string | null
  currentSessionAttendance: Record<string, string> // { code: time }
  sessionLoading: boolean

  // Attendance data
  attendanceDates: string[]
  selectedDate: string | null
  selectedDateStats: AttendanceStats | null
  absentChildren: any[]

  loading: boolean
  error: string | null

  // Actions
  startSession: () => void
  endSession: () => Promise<void>
  recordAttendance: (code: string, time: string) => Promise<void>
  removeAttendance: (code: string) => Promise<void>
  fetchAttendanceDates: () => Promise<void>
  fetchAttendanceStats: (date: string) => Promise<void>
  fetchAbsentChildren: (date: string) => Promise<void>
  getAbsentChildrenByClass: (date: string, className: string) => Promise<any[]>
}

export const useAttendanceStore = create<AttendanceState>((set, get) => ({
  currentSessionDate: null,
  currentSessionAttendance: {},
  sessionLoading: false,
  attendanceDates: [],
  selectedDate: null,
  selectedDateStats: null,
  absentChildren: [],
  loading: false,
  error: null,

  startSession: () => {
    const today = formatDate(new Date())
    set({
      currentSessionDate: today,
      currentSessionAttendance: {},
      sessionLoading: false,
    })
  },

  endSession: async () => {
    try {
      set({ sessionLoading: true, error: null })
      // Session is automatically saved to Firestore on each recordAttendance call
      // Just clear the session state
      set({
        currentSessionDate: null,
        currentSessionAttendance: {},
      })
      // Refresh attendance dates
      await get().fetchAttendanceDates()
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Failed to end session',
      })
    } finally {
      set({ sessionLoading: false })
    }
  },

  recordAttendance: async (code: string, time: string) => {
    try {
      set({ error: null, sessionLoading: true })
      const user = useAuthStore.getState().user
      if (!user) throw new Error('User not authenticated')

      const date = get().currentSessionDate || formatDate(new Date())
      await attendanceDB.recordAttendance(code, date, time, user.uid)

      // Update local session state
      set((state) => ({
        currentSessionAttendance: {
          ...state.currentSessionAttendance,
          [code]: time,
        },
      }))
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Failed to record attendance',
      })
      throw err
    } finally {
      set({ sessionLoading: false })
    }
  },

  removeAttendance: async (code: string) => {
    try {
      set({ error: null })
      const date = get().selectedDate
      if (!date) throw new Error('No date selected')

      await attendanceDB.removeAttendance(code, date)

      // Refresh data
      await get().fetchAttendanceStats(date)
      await get().fetchAbsentChildren(date)
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Failed to remove attendance',
      })
      throw err
    }
  },

  fetchAttendanceDates: async () => {
    try {
      set({ loading: true, error: null })
      const dates = await attendanceDB.getAttendanceDates()
      set({ attendanceDates: dates })
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Failed to fetch attendance dates',
      })
    } finally {
      set({ loading: false })
    }
  },

  fetchAttendanceStats: async (date: string) => {
    try {
      set({ loading: true, error: null, selectedDate: date })
      const stats = await attendanceDB.getAttendanceStats(date)
      set({ selectedDateStats: stats })
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Failed to fetch attendance stats',
      })
    } finally {
      set({ loading: false })
    }
  },

  fetchAbsentChildren: async (date: string) => {
    try {
      set({ error: null })
      const absent = await attendanceDB.getAbsentChildren(date)
      set({ absentChildren: absent })
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Failed to fetch absent children',
      })
    }
  },

  getAbsentChildrenByClass: async (date: string, className: string) => {
    try {
      return await attendanceDB.getAbsentChildrenByClass(date, className)
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Failed to fetch absent children by class',
      })
      return []
    }
  },
}))
