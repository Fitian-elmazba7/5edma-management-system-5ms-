import * as functions from 'firebase-functions'
import * as admin from 'firebase-admin'

/**
 * Sync offline changes to Firestore
 * Called by the app when coming back online to upload local changes
 */
export const syncOfflineChanges = functions.https.onCall(
  async (data, context) => {
    if (!context.auth) {
      throw new functions.https.HttpsError(
        'unauthenticated',
        'User must be authenticated',
      )
    }

    const db = admin.firestore()
    const { changes } = data
    const uid = context.auth.uid

    if (!Array.isArray(changes) || changes.length === 0) {
      return {
        success: true,
        syncedCount: 0,
        message: 'No changes to sync',
      }
    }

    const batch = db.batch()
    let syncedCount = 0

    try {
      for (const change of changes) {
        const { collection, docId, operation, data: docData } = change

        const docRef = db.collection(collection).doc(docId)

        if (operation === 'set') {
          batch.set(docRef, docData, { merge: true })
          syncedCount++
        } else if (operation === 'delete') {
          batch.delete(docRef)
          syncedCount++
        }
      }

      await batch.commit()

      // Update sync metadata
      await db.collection('sync').doc(uid).set(
        {
          lastSyncTime: admin.firestore.FieldValue.serverTimestamp(),
          syncedChanges: syncedCount,
        },
        { merge: true },
      )

      console.log(`[syncOfflineChanges] Synced ${syncedCount} changes for user ${uid}`)

      return {
        success: true,
        syncedCount,
        message: `Synced ${syncedCount} changes`,
      }
    } catch (error) {
      console.error(`[syncOfflineChanges] Error for user ${uid}:`, error)
      throw new functions.https.HttpsError(
        'internal',
        `Sync failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
      )
    }
  },
)
