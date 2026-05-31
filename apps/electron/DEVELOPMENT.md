# Electron Development Guide

## Quick Start

### Prerequisites

- Node.js 18+
- pnpm
- Windows 10+ (for packaging)

### Development Setup

```bash
# From project root
cd apps/electron

# Install dependencies
pnpm install

# Run in development mode
pnpm dev
```

This will:
1. Compile TypeScript with `tsc`
2. Launch Electron pointing to `dist/main.js`
3. Open developer tools for debugging

## File Structure

```
src/
├── main.ts              # Electron main process entry point
├── preload.ts           # Context isolation bridge
├── ipc/
│   └── handlers.ts      # IPC event handlers (database, file dialogs, sync)
├── sqlite/
│   └── db.ts            # SQLite database initialization and queries
├── sync/
│   └── SyncEngine.ts    # Offline sync engine
└── utils/
    └── platform.ts      # Platform-specific utilities
```

## Available Commands

```bash
# Development
pnpm dev              # Run Electron with hot reload

# Building
pnpm build            # TypeScript compilation + Vite bundling
pnpm dist             # Full build + create installer (.exe)
pnpm package          # Build without publishing

# Linting
pnpm typecheck        # Run TypeScript type checker
```

## Debugging

### Main Process
- Open Electron DevTools: F12 in the app window
- DevTools automatically opens in dev mode
- Check console for main process logs

### SQLite Database
Database file location (varies by OS):
- **Windows:** `%APPDATA%/5edma/data/local.db`
- **macOS:** `~/Library/Application Support/5edma/data/local.db`
- **Linux:** `~/.config/5edma/data/local.db`

Use SQLite browser to inspect:
```bash
# Example on Windows
sqlite3 %APPDATA%/5edma/data/local.db
```

### Sync Queue
Check pending operations:
```sql
SELECT * FROM sync_queue ORDER BY timestamp DESC;
```

## Architecture

### IPC Communication

The preload script exposes a safe API to the renderer:

```typescript
// In renderer process
const children = await window.electronAPI.db.getChildren()
const { filePath } = await window.electronAPI.openFile({
  filters: [{ name: 'Excel', extensions: ['xlsx', 'xls'] }]
})
```

### Offline Sync Flow

```
User Action (Offline)
    ↓
Renderer Process (React)
    ↓
IPC Call (preload → main)
    ↓
SQLite Insert + sync_queue entry
    ↓
User comes online
    ↓
SyncEngine.drainQueue()
    ↓
Firestore batch write
    ↓
Remove from sync_queue
```

### Database Schema

**children table** — all child records with contact info
- `code` (PK): unique ID
- `name`, `class`, region/address fields
- Mobile/phone contact fields
- `createdAt`, `updatedAt` (Unix ms timestamps)

**attendance table** — daily attendance records
- `date` (PK): YYYY-MM-DD format
- `childCode`, `time`: attended at this time
- `serviceDay`: boolean flag
- `updatedAt`: last modified timestamp

**sync_queue table** — pending Firestore writes
- `id` (PK): unique operation ID
- `operation`: "CREATE", "UPDATE", "DELETE"
- `collection`: "children", "attendance", "settings"
- `documentId`: Firestore document ID
- `data`: JSON payload
- `timestamp`, `retries`: sync metadata

**settings table** — key-value configuration
- `key` (PK): setting name
- `value`: JSON or plain text value

## Building for Distribution

### Create Windows Installer

```bash
pnpm dist
```

Output: `dist/5edma Management System Setup 1.0.0.exe`

### NSIS Configuration

The installer is configured in `electron-builder.json`:
- **One-click install:** Disabled (user can choose directory)
- **Desktop shortcut:** Automatically created
- **Start menu entry:** Automatically created
- **Uninstaller:** Included

### Code Signing (Optional)

For production releases, add certificate to `electron-builder.json`:

```json
{
  "win": {
    "certificateFile": "path/to/certificate.pfx",
    "certificatePassword": "your-password"
  }
}
```

## Environment Variables

Create `.env.local` in `apps/electron/` for dev overrides:

```
VITE_DEV_SERVER_URL=http://localhost:5173
NODE_ENV=development
```

These are automatically set during `pnpm dev`.

## Common Issues

### Database Lock Error
If SQLite reports "database is locked":
1. Close all instances of the app
2. Delete the database file (it will be recreated)
3. Force sync from Firestore on next launch

### White Screen on Startup
1. Check DevTools console for errors
2. Verify SQLite database path exists: `%APPDATA%/5edma/data/`
3. Ensure preload.js exists in dist/

### Sync Not Working
1. Verify Firebase credentials in `.env`
2. Check sync_queue table for pending operations
3. Inspect Firestore rules in Firebase Console
4. Review main process logs (F12 → console tab)

## Testing

### Manual Testing Checklist

- [ ] Launch app, login with test credentials
- [ ] Register a child offline (disconnect internet)
- [ ] Reconnect and verify sync completes
- [ ] Export attendance to Excel
- [ ] Import Excel file with new children
- [ ] Verify data appears in Firestore Console
- [ ] Test role-based access (login as viewer/servant)

### Automated Tests

Create tests in `src/__tests__/`:

```bash
# Example: test sync engine
pnpm test -- sync.test.ts
```

## Performance Tips

1. **Minimize IPC calls** — batch operations when possible
2. **Use SQLite for reads** — Firestore reads are async
3. **Index frequently-queried columns** — e.g., attendance.date
4. **Lazy load reports** — paginate large result sets
5. **Cache UI state** — don't refetch on every render

## Deployment

### Release Checklist

- [ ] Bump version in `package.json`
- [ ] Update `CHANGELOG.md`
- [ ] Run full test suite
- [ ] Build and test installer on clean Windows VM
- [ ] Tag release in git: `git tag v1.0.0`
- [ ] Push installer to release server
- [ ] Update auto-update manifest (if applicable)

### Auto-Updates

To enable in-app updates, configure electron-builder:

```json
{
  "publish": {
    "provider": "s3",
    "bucket": "your-bucket",
    "path": "/releases"
  }
}
```

Then in main.ts:

```typescript
import { autoUpdater } from 'electron-updater'
autoUpdater.checkForUpdatesAndNotify()
```

## Resources

- [Electron Security Best Practices](https://www.electronjs.org/docs/tutorial/security)
- [electron-builder Documentation](https://www.electron.build/)
- [better-sqlite3 API](https://github.com/WiseLibs/better-sqlite3/wiki/API)
- [IPC Patterns](https://www.electronjs.org/docs/api/ipc-main)
