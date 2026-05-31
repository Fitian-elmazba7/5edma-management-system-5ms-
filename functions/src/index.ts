import * as functions from 'firebase-functions'
import * as admin from 'firebase-admin'

import { syncOfflineChanges } from './sync'

admin.initializeApp()

const db = admin.firestore()
const auth = admin.auth()

/**
 * Set custom claims when user document is created or updated
 * This function syncs the user's role from Firestore to Auth custom claims
 */
export const setCustomClaims = functions.firestore
  .document('users/{uid}')
  .onWrite(async (change, context) => {
    const uid = context.params.uid
    const afterData = change.after.data()

    if (!afterData) {
      // Document deleted, remove custom claims
      try {
        await auth.setCustomUserClaims(uid, { role: 'user' })
        console.log(`[setCustomClaims] Removed custom claims for user ${uid}`)
      } catch (error) {
        console.error(`[setCustomClaims] Error removing claims for ${uid}:`, error)
      }
      return
    }

    const role = afterData.role || 'user'

    try {
      await auth.setCustomUserClaims(uid, { role })
      console.log(`[setCustomClaims] Set role '${role}' for user ${uid}`)
    } catch (error) {
      console.error(`[setCustomClaims] Error setting claims for ${uid}:`, error)
      throw error
    }
  })

/**
 * Create user document when new Auth user is created
 * Called from the app when a new user is invited/created
 */
export const createUserDocument = functions.auth.user().onCreate(async (user) => {
  try {
    await db.collection('users').doc(user.uid).set(
      {
        email: user.email,
        displayName: user.displayName || '',
        role: 'viewer', // default role
        createdAt: admin.firestore.FieldValue.serverTimestamp(),
        lastSignIn: admin.firestore.FieldValue.serverTimestamp(),
      },
      { merge: true },
    )
    console.log(`[createUserDocument] Created user doc for ${user.uid}`)
  } catch (error) {
    console.error(`[createUserDocument] Error creating user doc for ${user.uid}:`, error)
    throw error
  }
})

/**
 * Update last sign-in time on user document
 */
export const updateLastSignIn = functions.https.onCall(async (data, context) => {
  if (!context.auth) {
    throw new functions.https.HttpsError('unauthenticated', 'User must be authenticated')
  }

  const uid = context.auth.uid

  try {
    await db
      .collection('users')
      .doc(uid)
      .update({
        lastSignIn: admin.firestore.FieldValue.serverTimestamp(),
      })

    return { success: true, uid }
  } catch (error) {
    console.error(`[updateLastSignIn] Error for ${uid}:`, error)
    throw new functions.https.HttpsError('internal', 'Failed to update last sign-in')
  }
})

/**
 * Invite a new user and set their role
 * Only admins can call this
 */
export const inviteUser = functions.https.onCall(async (data, context) => {
  if (!context.auth) {
    throw new functions.https.HttpsError('unauthenticated', 'User must be authenticated')
  }

  // Check if caller is admin
  const callerDoc = await db.collection('users').doc(context.auth.uid).get()
  if (!callerDoc.exists || callerDoc.data()?.role !== 'admin') {
    throw new functions.https.HttpsError('permission-denied', 'Only admins can invite users')
  }

  const { email, displayName, role } = data

  if (!email || !role) {
    throw new functions.https.HttpsError(
      'invalid-argument',
      'Email and role are required',
    )
  }

  if (!['admin', 'servant', 'viewer', 'user'].includes(role)) {
    throw new functions.https.HttpsError('invalid-argument', 'Invalid role')
  }

  try {
    // Create auth user
    const userRecord = await auth.createUser({
      email,
      displayName: displayName || '',
      password: Math.random().toString(36).slice(-12), // Temporary password
    })

    // Create user document with role
    await db.collection('users').doc(userRecord.uid).set({
      email,
      displayName: displayName || '',
      role,
      createdAt: admin.firestore.FieldValue.serverTimestamp(),
      createdBy: context.auth.uid,
    })

    // Send password reset email so user can set their own password
    const resetLink = await auth.generatePasswordResetLink(email)

    console.log(`[inviteUser] Created user ${userRecord.uid} with role '${role}'`)

    return {
      success: true,
      uid: userRecord.uid,
      email: userRecord.email,
      resetLink,
    }
  } catch (error) {
    console.error('[inviteUser] Error:', error)
    throw new functions.https.HttpsError(
      'internal',
      error instanceof Error ? error.message : 'Failed to invite user',
    )
  }
})

/**
 * Delete a user (admin only)
 */
export const deleteUser = functions.https.onCall(async (data, context) => {
  if (!context.auth) {
    throw new functions.https.HttpsError('unauthenticated', 'User must be authenticated')
  }

  // Check if caller is admin
  const callerDoc = await db.collection('users').doc(context.auth.uid).get()
  if (!callerDoc.exists || callerDoc.data()?.role !== 'admin') {
    throw new functions.https.HttpsError('permission-denied', 'Only admins can delete users')
  }

  const { uid } = data

  if (!uid) {
    throw new functions.https.HttpsError('invalid-argument', 'User UID is required')
  }

  try {
    // Delete auth user
    await auth.deleteUser(uid)

    // Delete user document
    await db.collection('users').doc(uid).delete()

    console.log(`[deleteUser] Deleted user ${uid}`)

    return { success: true, uid }
  } catch (error) {
    console.error('[deleteUser] Error:', error)
    throw new functions.https.HttpsError(
      'internal',
      error instanceof Error ? error.message : 'Failed to delete user',
    )
  }
})

/**
 * Update user role (admin only)
 */
export const updateUserRole = functions.https.onCall(async (data, context) => {
  if (!context.auth) {
    throw new functions.https.HttpsError('unauthenticated', 'User must be authenticated')
  }

  // Check if caller is admin
  const callerDoc = await db.collection('users').doc(context.auth.uid).get()
  if (!callerDoc.exists || callerDoc.data()?.role !== 'admin') {
    throw new functions.https.HttpsError('permission-denied', 'Only admins can update roles')
  }

  const { uid, role } = data

  if (!uid || !role) {
    throw new functions.https.HttpsError('invalid-argument', 'User UID and role are required')
  }

  if (!['admin', 'servant', 'viewer', 'user'].includes(role)) {
    throw new functions.https.HttpsError('invalid-argument', 'Invalid role')
  }

  try {
    // Update user document
    await db.collection('users').doc(uid).update({
      role,
      updatedAt: admin.firestore.FieldValue.serverTimestamp(),
      updatedBy: context.auth.uid,
    })

    // Custom claims are automatically updated by the onWrite trigger
    console.log(`[updateUserRole] Updated role for user ${uid} to '${role}'`)

    return { success: true, uid, role }
  } catch (error) {
    console.error('[updateUserRole] Error:', error)
    throw new functions.https.HttpsError(
      'internal',
      error instanceof Error ? error.message : 'Failed to update user role',
    )
  }
})

// Export sync function
export { syncOfflineChanges }
