import * as functions from 'firebase-functions';
import { syncOfflineChanges } from './sync';
/**
 * Set custom claims when user document is created or updated
 * This function syncs the user's role from Firestore to Auth custom claims
 */
export declare const setCustomClaims: functions.CloudFunction<functions.Change<functions.firestore.DocumentSnapshot>>;
/**
 * Create user document when new Auth user is created
 * Called from the app when a new user is invited/created
 */
export declare const createUserDocument: functions.CloudFunction<import("firebase-admin/lib/auth").UserRecord>;
/**
 * Update last sign-in time on user document
 */
export declare const updateLastSignIn: functions.HttpsFunction & functions.Runnable<any>;
/**
 * Invite a new user and set their role
 * Only admins can call this
 */
export declare const inviteUser: functions.HttpsFunction & functions.Runnable<any>;
/**
 * Delete a user (admin only)
 */
export declare const deleteUser: functions.HttpsFunction & functions.Runnable<any>;
/**
 * Update user role (admin only)
 */
export declare const updateUserRole: functions.HttpsFunction & functions.Runnable<any>;
export { syncOfflineChanges };
