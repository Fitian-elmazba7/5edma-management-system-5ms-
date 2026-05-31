import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';

export const setUserRole = functions.https.onCall(async (data, context) => {
  if (!context.auth) {
    throw new functions.https.HttpsError(
      'unauthenticated',
      'User must be authenticated'
    );
  }

  const callerRole = context.auth.token.role;
  if (callerRole !== 'admin') {
    throw new functions.https.HttpsError(
      'permission-denied',
      'Only admins can set user roles'
    );
  }

  const { uid, role } = data;
  const validRoles = ['admin', 'servant', 'viewer', 'user'];

  if (!validRoles.includes(role)) {
    throw new functions.https.HttpsError(
      'invalid-argument',
      `Invalid role. Must be one of: ${validRoles.join(', ')}`
    );
  }

  try {
    await admin.auth().setCustomUserClaims(uid, { role });
    return { success: true, message: `User ${uid} role set to ${role}` };
  } catch (error) {
    throw new functions.https.HttpsError(
      'internal',
      `Error setting user role: ${error}`
    );
  }
});

export const onUserCreate = functions.auth.user().onCreate(async (user) => {
  await admin.firestore().collection('users').doc(user.uid).set({
    email: user.email,
    displayName: user.displayName || '',
    role: 'user',
    createdAt: admin.firestore.FieldValue.serverTimestamp(),
  });
});
