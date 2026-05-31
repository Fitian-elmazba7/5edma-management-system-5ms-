# Electron ↔ React Integration Guide

## Overview

The Electron app reuses the same React UI code as the web version, but routes data through:
1. **Main process** (Electron) → SQLite database
2. **IPC bridge** → context-isolated preload script
3. **Renderer process** (React) → data adapter layer

## How It Works

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ Electron Renderer (React UI)                                │
│                                                              │
│  useChildrenStore()  →  data/adapter.ts  →  window.electronAPI
│  useAttendanceStore()   (detects environment)   (IPC bridge)
│                                                 │
└─────────────────────────────────┬──────────────┘
                                  │
                    IPC Communication (async)
                                  │
┌─────────────────────────────────▼──────────────────────────┐
│ Electron Main Process                                        │
│                                                              │
│  ipc/handlers.ts                                             │
│  ├── db.getChildren()  →  sqlite/db.ts  →  children table  │
│  ├── db.addChild()                    → INSERT/UPDATE       │
│  ├── db.recordAttendance()                                  │
│  ├── sync.getPendingOperations()  →  sync_queue table      │
│  └── sync.drainQueue()  →  SyncEngine.ts  →  Firestore    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Data Flow: User Registers Child

**Online (Electron):**
```
User adds child in UI
    ↓
createChild() → adapter
    ↓
window.electronAPI.db.addChild(child)
    ↓
IPC to main process
    ↓
SQLite INSERT into children table
    ↓
Sync automatically pushes to Firestore
```

**Offline (Electron):**
```
User adds child (no internet)
    ↓
createChild() → adapter
    ↓
window.electronAPI.db.addChild(child)
    ↓
SQLite INSERT + sync_queue INSERT
    ↓
[orange status bar: "1 pending"]
    ↓
User connects to internet
    ↓
Auto-drain: sync_queue → Firestore via batch write
    ↓
Status updates to green
```

## Using the Data Adapter

### In React Components

Instead of importing `firestore/children.ts` directly:

```typescript
// ❌ DON'T: Hard-coded Firestore
import { getAllChildren } from '@/lib/firestore/children'

// ✅ DO: Use adapter
import { getAllChildren } from '@/lib/data/adapter'

function ChildList() {
  useEffect(() => {
    getAllChildren().then(setChildren)
  }, [])
}
```

The adapter automatically:
- Detects if running in Electron vs web
- Calls SQLite via IPC in Electron
- Calls Firestore directly in web

### In Zustand Stores

Update your stores to use the adapter:

```typescript
import { getAllChildren, createChild, updateChild } from '@/lib/data/adapter'

const useChildrenStore = create((set) => ({
  fetchChildren: async () => {
    try {
      const children = await getAllChildren()
      set({ children })
    } catch (err) {
      set({ error: err.message })
    }
  },
  
  addChild: async (child: Child) => {
    await createChild(child)
    set((state) => ({
      children: [...state.children, child]
    }))
  },
}))
```

## Offline Sync Mechanics

### Sync Queue Schema

When offline, operations queue in SQLite:

```sql
INSERT INTO sync_queue (
  id, operation, collection, documentId, data, timestamp, retries
) VALUES (
  'op-12345',
  'CREATE',
  'children',
  'code-101',
  '{"name":"احمد","class":"الصف الأول",...}',
  1719819000000,
  0
)
```

### Retry Logic

`SyncEngine.drainQueue()` implements exponential backoff:

```
Retry 0: immediate
Retry 1: 1 second delay
Retry 2: 2 seconds delay
Retry 3: max 3 retries → give up, stay in queue

User can manually trigger retry via status indicator
```

### Last-Write-Wins Conflict Resolution

If device A and B both modify child code-101 offline:

```
Device A: updates name to "Ahmed" at 14:30:00 → updatedAt: 14:30:00
Device B: updates class to "الصف الثاني" at 14:29:00 → updatedAt: 14:29:00

On sync:
  Device A's change wins (newer timestamp)
  Device B's change is discarded (older timestamp)
```

This matches the current JSON-based approach.

## Connection Status Indicator

The `ConnectionStatusIndicator` component displays:

