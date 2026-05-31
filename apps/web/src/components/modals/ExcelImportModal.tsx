import { useState } from 'react'
import { GlassButton, GlassCard } from '../ui'
import { parseExcelFile, validateChildrenData } from '../../lib/excel'
import { Child } from '@5edma/shared'

interface ExcelImportModalProps {
  onClose: () => void
  onImport: (children: Child[], incremental: boolean) => Promise<void>
}

export default function ExcelImportModal({
  onClose,
  onImport,
}: ExcelImportModalProps) {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [parsedData, setParsedData] = useState<Child[] | null>(null)
  const [incremental, setIncremental] = useState(true)
  const [importErrors, setImportErrors] = useState<string[]>([])

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (!selectedFile) return

    setFile(selectedFile)
    setError(null)
    setParsedData(null)
    setImportErrors([])

    setLoading(true)
    try {
      const result = await parseExcelFile(selectedFile)

      if (result.errors.length > 0) {
        setImportErrors(result.errors)
      }

      // Validate the parsed data
      const { valid, invalid } = validateChildrenData(result.data)

      if (invalid.length > 0) {
        setImportErrors([
          ...result.errors,
          ...invalid.map((item) => `${item.data.code}: ${item.error}`),
        ])
      }

      setParsedData(valid)
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'فشل في قراءة الملف',
      )
    } finally {
      setLoading(false)
    }
  }

  const handleImport = async () => {
    if (!parsedData || parsedData.length === 0) {
      setError('لا توجد بيانات صحيحة للاستيراد')
      return
    }

    setLoading(true)
    try {
      await onImport(parsedData, incremental)
      onClose()
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'فشل الاستيراد',
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="modal-overlay">
      <div className="modal-content max-w-2xl max-h-96 overflow-y-auto">
        <div className="modal-header">
          <h2 className="modal-title">استيراد من Excel</h2>
          <button className="modal-close" onClick={onClose}>
            ✕
          </button>
        </div>

        <div className="modal-body space-y-4">
          {/* File Upload */}
          <div className="glass p-4 rounded-lg border-2 border-dashed border-glass-border">
            <input
              type="file"
              accept=".xlsx,.xls,.csv"
              onChange={handleFileSelect}
              className="w-full"
              disabled={loading}
            />
            <p className="text-sm text-glass-muted mt-2">
              ادعم صيغ: Excel (.xlsx, .xls), CSV
            </p>
          </div>

          {/* Options */}
          {parsedData && parsedData.length > 0 && (
            <label className="flex items-center gap-3 text-glass-text cursor-pointer">
              <input
                type="checkbox"
                checked={incremental}
                onChange={(e) => setIncremental(e.target.checked)}
                className="rounded w-4 h-4"
              />
              <span className="text-sm">
                الوضع التزايدي (تخطي الأطفال الموجودين)
              </span>
            </label>
          )}

          {/* Results */}
          {parsedData && parsedData.length > 0 && (
            <div className="space-y-2">
              <div className="glass p-3 rounded-lg">
                <p className="text-sm text-glass-muted">سيتم استيراد</p>
                <p className="text-2xl font-bold text-green-300">
                  {parsedData.length} طفل/ة
                </p>
              </div>
            </div>
          )}

          {/* Errors */}
          {importErrors.length > 0 && (
            <div className="glass p-3 rounded-lg border border-red-500/30 bg-red-500/10">
              <p className="text-sm font-medium text-red-300 mb-2">
                تنبيهات / أخطاء ({importErrors.length})
              </p>
              <div className="space-y-1 max-h-32 overflow-y-auto">
                {importErrors.slice(0, 10).map((err, i) => (
                  <p key={i} className="text-xs text-red-200">
                    • {err}
                  </p>
                ))}
                {importErrors.length > 10 && (
                  <p className="text-xs text-red-200">
                    ... و {importErrors.length - 10} أخطاء أخرى
                  </p>
                )}
              </div>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="p-3 rounded-lg bg-red-500/20 border border-red-500/50">
              <p className="text-red-300 text-sm">{error}</p>
            </div>
          )}

          {/* Summary */}
          {file && (
            <p className="text-xs text-glass-muted">
              الملف: {file.name} ({(file.size / 1024).toFixed(1)} KB)
            </p>
          )}
        </div>

        <div className="modal-footer">
          <GlassButton variant="secondary" onClick={onClose}>
            إلغاء
          </GlassButton>
          <GlassButton
            variant="primary"
            onClick={handleImport}
            disabled={!parsedData || parsedData.length === 0 || loading}
            loading={loading}
          >
            استيراد الآن
          </GlassButton>
        </div>
      </div>
    </div>
  )
}
