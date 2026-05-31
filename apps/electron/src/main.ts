import { app, BrowserWindow, Menu } from 'electron'
import path from 'path'
import { initializeDatabase, closeDatabase } from './sqlite/db'
import { registerIpcHandlers } from './ipc/handlers'
import { getSyncEngine } from './sync/SyncEngine'

let mainWindow: BrowserWindow | null

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: true,
    },
  })

  if (process.env.VITE_DEV_SERVER_URL) {
    mainWindow.loadURL(process.env.VITE_DEV_SERVER_URL)
    mainWindow.webContents.openDevTools()
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'))
  }

  mainWindow.on('closed', () => {
    mainWindow = null
  })

  // Create application menu
  createMenu()
}

function createMenu() {
  const template: any = [
    {
      label: 'File',
      submenu: [
        {
          label: 'Exit',
          accelerator: 'CmdOrCtrl+Q',
          click: () => {
            app.quit()
          },
        },
      ],
    },
    {
      label: 'Edit',
      submenu: [
        { role: 'undo' },
        { role: 'redo' },
        { type: 'separator' },
        { role: 'cut' },
        { role: 'copy' },
        { role: 'paste' },
      ],
    },
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { role: 'toggleDevTools' },
      ],
    },
  ]

  const menu = Menu.buildFromTemplate(template)
  Menu.setApplicationMenu(menu)
}

// Initialize app
app.on('ready', () => {
  // Initialize database
  initializeDatabase()

  // Register IPC handlers
  registerIpcHandlers()

  // Create window
  createWindow()

  // Perform full sync on startup
  console.log('[App] Checking for pending sync operations...')
  getSyncEngine().drainSyncQueue().catch((err) => {
    console.error('[App] Sync error:', err)
  })
})

app.on('window-all-closed', () => {
  // Close database before quitting
  closeDatabase()

  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})

// Handle any uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error('[App] Uncaught exception:', error)
})
