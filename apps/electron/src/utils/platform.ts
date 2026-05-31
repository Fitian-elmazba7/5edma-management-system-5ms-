import { app } from 'electron'
import path from 'path'
import fs from 'fs'

/**
 * Platform and file system utilities for Electron main process
 */

export function getDataDirectory(): string {
  const userData = app.getPath('userData')
  const dataDir = path.join(userData, 'data')

  // Create directory if it doesn't exist
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true })
  }

  return dataDir
}

export function getLogsDirectory(): string {
  const userData = app.getPath('userData')
  const logsDir = path.join(userData, 'logs')

  if (!fs.existsSync(logsDir)) {
    fs.mkdirSync(logsDir, { recursive: true })
  }

  return logsDir
}

export function getDatabasePath(): string {
  return path.join(getDataDirectory(), 'local.db')
}

export function getAppDataPath(): string {
  return app.getPath('userData')
}

export function isProduction(): boolean {
  return !process.env.VITE_DEV_SERVER_URL
}

export function isDevelopment(): boolean {
  return !!process.env.VITE_DEV_SERVER_URL
}

export function getAppVersion(): string {
  return app.getVersion()
}

export function getPlatform(): string {
  return process.platform
}

export function getArchitecture(): string {
  return process.arch
}