- 🟢 **Green pulse** — Syncing in progress
- 🟢 **Green dot** — Online and synced
- 🔴 **Red dot** — Offline mode
- **Text** — "Offline mode" or "2 pending"

Add it to your layout:

```typescript
import { ConnectionStatusIndicator } from '@/hooks/useConnectionStatus'

function Layout() {
  return (
    <>
      <Header />
      <Main />
      <ConnectionStatusIndicator />
    </>
  )
}
```

## Testing Offline Mode

### Simulate Offline in Electron

1. **Method 1: DevTools**
   - F12 in Electron window
   - Network tab → Offline checkbox

2. **Method 2: System**
   - Disconnect WiFi / unplug ethernet
   - App continues working from SQLite

### Test Checklist

- [ ] Add child while offline
- [ ] Verify child appears in UI immediately
- [ ] Check sync_queue table: `SELECT * FROM sync_queue`
- [ ] Reconnect to internet
- [ ] Wait 5 seconds for auto-sync
- [ ] Check Firestore Console — child now present
- [ ] Close app and reopen
- [ ] Verify child still there (persisted in SQLite)
- [ ] Login to web version — see same child
- [ ] Modify child on web
- [ ] Close web, reopen Electron
- [ ] Verify Electron has latest changes

## Database Synchronization

### First Launch

On first app launch, the sync engine:

```typescript
// In SyncEngine.ts
async performFullSync() {
  1. Fetch all Firestore collections (children, attendance, settings)
  2. Populate local SQLite tables
  3. Store lastSyncTimestamp
  4. Set up incremental sync for future changes
}
```

### Incremental Sync

After first sync, only pull changes since `lastSyncTimestamp`:

```sql
-- Instead of:
SELECT * FROM children

-- Pull only changes since last sync:
SELECT * FROM children WHERE updatedAt > ?lastSyncTimestamp
```

This is implemented in `SyncEngine.drainSyncQueue()`.

## Firebase Rules for Electron Clients

In `firestore.rules`, treat Electron clients as authenticated:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /children/{code} {
      allow read, write: if request.auth != null
    }
    match /attendance/{date} {
      allow read, write: if request.auth != null
    }
  }
}
```

Electron always includes Firebase auth token (cached on device).

## Common Issues & Solutions

### Issue: "Database is locked"

**Cause:** Multiple processes accessing SQLite simultaneously

**Solution:**
```typescript
// In db.ts - use WAL mode for better concurrency
db.pragma('journal_mode = WAL')
```

### Issue: Data appears in SQLite but not Firestore

**Cause:** Sync queue has failed operations, stuck in retries

**Solutions:**
1. Check main process logs (F12 in app)
2. Manual sync via status indicator
3. Verify Firebase auth token hasn't expired
4. Check Firestore security rules

### Issue: Electron app shows stale data

**Cause:** SQLite cache is older than Firestore

**Solution:** Force full sync on next launch:
```typescript
// In main.ts
if (process.argv.includes('--full-sync')) {
  await getSyncEngine().performFullSync()
}
```

## Performance Tips

1. **Batch operations** — Insert 100 children in one transaction
2. **Index the sync_queue** — Add index on `collection, timestamp`
3. **Lazy-sync reports** — Don't block UI, sync in background
4. **Cache frequently-read settings** — Don't query per-render

## Migration Guide (PyQt5 → Electron)

### Import Old JSON Database

```typescript
// 1. Export JSON from old PyQt5 app
// 2. In Electron: call import endpoint
const json = await readFile('database.json')
const data = JSON.parse(json)

// 3. Bulk insert to SQLite
data.children.forEach(child => {
  db.prepare('INSERT INTO children (...) VALUES (...)').run(...)
})

// 4. Push to Firestore via normal sync
await syncEngine.drainQueue()
```

### User Migration

1. First launch of Electron app
2. Show setup wizard
3. Download existing data from old system
4. Bulk import via Excel or direct JSON
5. Verify count matches old system
6. Archive old app

## Next Steps

After Phase 6 is complete:

- **Phase 7:** Firebase deployment (Hosting + Security Rules)
- Set up auto-update mechanism for Electron installer
- Create GitHub Actions workflow for building installers
- Add telemetry/analytics (optional)
- User onboarding guide for first-time setup
