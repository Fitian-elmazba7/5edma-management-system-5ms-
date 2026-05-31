import { getDatabase } from '../sqlite/db'
import { SyncQueueItem } from '@5edma/shared'

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
   * Implementation will connect to Firestore in Phase 3+
   */
  async performFullSync(): Promise<void> {
    // TODO: Implement full sync from Firestore
    console.log('[SyncEngine] Performing full sync...')
  }

  /**
   * Drain sync queue (push pending operations to Firestore)
   * Implementation will connect to Firestore in Phase 3+
   */
  async drainSyncQueue(): Promise<void> {
    const operations = this.getPendingOperations()

    if (operations.length === 0) {
      console.log('[SyncEngine] No pending operations to sync')
      return
    }

    console.log(`[SyncEngine] Draining ${operations.length} pending operations...`)

    // TODO: Implement Firestore batch writes
    // For now, just clear the queue after demo sync
    for (const op of operations) {
      try {
        // await firebaseAPI.sync(op)
        this.markSynced(op.id)
      } catch (err) {
        console.error(`[SyncEngine] Failed to sync ${op.id}:`, err)
        this.incrementRetry(op.id)

        // Retry max 3 times
        const updatedOp = this.getPendingOperations().find((o) => o.id === op.id)
        if (updatedOp && updatedOp.retries >= 3) {
          console.warn(`[SyncEngine] Giving up on ${op.id} after 3 retries`)
          this.markSynced(op.id)
        }
      }
    }

    console.log('[SyncEngine] Sync complete')
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
