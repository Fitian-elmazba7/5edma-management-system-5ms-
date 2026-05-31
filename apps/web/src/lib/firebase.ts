import { initializeApp } from 'firebase/app'
import { getAuth, connectAuthEmulator, type Auth } from 'firebase/auth'
import { getFirestore, connectFirestoreEmulator, type Firestore } from 'firebase/firestore'
import { getStorage, connectStorageEmulator, type FirebaseStorage } from 'firebase/storage'
import { getFunctions, connectFunctionsEmulator, type Functions } from 'firebase/functions'
import { type FirebaseApp } from 'firebase/app'

interface FirebaseConfig {
  apiKey: string
  authDomain: string
  projectId: string
  storageBucket: string
  messagingSenderId: string
  appId: string
}

const firebaseConfig: FirebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
}

// Initialize Firebase
const app: FirebaseApp = initializeApp(firebaseConfig)

// Initialize Firebase Authentication and get a reference to the service
export const auth: Auth = getAuth(app)

// Initialize Firestore
export const db: Firestore = getFirestore(app)

// Initialize Storage
export const storage: FirebaseStorage = getStorage(app)

// Initialize Cloud Functions
export const functions: Functions = getFunctions(app)

// Development: Connect to emulators if in development and they're available
if (import.meta.env.DEV) {
  try {
    // Check if already connected to avoid re-connection errors
    if (auth.emulatorConfig === null) {
      connectAuthEmulator(auth, 'http://localhost:9099')
    }
  } catch (error) {
    // Emulator not available or already connected
    console.debug('Auth emulator connection skipped:', error instanceof Error ? error.message : 'Unknown error')
  }

  try {
    if (!db.app._deleted) {
      connectFirestoreEmulator(db, 'localhost', 8080)
    }
  } catch (error) {
    // Emulator not available or already connected
    console.debug('Firestore emulator connection skipped:', error instanceof Error ? error.message : 'Unknown error')
  }

  try {
    connectStorageEmulator(storage, 'localhost', 9199)
  } catch (error) {
    // Emulator not available or already connected
    console.debug('Storage emulator connection skipped:', error instanceof Error ? error.message : 'Unknown error')
  }

  try {
    connectFunctionsEmulator(functions, 'localhost', 5001)
  } catch (error) {
    // Emulator not available or already connected
    console.debug('Functions emulator connection skipped:', error instanceof Error ? error.message : 'Unknown error')
  }
}

export default app
