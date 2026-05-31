"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.syncOfflineChanges = void 0;
const functions = __importStar(require("firebase-functions"));
const admin = __importStar(require("firebase-admin"));
const db = admin.firestore();
/**
 * Sync offline changes to Firestore
 * Called by the app when coming back online to upload local changes
 */
exports.syncOfflineChanges = functions.https.onCall(async (data, context) => {
    if (!context.auth) {
        throw new functions.https.HttpsError('unauthenticated', 'User must be authenticated');
    }
    const { changes } = data;
    const uid = context.auth.uid;
    if (!Array.isArray(changes) || changes.length === 0) {
        return {
            success: true,
            syncedCount: 0,
            message: 'No changes to sync',
        };
    }
    const batch = db.batch();
    let syncedCount = 0;
    try {
        for (const change of changes) {
            const { collection, docId, operation, data: docData } = change;
            const docRef = db.collection(collection).doc(docId);
            if (operation === 'set') {
                batch.set(docRef, docData, { merge: true });
                syncedCount++;
            }
            else if (operation === 'delete') {
                batch.delete(docRef);
                syncedCount++;
            }
        }
        await batch.commit();
        // Update sync metadata
        await db.collection('sync').doc(uid).set({
            lastSyncTime: admin.firestore.FieldValue.serverTimestamp(),
            syncedChanges: syncedCount,
        }, { merge: true });
        console.log(`[syncOfflineChanges] Synced ${syncedCount} changes for user ${uid}`);
        return {
            success: true,
            syncedCount,
            message: `Synced ${syncedCount} changes`,
        };
    }
    catch (error) {
        console.error(`[syncOfflineChanges] Error for user ${uid}:`, error);
        throw new functions.https.HttpsError('internal', `Sync failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
});
//# sourceMappingURL=sync.js.map