import { functions } from './firebase'
import { httpsCallable } from 'firebase/functions'
import { UserRole } from '@5edma/shared'

export interface InviteUserResponse {
  success: boolean
  uid: string
  email: string
  resetLink: string
}

/**
 * Invite a new user (admin only)
 * Creates a Firebase Auth user and Firestore user document with the specified role
 */
export async function inviteUser(
  email: string,
  role: UserRole,
  displayName?: string,
): Promise<InviteUserResponse> {
  const inviteUserFunction = httpsCallable<
    {
      email: string
      role: UserRole
      displayName?: string
    },
    InviteUserResponse
  >(functions, 'inviteUser')

  const result = await inviteUserFunction({
    email,
    role,
    displayName,
  })

  return result.data
}

/**
 * Delete a user (admin only)
 */
export async function deleteUserAccount(uid: string): Promise<{ success: boolean }> {
  const deleteUserFunction = httpsCallable<{ uid: string }, { success: boolean }>(
    functions,
    'deleteUser',
  )

  const result = await deleteUserFunction({ uid })
  return result.data
}

/**
 * Update last sign-in time (called after user logs in)
 */
export async function updateLastSignIn(): Promise<{ success: boolean; uid: string }> {
  const updateLastSignInFunction = httpsCallable<
    Record<string, never>,
    { success: boolean; uid: string }
  >(functions, 'updateLastSignIn')

  const result = await updateLastSignInFunction({})
  return result.data
}
