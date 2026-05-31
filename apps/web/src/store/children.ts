import { create } from 'zustand'
import { Child } from '@5edma/shared'
import * as childrenDB from '../lib/firestore/children'
import { useAuthStore } from './auth'

interface ChildrenState {
  children: Child[]
  loading: boolean
  error: string | null

  // Actions
  fetchChildren: () => Promise<void>
  fetchChildrenByClass: (className: string) => Promise<Child[]>
  createChild: (child: Omit<Child, 'createdAt' | 'updatedAt' | 'createdBy'>) => Promise<void>
  updateChild: (
    code: string,
    updates: Partial<Omit<Child, 'code' | 'createdAt' | 'createdBy'>>,
  ) => Promise<void>
  deleteChild: (code: string) => Promise<void>
  importChildren: (children: Omit<Child, 'createdAt' | 'updatedAt' | 'createdBy'>[]) => Promise<{
    imported: number
    skipped: number
    errors: string[]
  }>
  getChildByCode: (code: string) => Child | undefined
}

export const useChildrenStore = create<ChildrenState>((set, get) => ({
  children: [],
  loading: false,
  error: null,

  fetchChildren: async () => {
    set({ loading: true, error: null })
    try {
      const children = await childrenDB.getAllChildren()
      set({ children })
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Failed to fetch children',
      })
    } finally {
      set({ loading: false })
    }
  },

  fetchChildrenByClass: async (className: string) => {
    try {
      return await childrenDB.getChildrenByClass(className)
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Failed to fetch children by class',
      })
      return []
    }
  },

  createChild: async (child) => {
    try {
      set({ error: null })
      const user = useAuthStore.getState().user
      if (!user) throw new Error('User not authenticated')

      await childrenDB.createChild(child, user.uid)
      // Refresh the list
      await get().fetchChildren()
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Failed to create child',
      })
      throw err
    }
  },

  updateChild: async (code, updates) => {
    try {
      set({ error: null })
      await childrenDB.updateChild(code, updates)
      // Update local state
      set((state) => ({
        children: state.children.map((c) =>
          c.code === code ? { ...c, ...updates } : c,
        ),
      }))
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Failed to update child',
      })
      throw err
    }
  },

  deleteChild: async (code) => {
    try {
      set({ error: null })
      await childrenDB.deleteChild(code)
      // Remove from local state
      set((state) => ({
        children: state.children.filter((c) => c.code !== code),
      }))
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Failed to delete child',
      })
      throw err
    }
  },

  importChildren: async (children) => {
    try {
      set({ error: null })
      const user = useAuthStore.getState().user
      if (!user) throw new Error('User not authenticated')

      const result = await childrenDB.importChildren(children, user.uid)
      // Refresh the list
      await get().fetchChildren()
      return result
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : 'Failed to import children',
      })
      throw err
    }
  },

  getChildByCode: (code) => {
    return get().children.find((c) => c.code === code)
  },
}))
