import {
  collection,
  doc,
  getDoc,
  getDocs,
  addDoc,
  updateDoc,
  deleteDoc,
  query,
  where,
  QueryConstraint,
  serverTimestamp,
} from 'firebase/firestore'
import { db } from '../firebase'
import { Child } from '@5edma/shared'

const COLLECTION = 'children'

// Create a new child
export async function createChild(
  childData: Omit<Child, 'createdAt' | 'updatedAt' | 'createdBy'>,
  userId: string,
): Promise<Child> {
  const now = Date.now()
  const docRef = await addDoc(collection(db, COLLECTION), {
    ...childData,
    createdAt: now,
    updatedAt: now,
    createdBy: userId,
  })

  return {
    ...childData,
    createdAt: now,
    updatedAt: now,
    createdBy: userId,
  } as Child
}

// Get a child by code
export async function getChildByCode(code: string): Promise<Child | null> {
  const docRef = doc(db, COLLECTION, code)
  const docSnap = await getDoc(docRef)

  if (!docSnap.exists()) return null

  return {
    ...docSnap.data(),
    code: docSnap.id,
  } as Child
}

// Get all children
export async function getAllChildren(): Promise<Child[]> {
  const querySnapshot = await getDocs(collection(db, COLLECTION))
  return querySnapshot.docs.map(
    (docSnap) =>
      ({
        ...docSnap.data(),
        code: docSnap.id,
      }) as Child,
  )
}

// Get children by class
export async function getChildrenByClass(className: string): Promise<Child[]> {
  const q = query(
    collection(db, COLLECTION),
    where('class', '==', className),
  )
  const querySnapshot = await getDocs(q)

  return querySnapshot.docs.map(
    (docSnap) =>
      ({
        ...docSnap.data(),
        code: docSnap.id,
      }) as Child,
  )
}

// Update a child
export async function updateChild(
  code: string,
  updates: Partial<Omit<Child, 'code' | 'createdAt' | 'createdBy'>>,
): Promise<void> {
  const docRef = doc(db, COLLECTION, code)
  await updateDoc(docRef, {
    ...updates,
    updatedAt: Date.now(),
  })
}

// Delete a child
export async function deleteChild(code: string): Promise<void> {
  const docRef = doc(db, COLLECTION, code)
  await deleteDoc(docRef)
}

// Batch import children (incremental - skips existing codes)
export async function importChildren(
  childrenData: Omit<Child, 'createdAt' | 'updatedAt' | 'createdBy'>[],
  userId: string,
): Promise<{ imported: number; skipped: number; errors: string[] }> {
  const imported: number[] = []
  const skipped: number[] = []
  const errors: string[] = []

  for (const child of childrenData) {
    try {
      const existing = await getChildByCode(child.code)
      if (existing) {
        skipped.push(1)
      } else {
        await createChild(child, userId)
        imported.push(1)
      }
    } catch (err) {
      errors.push(`Error importing ${child.code}: ${err instanceof Error ? err.message : 'Unknown error'}`)
    }
  }

  return {
    imported: imported.length,
    skipped: skipped.length,
    errors,
  }
}
