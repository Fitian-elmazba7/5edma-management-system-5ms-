import Database from 'better-sqlite3'
import { getDatabasePath } from '../utils/platform'

const dbPath = getDatabasePath()

let db: Database.Database | null = null

export function initializeDatabase(): Database.Database {
  if (db) return db

  db = new Database(dbPath)

  // Enable foreign keys
  db.pragma('foreign_keys = ON')

  // Create tables
  createTables()

  return db
}

export function getDatabase(): Database.Database {
  if (!db) {
    throw new Error('Database not initialized. Call initializeDatabase() first.')
  }
  return db
}

function createTables() {
  if (!db) throw new Error('Database not initialized')

  // Children table
  db.exec(`
    CREATE TABLE IF NOT EXISTS children (
      code TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      class TEXT NOT NULL,
      region TEXT,
      building TEXT,
      street TEXT,
      floor TEXT,
      apartment TEXT,
      childMobile TEXT,
      fatherMobile TEXT,
      motherMobile TEXT,
      homeLine TEXT,
      school TEXT,
      isDeacon BOOLEAN DEFAULT 0,
      confessorFather TEXT,
      notes TEXT,
      attendanceClass TEXT,
      lastConfession TEXT,
      createdAt INTEGER,
      updatedAt INTEGER,
      createdBy TEXT
    )
  `)

  // Attendance table
  db.exec(`
    CREATE TABLE IF NOT EXISTS attendance (
      date TEXT PRIMARY KEY,
      childCode TEXT,
      time TEXT,
      serviceDay BOOLEAN DEFAULT 0,
      createdBy TEXT,
      updatedAt INTEGER,
      FOREIGN KEY (childCode) REFERENCES children(code)
    )
  `)

  // Settings table
  db.exec(`
    CREATE TABLE IF NOT EXISTS settings (
      key TEXT PRIMARY KEY,
      value TEXT
    )
  `)

  // Sync queue (for offline changes)
  db.exec(`
    CREATE TABLE IF NOT EXISTS sync_queue (
      id TEXT PRIMARY KEY,
      operation TEXT NOT NULL,
      collection TEXT NOT NULL,
      documentId TEXT NOT NULL,
      data TEXT NOT NULL,
      timestamp INTEGER,
      retries INTEGER DEFAULT 0
    )
  `)
}

export function closeDatabase() {
  if (db) {
    db.close()
    db = null
  }
}
