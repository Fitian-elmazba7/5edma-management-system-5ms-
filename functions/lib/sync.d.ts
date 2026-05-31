import * as functions from 'firebase-functions';
/**
 * Sync offline changes to Firestore
 * Called by the app when coming back online to upload local changes
 */
export declare const syncOfflineChanges: functions.HttpsFunction & functions.Runnable<any>;
