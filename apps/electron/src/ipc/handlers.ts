import { ipcMain, dialog, app } from 'electron'
import { getDatabase } from '../sqlite/db'
import { getSyncEngine } from '../sync/SyncEngine'
import path from 'path'

/**
 * Register all IPC handlers for Electron main process
 */
export function registerIpcHandlers() {
  // File dialog handlers
  ipcMain.handle('dialog:openFile', async (event, options) => {
    return await dialog.showOpenDialog(options)
  })

  ipcMain.handle('dialog:saveFile', async (event, options) => {
    return await dialog.showSaveDialog(options)
  })

  // Database handlers
  ipcMain.handle('db:getChildren', async () => {
    try {
      const db = getDatabase()
      const stmt = db.prepare('SELECT * FROM children')
      const children = stmt.all()
      return { success: true, data: children }
    } catch (err) {
      return {
        success: false,
        error: err instanceof Error ? err.message : 'Unknown error',
      }
    }
  })

  ipcMain.handle('db:getChild', async (event, code: string) => {
    try {
      const db = getDatabase()
      const stmt = db.prepare('SELECT * FROM children WHERE code = ?')
      const child = stmt.get(code)
      return { success: true, data: child }
    } catch (err) {
      return {
        success: false,
        error: err instanceof Error ? err.message : 'Unknown error',
      }
    }
  })

  ipcMain.handle('db:addChild', async (event, child: any) => {
    try {
      const db = getDatabase()
      const stmt = db.prepare(`
        INSERT INTO children (
          code, name, class, region, building, street, floor, apartment,
          childMobile, fatherMobile, motherMobile, homeLine, school,
          isDeacon, confessorFather, notes, attendanceClass, lastConfession,
          createdAt, updatedAt, createdBy
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `)

      stmt.run(
        child.code,
        child.name,
        child.class,
        child.region,
        child.building,
        child.street,
        child.floor,
        child.apartment,
        child.childMobile,
        child.fatherMobile,
        child.motherMobile,
        child.homeLine,
        child.school,
        child.isDeacon ? 1 : 0,
        child.confessorFather,
        child.notes,
        child.attendanceClass,
        child.lastConfession,
        Date.now(),
        Date.now(),
        child.createdBy,
      )

      return { success: true }
    } catch (err) {
      return {
        success: false,
        error: err instanceof Error ? err.message : 'Unknown error',
      }
    }
  })

  ipcMain.handle('db:updateChild', async (event, code: string, updates: any) => {
    try {
      const db = getDatabase()
      const fields = Object.keys(updates)
        .map((key) => `${key} = ?`)
        .join(', ')
      const values = Object.values(updates)

      const stmt = db.prepare(`
        UPDATE children
        SET ${fields}, updatedAt = ?
        WHERE code = ?
      `)

      stmt.run(...values, Date.now(), code)

      return { success: true }
    } catch (err) {
      return {
        success: false,
        error: err instanceof Error ? err.message : 'Unknown error',
      }
    }
  })

  ipcMain.handle('db:deleteChild', async (event, code: string) => {
    try {
      const db = getDatabase()
      const stmt = db.prepare('DELETE FROM children WHERE code = ?')
      stmt.run(code)
      return { success: true }
    } catch (err) {
      return {
        success: false,
        error: err instanceof Error ? err.message : 'Unknown error',
      }
    }
  })

  // Attendance handlers
  ipcMain.handle('db:recordAttendance', async (event, code: string, date: string, time: string) => {
    try {
      const db = getDatabase()
      const stmt = db.prepare(`
        INSERT OR REPLACE INTO attendance (date, childCode, time, updatedAt)
        VALUES (?, ?, ?, ?)
      `)
      stmt.run(date, code, time, Date.now())
      return { success: true }
    } catch (err) {
      return {
        success: false,
        error: err instanceof Error ? err.message : 'Unknown error',
      }
    }
  })

  ipcMain.handle('db:getAttendance', async (event, date: string) => {
    try {
      const db = getDatabase()
      const stmt = db.prepare('SELECT * FROM attendance WHERE date = ?')
      const records = stmt.all(date)
      return { success: true, data: records }
    } catch (err) {
      return {
        success: false,
        error: err instanceof Error ? err.message : 'Unknown error',
      }
    }
  })

  // Sync handlers
  ipcMain.handle('sync:getPendingOperations', async () => {
    try {
      const engine = getSyncEngine()
      const operations = engine.getPendingOperations()
      return { success: true, data: operations }
    } catch (err) {
      return {
        success: false,
        error: err instanceof Error ? err.message : 'Unknown error',
      }
    }
  })

  ipcMain.handle('sync:drainQueue', async () => {
    try {
      const engine = getSyncEngine()
      await engine.drainSyncQueue()
      return { success: true }
    } catch (err) {
      return {
        success: false,
        error: err instanceof Error ? err.message : 'Unknown error',
      }
    }
  })

  // App info handlers
  ipcMain.handle('app:getAppPath', async () => {
    return {
      userData: app.getPath('userData'),
      appVersion: app.getVersion(),
    }
  })
}
