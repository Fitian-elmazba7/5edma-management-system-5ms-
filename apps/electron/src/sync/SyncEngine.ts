import { getDatabase } from '../sqlite/db'
import { db as firestore } from '../lib/firebase-config'
import { collection, getDocs, doc, getDoc, writeBatch } from 'firebase/firestore'
import { SyncQueueItem, Child, AttendanceRecord, Settings } from '@5edma/shared'

/**
 * SyncEngine handles offline->online synchronization for Electron app
 * - Queues writes when offline
 * - Syncs on reconnect using last-write-wins strategy
 */

export class SyncEngine {
  private db: any

  constructor() {
    this.db = getDatabase()
  }

  /**
   * Add an operation to the sync queue (called when offline)
   */
  queueOperation(item: Omit<SyncQueueItem, 'id' | 'retries'>): void {
    const id = `${item.collection}-${item.documentId}-${Date.now()}`
    const stmt = this.db.prepare(`
      INSERT INTO sync_queue (id, operation, collection, documentId, data, timestamp)
      VALUES (?, ?, ?, ?, ?, ?)
    `)

    stmt.run(
      id,
      item.operation,
      item.collection,
      item.documentId,
      JSON.stringify(item.data),
      item.timestamp,
    )
  }

  /**
   * Get all pending sync operations
   */
  getPendingOperations(): SyncQueueItem[] {
    const stmt = this.db.prepare('SELECT * FROM sync_queue ORDER BY timestamp ASC')
    const rows = stmt.all()

    return rows.map((row: any) => ({
      id: row.id,
      operation: row.operation,
      collection: row.collection,
      documentId: row.documentId,
      data: JSON.parse(row.data),
      timestamp: row.timestamp,
      retries: row.retries,
    }))
  }

  /**
   * Mark an operation as synced and remove from queue
   */
  markSynced(id: string): void {
    const stmt = this.db.prepare('DELETE FROM sync_queue WHERE id = ?')
    stmt.run(id)
  }

  /**
   * Increment retry count for an operation
   */
  incrementRetry(id: string): void {
    const stmt = this.db.prepare('UPDATE sync_queue SET retries = retries + 1 WHERE id = ?')
    stmt.run(id)
  }

  /**
   * Clear all sync operations (should only be called after successful full sync)
   */
  clearQueue(): void {
    const stmt = this.db.prepare('DELETE FROM sync_queue')
    stmt.run()
  }

  /**
   * Perform full sync (pull all data from Firestore and update local DB)
   */
  async performFullSync(): Promise<void> {
    console.log('[SyncEngine] Performing full sync from Firestore...')

    try {
      // Sync children collection
      const childrenSnap = await getDocs(collection(firestore, 'children'))
      const childrenStmt = this.db.prepare(`
        INSERT OR REPLACE INTO children (code, name, class, region, building, street, floor, apartment,
          childMobile, fatherMobile, motherMobile, homeLine, school, isDeacon, confessorFather, notes,
          attendanceClass, lastConfession, createdAt, updatedAt, createdBy)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `)

      for (const doc of childrenSnap.docs) {
        const data = doc.data() as Child
        childrenStmt.run(
          data.code,
          data.name,
          data.class,
          data.region,
          data.building,
          data.street,
          data.floor,
          data.apartment,
          data.childMobile,
          data.fatherMobile,
          data.motherMobile,
          data.homeLine,
          data.school,
          data.isDeacon ? 1 : 0,
          data.confessorFather,
          data.notes,
          data.attendanceClass,
          data.lastConfession,
          data.createdAt,
          data.updatedAt,
          data.createdBy,
        )
      }

      // Sync attendance collection
      const attendanceSnap = await getDocs(collection(firestore, 'attendance'))
      const attendanceStmt = this.db.prepare(`
        INSERT OR REPLACE INTO attendance (date, records, serviceDay, createdBy, updatedAt)
        VALUES (?, ?, ?, ?, ?)
      `)

      for (const doc of attendanceSnap.docs) {
        const data = doc.data() as AttendanceRecord
        attendanceStmt.run(
          data.date,
          JSON.stringify(data.records),
          data.serviceDay ? 1 : 0,
          data.createdBy,
          data.updatedAt,
        )
      }

      // Sync settings
      const settingsDoc = await getDoc(doc(firestore, 'settings', 'config'))
      if (settingsDoc.exists()) {
        const data = settingsDoc.data() as Settings
        const settingsStmt = this.db.prepare(`
          INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)
        `)
        settingsStmt.run('serviceDay', data.serviceDay)
        settingsStmt.run('serviceTime', data.serviceTime)
        settingsStmt.run('orgName', data.orgName)
      }

      console.log('[SyncEngine] Full sync completed successfully')
    } catch (err) {
      console.error('[SyncEngine] Full sync failed:', err)
      throw err
    }
  }

  /**
   * Drain sync queue (push pending operations to Firestore)
   */
  async drainSyncQueue(): Promise<void> {
    const operations = this.getPendingOperations()

    if (operations.length === 0) {
      console.log('[SyncEngine] No pending operations to sync')
      return
    }

    console.log(`[SyncEngine] Draining ${operations.length} pending operations...`)

    try {
      // Group operations by type for batch processing
      const batch = writeBatch(firestore)
      let operationCount = 0

      for (const op of operations) {
        try {
          const docRef = doc(firestore, op.collection, op.documentId)

          if (op.operation === 'create' || op.operation === 'update') {
            batch.set(docRef, op.data, { merge: true })
          } else if (op.operation === 'delete') {
            batch.delete(docRef)
          }

          operationCount++

          // Firebase batch has a 500 operation limit
          if (operationCount >= 500) {
            await batch.commit()
            console.log('[SyncEngine] Committed batch of 500 operations')
            operationCount = 0
          }
        } catch (err) {
          console.error(`[SyncEngine] Error processing operation ${op.id}:`, err)
          this.incrementRetry(op.id)

          const updatedOp = this.getPendingOperations().find((o) => o.id === op.id)
          if (updatedOp && updatedOp.retries >= 3) {
            console.warn(`[SyncEngine] Giving up on ${op.id} after 3 retries`)
            this.markSynced(op.id)
          }
        }
      }

      // Commit remaining operations
      if (operationCount > 0) {
        await batch.commit()
        console.log(`[SyncEngine] Committed final batch of ${operationCount} operations`)
      }

      // Mark all successfully synced operations as complete
      for (const op of operations) {
        const updatedOp = this.getPendingOperations().find((o) => o.id === op.id)
        if (!updatedOp || updatedOp.retries < 3) {
          this.markSynced(op.id)
        }
      }

      console.log('[SyncEngine] Sync queue drained successfully')
    } catch (err) {
      console.error('[SyncEngine] Failed to drain sync queue:', err)
      throw err
    }
  }
}

// Singleton instance
let instance: SyncEngine | null = null

export function getSyncEngine(): SyncEngine {
  if (!instance) {
    instance = new SyncEngine()
  }
  return instance
}
