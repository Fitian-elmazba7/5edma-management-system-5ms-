# 5edma Desktop App (Electron)

Desktop application for 5edma Church Attendance Management System with offline support and local database synchronization.

## Features

- **Offline-First**: Full functionality with local SQLite database
- **Auto-Sync**: Automatic synchronization with Firebase Firestore when online
- **Native UI**: Windows native file dialogs and system integration
- **Context Isolation**: Secure IPC with renderer process isolation
- **Session Persistence**: Auto-saves session state on exit

## Development

### Prerequisites

- Node.js 18+
- pnpm

### Setup

```bash
# Install dependencies
pnpm install

# Development mode (watch and rebuild on changes)
pnpm dev

# Build for distribution
pnpm build

# Build installer (.exe)
pnpm dist
```

## Architecture

### Main Process (`src/main.ts`)
- Initializes Electron window
- Sets up SQLite database
- Registers IPC handlers
- Manages application lifecycle

### IPC Handlers (`src/ipc/handlers.ts`)
- Database operations (CRUD for children, attendance)
- File dialog operations
- Sync queue management
- App metadata

### Preload Script (`src/preload.ts`)
- Context isolation bridge
- Safe API exposure to renderer
- Type-safe IPC wrappers

### SQLite Layer (`src/sqlite/db.ts`)
- Database initialization
- Schema setup
- Connection management

### Sync Engine (`src/sync/SyncEngine.ts`)
- Offline operation queuing
- Retry logic with exponential backoff
- Firestore batch write coordination

## Security

- **Context Isolation**: Enabled by default
- **Sandbox**: Enabled for all renderer processes
- **Node Integration**: Disabled
- **Preload Scripts**: Minimal API surface

## Database

### Schema

```sql
-- children table
CREATE TABLE children (
  code TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  ... (all child fields)
)

-- attendance table
CREATE TABLE attendance (
  date TEXT,
  childCode TEXT,
  time TEXT,
  FOREIGN KEY (childCode) REFERENCES children(code)
)

-- sync_queue table
CREATE TABLE sync_queue (
  id TEXT PRIMARY KEY,
  operation TEXT NOT NULL,
  collection TEXT NOT NULL,
  documentId TEXT NOT NULL,
  data TEXT NOT NULL,
  timestamp INTEGER,
  retries INTEGER DEFAULT 0
)
```

## Offline Sync

### When Offline
1. User operations are recorded in `sync_queue`
2. Each operation has a unique ID and timestamp
3. Retry counter tracks failed attempts

### When Online
1. App automatically checks for pending operations
2. Drains sync queue in order (FIFO)
3. Last-write-wins conflict resolution
4. Successful operations removed from queue

## Building

### Development Build
```bash
pnpm dev
```
Runs Electron with hot reload from Vite dev server.

### Production Build
```bash
pnpm build
```
Creates optimized build with:
- TypeScript compilation
- Code minification
- Asset optimization

### Installer
```bash
pnpm dist
```
Generates Windows NSIS installer (.exe) at `dist/5edma Management System Setup 1.0.0.exe`

### Installer Options

The NSIS installer includes:
- One-click installation
- Desktop shortcut creation
- Start menu entry
- Automatic updates support
- Uninstaller

## File Structure

```
apps/electron/
├── src/
│   ├── main.ts              # Main process entry
│   ├── preload.ts           # Preload script
│   ├── ipc/handlers.ts      # IPC handlers
│   ├── sqlite/db.ts         # SQLite setup
│   └── sync/SyncEngine.ts   # Sync logic
├── vite.config.ts           # Vite configuration
├── electron-builder.json    # Builder config
└── package.json
```

## Environment Variables

- `VITE_DEV_SERVER_URL`: Dev server URL (auto-set during dev)
- `NODE_ENV`: Development or production

## Tips

- Check `%APPDATA%/5edma/` for local database and logs
- Data is stored in SQLite until synced to Firestore
- Failed sync operations are retried up to 3 times
- Use DevTools (F12) in development to debug
