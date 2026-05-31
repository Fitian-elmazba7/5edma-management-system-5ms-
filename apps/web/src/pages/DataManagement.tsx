import { useState, useEffect } from 'react'
import { GlassCard, GlassButton, GlassInput, ChildCard } from '../components/ui'
import { useChildrenStore } from '../store/children'
import { Child } from '@5edma/shared'

export default function DataManagementPage() {
  const {
    children,
    fetchChildren,
    createChild,
    updateChild,
    deleteChild,
    loading,
  } = useChildrenStore()

  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [selectedClass, setSelectedClass] = useState('الكل')
  const [searchQuery, setSearchQuery] = useState('')
  const [showAddModal, setShowAddModal] = useState(false)
  const [selectedChild, setSelectedChild] = useState<Child | null>(null)
  const [showEditModal, setShowEditModal] = useState(false)

  const [formData, setFormData] = useState<Partial<Child>>({
    code: '',
    name: '',
    class: 'الصف الأول',
    region: '',
    building: '',
    street: '',
    floor: '',
    apartment: '',
    childMobile: '',
    fatherMobile: '',
    motherMobile: '',
    homeLine: '',
    school: '',
  })

  useEffect(() => {
    fetchChildren()
  }, [])

  const classes = ['الكل', 'الصف الأول', 'الصف الثاني', 'الصف الثالث']

  const filteredChildren = children.filter((child) => {
    const matchesClass =
      selectedClass === 'الكل' || child.class === selectedClass
    const matchesSearch =
      child.name.includes(searchQuery) || child.code.includes(searchQuery)
    return matchesClass && matchesSearch
  })

  const handleAddChild = async () => {
    if (!formData.code || !formData.name) {
      alert('يجب إدخال الرقم والاسم على الأقل')
      return
    }

    try {
      await createChild(formData as Omit<Child, 'createdAt' | 'updatedAt' | 'createdBy'>)
      setShowAddModal(false)
      setFormData({
        code: '',
        name: '',
        class: 'الصف الأول',
      })
    } catch (err) {
      alert('خطأ في إضافة الطفل')
    }
  }

  const handleEditChild = async () => {
    if (!selectedChild) return

    try {
      await updateChild(selectedChild.code, formData)
      setShowEditModal(false)
      setSelectedChild(null)
    } catch (err) {
      alert('خطأ في تحديث بيانات الطفل')
    }
  }

  const handleDeleteChild = async (code: string) => {
    if (window.confirm('هل تريد حذف هذا الطفل؟')) {
      try {
        await deleteChild(code)
      } catch (err) {
        alert('خطأ في حذف الطفل')
      }
    }
  }

  return (
    <div className="min-h-screen bg-glass-bg p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gradient mb-2">
              📊 إدارة البيانات
            </h1>
            <p className="text-glass-muted">
              إدارة بيانات الأطفال والاستيراد من Excel
            </p>
          </div>
          <GlassButton
            variant="primary"
            onClick={() => {
              setFormData({
                code: '',
                name: '',
                class: 'الصف الأول',
              })
              setShowAddModal(true)
            }}
          >
            + إضافة طفل جديد
          </GlassButton>
        </div>

        {/* Filters */}
        <GlassCard className="mb-6">
          <div className="flex gap-4 flex-wrap">
            <div className="flex-1 min-w-64">
              <GlassInput
                placeholder="بحث بالاسم أو الرقم..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>

            <div className="flex gap-2">
              {classes.map((className) => (
                <button
                  key={className}
                  onClick={() => setSelectedClass(className)}
                  className={`px-4 py-2 rounded-lg transition-colors font-medium text-sm ${
                    selectedClass === className
                      ? 'bg-blue-600/20 text-blue-300 border border-blue-500/30'
                      : 'glass text-glass-text hover:bg-blue-500/10'
                  }`}
                >
                  {className}
                </button>
              ))}
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => setViewMode('grid')}
                className={`px-3 py-2 rounded-lg ${
                  viewMode === 'grid'
                    ? 'bg-blue-600/20 text-blue-300'
                    : 'glass text-glass-text'
                }`}
              >
                📊
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`px-3 py-2 rounded-lg ${
                  viewMode === 'list'
                    ? 'bg-blue-600/20 text-blue-300'
                    : 'glass text-glass-text'
                }`}
              >
                📋
              </button>
            </div>
          </div>
        </GlassCard>

        {/* Content */}
        {loading ? (
          <GlassCard className="text-center py-8">
            <p className="text-glass-muted">جاري التحميل...</p>
          </GlassCard>
        ) : viewMode === 'grid' ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredChildren.map((child) => (
              <ChildCard
                key={child.code}
                child={child}
                onClick={() => {
                  setSelectedChild(child)
                  setFormData(child)
                  setShowEditModal(true)
                }}
                actions={
                  <button
                    onClick={() => handleDeleteChild(child.code)}
                    className="px-2 py-1 rounded bg-red-500/20 text-red-300 hover:bg-red-500/30 text-xs"
                  >
                    حذف
                  </button>
                }
              />
            ))}
          </div>
        ) : (
          <GlassCard>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-glass-border">
                    <th className="px-4 py-3 text-right font-semibold text-glass-text">
                      الرقم
                    </th>
                    <th className="px-4 py-3 text-right font-semibold text-glass-text">
                      الاسم
                    </th>
                    <th className="px-4 py-3 text-right font-semibold text-glass-text">
                      الصف
                    </th>
                    <th className="px-4 py-3 text-right font-semibold text-glass-text">
                      المدرسة
                    </th>
                    <th className="px-4 py-3 text-right font-semibold text-glass-text">
                      الإجراءات
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {filteredChildren.map((child) => (
                    <tr
                      key={child.code}
                      className="border-b border-glass-border/50 hover:bg-blue-500/5"
                    >
                      <td className="px-4 py-3 text-glass-text">{child.code}</td>
                      <td className="px-4 py-3 text-glass-text">{child.name}</td>
                      <td className="px-4 py-3 text-glass-muted">{child.class}</td>
                      <td className="px-4 py-3 text-glass-muted">
                        {child.school}
                      </td>
                      <td className="px-4 py-3 space-x-2">
                        <button
                          onClick={() => {
                            setSelectedChild(child)
                            setFormData(child)
                            setShowEditModal(true)
                          }}
                          className="px-3 py-1 rounded bg-blue-500/20 text-blue-300 hover:bg-blue-500/30 text-xs"
                        >
                          تحرير
                        </button>
                        <button
                          onClick={() => handleDeleteChild(child.code)}
                          className="px-3 py-1 rounded bg-red-500/20 text-red-300 hover:bg-red-500/30 text-xs"
                        >
                          حذف
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </GlassCard>
        )}

        {/* Add/Edit Modal */}
        {(showAddModal || showEditModal) && (
          <div className="modal-overlay">
            <div className="modal-content max-w-2xl max-h-96 overflow-y-auto">
              <div className="modal-header">
                <h2 className="modal-title">
                  {showAddModal ? 'إضافة طفل جديد' : 'تحرير بيانات الطفل'}
                </h2>
                <button
                  className="modal-close"
                  onClick={() => {
                    setShowAddModal(false)
                    setShowEditModal(false)
                    setSelectedChild(null)
                  }}
                >
                  ✕
                </button>
              </div>

              <div className="modal-body space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <GlassInput
                    label="الرقم"
                    value={formData.code || ''}
                    onChange={(e) =>
                      setFormData({ ...formData, code: e.target.value })
                    }
                    disabled={showEditModal}
                  />
                  <GlassInput
                    label="الاسم"
                    value={formData.name || ''}
                    onChange={(e) =>
                      setFormData({ ...formData, name: e.target.value })
                    }
                  />
                  <div>
                    <label className="block text-sm font-medium text-glass-text mb-2">
                      الصف
                    </label>
                    <select
                      value={formData.class || 'الصف الأول'}
                      onChange={(e) =>
                        setFormData({ ...formData, class: e.target.value as any })
                      }
                      className="glass-select w-full"
                    >
                      <option>الصف الأول</option>
                      <option>الصف الثاني</option>
                      <option>الصف الثالث</option>
                    </select>
                  </div>
                  <GlassInput
                    label="المدرسة"
                    value={formData.school || ''}
                    onChange={(e) =>
                      setFormData({ ...formData, school: e.target.value })
                    }
                  />
                </div>

                <h3 className="text-lg font-semibold text-glass-text pt-4 border-t border-glass-border">
                  بيانات الاتصال
                </h3>

                <div className="grid grid-cols-2 gap-4">
                  <GlassInput
                    label="موبايل الطفل"
                    value={formData.childMobile || ''}
                    onChange={(e) =>
                      setFormData({ ...formData, childMobile: e.target.value })
                    }
                  />
                  <GlassInput
                    label="موبايل الأب"
                    value={formData.fatherMobile || ''}
                    onChange={(e) =>
                      setFormData({ ...formData, fatherMobile: e.target.value })
                    }
                  />
                  <GlassInput
                    label="موبايل الأم"
                    value={formData.motherMobile || ''}
                    onChange={(e) =>
                      setFormData({ ...formData, motherMobile: e.target.value })
                    }
                  />
                  <GlassInput
                    label="تليفون البيت"
                    value={formData.homeLine || ''}
                    onChange={(e) =>
                      setFormData({ ...formData, homeLine: e.target.value })
                    }
                  />
                </div>
              </div>

              <div className="modal-footer">
                <GlassButton
                  variant="secondary"
                  onClick={() => {
                    setShowAddModal(false)
                    setShowEditModal(false)
                    setSelectedChild(null)
                  }}
                >
                  إلغاء
                </GlassButton>
                <GlassButton
                  variant="primary"
                  onClick={() => {
                    if (showAddModal) {
                      handleAddChild()
                    } else {
                      handleEditChild()
                    }
                  }}
                >
                  {showAddModal ? 'إضافة' : 'حفظ التغييرات'}
                </GlassButton>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
