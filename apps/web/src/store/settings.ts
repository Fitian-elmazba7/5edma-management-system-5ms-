import { create } from 'zustand'
import { Settings } from '@5edma/shared'
import * as settingsDB from '../lib/firestore/settings'

interface SettingsState {
  settings: Settings | null
  loading: boolean
  error: string | null

  // Actions
  fetchSettings: () => Promise<void>
  updateServiceDay: (day: string) => Promise<void>
  updateServiceTime: (time: string) => Promise<void>
  updateOrgName: (name: string) => Promise<void>
}

export const useSettingsStore = create<SettingsState>((set, get) => ({
  settings: null,
  loading: false,
  error: null,

  fetchSettings: async () => {
    set({ loading: true, error: null })
    try {
      const settings = await settingsDB.getSettings()
      set({ settings })
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Failed to fetch settings',
      })
    } finally {
      set({ loading: false })
    }
  },

  updateServiceDay: async (day: string) => {
    try {
      set({ error: null })
      await settingsDB.updateServiceDay(day)
      set((state) => ({
        settings: state.settings
          ? { ...state.settings, serviceDay: day }
          : null,
      }))
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Failed to update service day',
      })
      throw err
    }
  },

  updateServiceTime: async (time: string) => {
    try {
      set({ error: null })
      await settingsDB.updateServiceTime(time)
      set((state) => ({
        settings: state.settings
          ? { ...state.settings, serviceTime: time }
          : null,
      }))
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Failed to update service time',
      })
      throw err
    }
  },

  updateOrgName: async (name: string) => {
    try {
      set({ error: null })
      await settingsDB.updateOrgName(name)
      set((state) => ({
        settings: state.settings
          ? { ...state.settings, orgName: name }
          : null,
      }))
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Failed to update organization name',
      })
      throw err
    }
  },
}))
