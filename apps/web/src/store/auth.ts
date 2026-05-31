import { create } from 'zustand'
import { auth, db } from '../lib/firebase'
import {
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  User as FirebaseUser,
} from 'firebase/auth'
import { doc, getDoc } from 'firebase/firestore'
import { User, UserRole } from '@5edma/shared'

interface AuthState {
  user: User | null
  firebaseUser: FirebaseUser | null
  loading: boolean
  error: string | null

  // Actions
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  initializeAuth: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  firebaseUser: null,
  loading: true,
  error: null,

  login: async (email: string, password: string) => {
    try {
      set({ error: null, loading: true })
      await signInWithEmailAndPassword(auth, email, password)
      // User state will be updated by onAuthStateChanged listener
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to login',
      })
      throw error
    } finally {
      set({ loading: false })
    }
  },

  logout: async () => {
    try {
      set({ error: null, loading: true })
      await signOut(auth)
      set({ user: null, firebaseUser: null })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to logout',
      })
      throw error
    } finally {
      set({ loading: false })
    }
  },

  initializeAuth: () => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      if (firebaseUser) {
        let role: UserRole = (firebaseUser.customClaims?.role || 'viewer') as UserRole

        // Fallback: check Firestore user document for role
        try {
          const userDocRef = doc(db, 'users', firebaseUser.uid)
          const userDocSnap = await getDoc(userDocRef)
          if (userDocSnap.exists()) {
            const firestoreRole = userDocSnap.data().role
            if (firestoreRole) {
              role = firestoreRole as UserRole
            }
          }
        } catch (error) {
          console.warn('Failed to fetch user role from Firestore:', error)
        }

        // Convert Firebase user to our User type
        const user: User = {
          uid: firebaseUser.uid,
          email: firebaseUser.email || '',
          displayName: firebaseUser.displayName || '',
          role,
          createdAt: firebaseUser.metadata.creationTime
            ? new Date(firebaseUser.metadata.creationTime).getTime()
            : Date.now(),
        }
        set({ user, firebaseUser, loading: false })
      } else {
        set({ user: null, firebaseUser: null, loading: false })
      }
    })

    return unsubscribe
  },
}))
