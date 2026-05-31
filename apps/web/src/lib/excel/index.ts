export * from './export'
export * from './import'

export interface ImportResult {
  imported: number
  skipped: number
  errors: string[]
  warnings: string[]
}

export interface ImportOptions {
  incremental?: boolean // Skip existing codes
  validateOnly?: boolean // Just validate, don't import
}
