import { doc, getDoc, setDoc, updateDoc } from 'firebase/firestore'
import { db } from '../firebase'
import { Settings } from '@5edma/shared'

const DOC_ID = 'config'
const COLLECTION = 'settings'

const DEFAULT_SETTINGS: Settings = {
  serviceDay: 'Thursday',
  serviceTime: '19:00',
  orgName: 'الكنيسة القبطية الأرثوذكسية',
}

// Get all settings
export async function getSettings(): Promise<Settings> {
  const docRef = doc(db, COLLECTION, DOC_ID)
  const docSnap = await getDoc(docRef)

  if (!docSnap.exists()) {
    // Initialize with defaults if not exists
    await setDoc(docRef, DEFAULT_SETTINGS)
    return DEFAULT_SETTINGS
  }

  return docSnap.data() as Settings
}

// Update settings
export async function updateSettings(
  updates: Partial<Settings>,
): Promise<void> {
  const docRef = doc(db, COLLECTION, DOC_ID)
  const docSnap = await getDoc(docRef)

  if (!docSnap.exists()) {
    // Create with defaults + updates
    await setDoc(docRef, { ...DEFAULT_SETTINGS, ...updates })
  } else {
    // Update existing
    await updateDoc(docRef, updates)
  }
}

// Get service day
export async function getServiceDay(): Promise<string> {
  const settings = await getSettings()
  return settings.serviceDay
}

// Get service time
export async function getServiceTime(): Promise<string> {
  const settings = await getSettings()
  return settings.serviceTime
}

// Update service day
export async function updateServiceDay(day: string): Promise<void> {
  await updateSettings({ serviceDay: day })
}

// Update service time
export async function updateServiceTime(time: string): Promise<void> {
  await updateSettings({ serviceTime: time })
}

// Get organization name
export async function getOrgName(): Promise<string> {
  const settings = await getSettings()
  return settings.orgName
}

// Update organization name
export async function updateOrgName(name: string): Promise<void> {
  await updateSettings({ orgName: name })
}

// Reset settings to defaults
export async function resetSettings(): Promise<void> {
  const docRef = doc(db, COLLECTION, DOC_ID)
  await setDoc(docRef, DEFAULT_SETTINGS)
}
