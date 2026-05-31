import { contextBridge, ipcRenderer } from 'electron'

/**
 * Preload script for context isolation
 * Exposes safe IPC methods to the renderer process
 */

const electronAPI = {
  // File dialogs
  openFile: (options: any) => ipcRenderer.invoke('dialog:openFile', options),
  saveFile: (options: any) => ipcRenderer.invoke('dialog:saveFile', options),

  // Database operations
  db: {
    getChildren: () => ipcRenderer.invoke('db:getChildren'),
    getChild: (code: string) => ipcRenderer.invoke('db:getChild', code),
    addChild: (child: any) => ipcRenderer.invoke('db:addChild', child),
    updateChild: (code: string, updates: any) =>
      ipcRenderer.invoke('db:updateChild', code, updates),
    deleteChild: (code: string) => ipcRenderer.invoke('db:deleteChild', code),
    recordAttendance: (code: string, date: string, time: string) =>
      ipcRenderer.invoke('db:recordAttendance', code, date, time),
    getAttendance: (date: string) => ipcRenderer.invoke('db:getAttendance', date),
  },

  // Sync operations
  sync: {
    getPendingOperations: () => ipcRenderer.invoke('sync:getPendingOperations'),
    drainQueue: () => ipcRenderer.invoke('sync:drainQueue'),
  },

  // App info
  app: {
    getAppPath: () => ipcRenderer.invoke('app:getAppPath'),
  },
}

// Expose the API to the renderer process
contextBridge.exposeInMainWorld('electronAPI', electronAPI)

// Type declaration for TypeScript
declare global {
  interface Window {
    electronAPI: typeof electronAPI
  }
}
