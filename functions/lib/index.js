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
exports.syncOfflineChanges = exports.updateUserRole = exports.deleteUser = exports.inviteUser = exports.updateLastSignIn = exports.createUserDocument = exports.setCustomClaims = void 0;
const functions = __importStar(require("firebase-functions"));
const admin = __importStar(require("firebase-admin"));
const sync_1 = require("./sync");
Object.defineProperty(exports, "syncOfflineChanges", { enumerable: true, get: function () { return sync_1.syncOfflineChanges; } });
admin.initializeApp();
const db = admin.firestore();
const auth = admin.auth();
/**
 * Set custom claims when user document is created or updated
 * This function syncs the user's role from Firestore to Auth custom claims
 */
exports.setCustomClaims = functions.firestore
    .document('users/{uid}')
    .onWrite(async (change, context) => {
    const uid = context.params.uid;
    const afterData = change.after.data();
    if (!afterData) {
        // Document deleted, remove custom claims
        try {
            await auth.setCustomUserClaims(uid, { role: 'user' });
            console.log(`[setCustomClaims] Removed custom claims for user ${uid}`);
        }
        catch (error) {
            console.error(`[setCustomClaims] Error removing claims for ${uid}:`, error);
        }
        return;
    }
    const role = afterData.role || 'user';
    try {
        await auth.setCustomUserClaims(uid, { role });
        console.log(`[setCustomClaims] Set role '${role}' for user ${uid}`);
    }
    catch (error) {
        console.error(`[setCustomClaims] Error setting claims for ${uid}:`, error);
        throw error;
    }
});
/**
 * Create user document when new Auth user is created
 * Called from the app when a new user is invited/created
 */
exports.createUserDocument = functions.auth.user().onCreate(async (user) => {
    try {
        await db.collection('users').doc(user.uid).set({
            email: user.email,
            displayName: user.displayName || '',
            role: 'viewer', // default role
            createdAt: admin.firestore.FieldValue.serverTimestamp(),
            lastSignIn: admin.firestore.FieldValue.serverTimestamp(),
        }, { merge: true });
        console.log(`[createUserDocument] Created user doc for ${user.uid}`);
    }
    catch (error) {
        console.error(`[createUserDocument] Error creating user doc for ${user.uid}:`, error);
        throw error;
    }
});
/**
 * Update last sign-in time on user document
 */
exports.updateLastSignIn = functions.https.onCall(async (data, context) => {
    if (!context.auth) {
        throw new functions.https.HttpsError('unauthenticated', 'User must be authenticated');
    }
    const uid = context.auth.uid;
    try {
        await db
            .collection('users')
            .doc(uid)
            .update({
            lastSignIn: admin.firestore.FieldValue.serverTimestamp(),
        });
        return { success: true, uid };
    }
    catch (error) {
        console.error(`[updateLastSignIn] Error for ${uid}:`, error);
        throw new functions.https.HttpsError('internal', 'Failed to update last sign-in');
    }
});
/**
 * Invite a new user and set their role
 * Only admins can call this
 */
exports.inviteUser = functions.https.onCall(async (data, context) => {
    if (!context.auth) {
        throw new functions.https.HttpsError('unauthenticated', 'User must be authenticated');
    }
    // Check if caller is admin
    const callerDoc = await db.collection('users').doc(context.auth.uid).get();
    if (!callerDoc.exists || callerDoc.data()?.role !== 'admin') {
        throw new functions.https.HttpsError('permission-denied', 'Only admins can invite users');
    }
    const { email, displayName, role } = data;
    if (!email || !role) {
        throw new functions.https.HttpsError('invalid-argument', 'Email and role are required');
    }
    if (!['admin', 'servant', 'viewer', 'user'].includes(role)) {
        throw new functions.https.HttpsError('invalid-argument', 'Invalid role');
    }
    try {
        // Create auth user
        const userRecord = await auth.createUser({
            email,
            displayName: displayName || '',
            password: Math.random().toString(36).slice(-12), // Temporary password
        });
        // Create user document with role
        await db.collection('users').doc(userRecord.uid).set({
            email,
            displayName: displayName || '',
            role,
            createdAt: admin.firestore.FieldValue.serverTimestamp(),
            createdBy: context.auth.uid,
        });
        // Send password reset email so user can set their own password
        const resetLink = await auth.generatePasswordResetLink(email);
        console.log(`[inviteUser] Created user ${userRecord.uid} with role '${role}'`);
        return {
            success: true,
            uid: userRecord.uid,
            email: userRecord.email,
            resetLink,
        };
    }
    catch (error) {
        console.error('[inviteUser] Error:', error);
        throw new functions.https.HttpsError('internal', error instanceof Error ? error.message : 'Failed to invite user');
    }
});
/**
 * Delete a user (admin only)
 */
exports.deleteUser = functions.https.onCall(async (data, context) => {
    if (!context.auth) {
        throw new functions.https.HttpsError('unauthenticated', 'User must be authenticated');
    }
    // Check if caller is admin
    const callerDoc = await db.collection('users').doc(context.auth.uid).get();
    if (!callerDoc.exists || callerDoc.data()?.role !== 'admin') {
        throw new functions.https.HttpsError('permission-denied', 'Only admins can delete users');
    }
    const { uid } = data;
    if (!uid) {
        throw new functions.https.HttpsError('invalid-argument', 'User UID is required');
    }
    try {
        // Delete auth user
        await auth.deleteUser(uid);
        // Delete user document
        await db.collection('users').doc(uid).delete();
        console.log(`[deleteUser] Deleted user ${uid}`);
        return { success: true, uid };
    }
    catch (error) {
        console.error('[deleteUser] Error:', error);
        throw new functions.https.HttpsError('internal', error instanceof Error ? error.message : 'Failed to delete user');
    }
});
/**
 * Update user role (admin only)
 */
exports.updateUserRole = functions.https.onCall(async (data, context) => {
    if (!context.auth) {
        throw new functions.https.HttpsError('unauthenticated', 'User must be authenticated');
    }
    // Check if caller is admin
    const callerDoc = await db.collection('users').doc(context.auth.uid).get();
    if (!callerDoc.exists || callerDoc.data()?.role !== 'admin') {
        throw new functions.https.HttpsError('permission-denied', 'Only admins can update roles');
    }
    const { uid, role } = data;
    if (!uid || !role) {
        throw new functions.https.HttpsError('invalid-argument', 'User UID and role are required');
    }
    if (!['admin', 'servant', 'viewer', 'user'].includes(role)) {
        throw new functions.https.HttpsError('invalid-argument', 'Invalid role');
    }
    try {
        // Update user document
        await db.collection('users').doc(uid).update({
            role,
            updatedAt: admin.firestore.FieldValue.serverTimestamp(),
            updatedBy: context.auth.uid,
        });
        // Custom claims are automatically updated by the onWrite trigger
        console.log(`[updateUserRole] Updated role for user ${uid} to '${role}'`);
        return { success: true, uid, role };
    }
    catch (error) {
        console.error('[updateUserRole] Error:', error);
        throw new functions.https.HttpsError('internal', error instanceof Error ? error.message : 'Failed to update user role');
    }
});
//# sourceMappingURL=index.js.map