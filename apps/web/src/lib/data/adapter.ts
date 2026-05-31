/**
 * Data adapter layer that abstracts between Firestore and SQLite
 * Automatically chooses the correct backend based on environment
 */

import { isElectron } from '../env'
import type { Child, Attendance, Settings } from '@5edma/shared'

interface DataAdapter {
  children: ChildrenAdapter
  attendance: AttendanceAdapter
  settings: SettingsAdapter
}

interface ChildrenAdapter {
  getAll: () => Promise<Child[]>
  getByCode: (code: string) => Promise<Child | null>
  create: (child: Child) => Promise<void>
  update: (code: string, updates: Partial<Child>) => Promise<void>
  delete: (code: string) => Promise<void>
}

interface AttendanceAdapter {
  getByDate: (date: string) => Promise<Attendance[]>
  record: (code: string, date: string, time: string) => Promise<void>
  remove: (code: string, date: string) => Promise<void>
}

interface SettingsAdapter {
  get: (key: string) => Promise<string | null>
  set: (key: string, value: string) => Promise<void>
}

class FirestoreAdapter implements DataAdapter {
  children: ChildrenAdapter = {
    getAll: async () => {
      const { getAllChildren } = await import('../firestore/children')
      return getAllChildren()
    },
    getByCode: async (code: string) => {
      const { getChildByCode } = await import('../firestore/children')
      return getChildByCode(code)
    },
    create: async (child: Child) => {
      const { createChild } = await import('../firestore/children')
      return createChild(child)
    },
    update: async (code: string, updates: Partial<Child>) => {
      const { updateChild } = await import('../firestore/children')
      return updateChild(code, updates)
    },
    delete: async (code: string) => {
      const { deleteChild } = await import('../firestore/children')
      return deleteChild(code)
    },
  }

  attendance: AttendanceAdapter = {
    getByDate: async (date: string) => {
      const { getAttendanceForDate } = await import('../firestore/attendance')
      return getAttendanceForDate(date)
    },
    record: async (code: string, date: string, time: string) => {
      const { recordAttendance } = await import('../firestore/attendance')
      return recordAttendance(code, date, time)
    },
    remove: async (code: string, date: string) => {
      const { removeAttendance } = await import('../firestore/attendance')
      return removeAttendance(code, date)
    },
  }

  settings: SettingsAdapter = {
    get: async (key: string) => {
      const { getSettings } = await import('../firestore/settings')
      const settings = await getSettings()
      return settings[key as keyof typeof settings]?.toString() || null
    },
    set: async (key: string, value: string) => {
      const { updateSettings } = await import('../firestore/settings')
      return updateSettings({ [key]: value })
    },
  }
}

class ElectronAdapter implements DataAdapter {
  children: ChildrenAdapter = {
    getAll: async () => {
      const api = window.electronAPI
      const result = await api.db.getChildren()
      if (!result.success) throw new Error(result.error)
      return result.data
    },
    getByCode: async (code: string) => {
      const api = window.electronAPI
      const result = await api.db.getChild(code)
      if (!result.success) throw new Error(result.error)
      return result.data || null
    },
    create: async (child: Child) => {
      const api = window.electronAPI
      const result = await api.db.addChild(child)
      if (!result.success) throw new Error(result.error)
    },
    update: async (code: string, updates: Partial<Child>) => {
      const api = window.electronAPI
      const result = await api.db.updateChild(code, updates)
      if (!result.success) throw new Error(result.error)
    },
    delete: async (code: string) => {
      const api = window.electronAPI
      const result = await api.db.deleteChild(code)
      if (!result.success) throw new Error(result.error)
    },
  }

  attendance: AttendanceAdapter = {
    getByDate: async (date: string) => {
      const api = window.electronAPI
      const result = await api.db.getAttendance(date)
      if (!result.success) throw new Error(result.error)
      return result.data
    },
    record: async (code: string, date: string, time: string) => {
      const api = window.electronAPI
      const result = await api.db.recordAttendance(code, date, time)
      if (!result.success) throw new Error(result.error)
    },
    remove: async () => {
      throw new Error('Remove attendance not yet implemented in Electron adapter')
    },
  }

  settings: SettingsAdapter = {
    get: async () => {
      throw new Error('Settings adapter not yet implemented in Electron')
    },
    set: async () => {
      throw new Error('Settings adapter not yet implemented in Electron')
    },
  }
}

let adapter: DataAdapter | null = null

export function getDataAdapter(): DataAdapter {
  if (!adapter) {
    adapter = isElectron() ? new ElectronAdapter() : new FirestoreAdapter()
  }
  return adapter
}

export function resetAdapter(): void {
  adapter = null
}

export async function getAllChildren(): Promise<Child[]> {
  return getDataAdapter().children.getAll()
}

export async function getChildByCode(code: string): Promise<Child | null> {
  return getDataAdapter().children.getByCode(code)
}

export async function createChild(child: Child): Promise<void> {
  return getDataAdapter().children.create(child)
}

export async function updateChild(code: string, updates: Partial<Child>): Promise<void> {
  return getDataAdapter().children.update(code, updates)
}

export async function deleteChild(code: string): Promise<void> {
  return getDataAdapter().children.delete(code)
}

export async function getAttendanceByDate(date: string): Promise<Attendance[]> {
  return getDataAdapter().attendance.getByDate(date)
}

export async function recordAttendance(code: string, date: string, time: string): Promise<void> {
  return getDataAdapter().attendance.record(code, date, time)
}

export async function getSetting(key: string): Promise<string | null> {
  return getDataAdapter().settings.get(key)
}

export async function setSetting(key: string, value: string): Promise<void> {
  return getDataAdapter().settings.set(key, value)
}
