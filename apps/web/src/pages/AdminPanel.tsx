import React, { useEffect, useState } from 'react';
import { useNavigation } from '../context/NavigationContext';
import { GlassCard, CopticButton, DataTable } from '../components/coptic';

const AdminPanel: React.FC = () => {
  const { setCurrentSection } = useNavigation();
  const [roles, setRoles] = useState([
    { id: 1, name: 'Admin', members: 4, color: 'bg-red-500/30', borderColor: 'border-l-red-500' },
    { id: 2, name: 'Moderator', members: 12, color: 'bg-orange-500/30', borderColor: 'border-l-orange-500' },
    { id: 3, name: 'Member', members: 247, color: 'bg-blue-500/30', borderColor: 'border-l-blue-500' },
  ]);

  useEffect(() => {
    setCurrentSection('admin');
  }, [setCurrentSection]);

  return (
    <div className="min-h-screen bg-navy-bg p-6 md:p-8">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="font-display font-bold text-4xl text-cream mb-2">Administration</h1>
          <p className="font-body text-text-muted text-lg">Manage roles, permissions, and community settings</p>
        </div>

        {/* Role Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {roles.map((role) => (
            <GlassCard key={role.id} variant="with-top-border">
              <div className="space-y-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h2 className="font-display font-semibold text-xl text-cream">{role.name}</h2>
                    <p className="text-gold-accent text-sm font-bold uppercase mt-1">Role</p>
                  </div>
                  <div className={`w-3 h-3 rounded-full ${role.color}`} />
                </div>
                <div className="border-t border-gold-primary/20 pt-4">
                  <div className="text-3xl font-display font-bold text-gold-primary mb-1">
                    {role.members}
                  </div>
                  <div className="text-text-muted text-sm font-body">Members in this role</div>
                </div>
                <div className="flex gap-2">
                  <CopticButton variant="secondary" className="flex-1 text-xs">
                    Manage
                  </CopticButton>
                  <CopticButton variant="text" className="flex-1 text-xs">
                    View
                  </CopticButton>
                </div>
              </div>
            </GlassCard>
          ))}
        </div>

        {/* Main Content Area */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Section - Left (2 columns) */}
          <div className="lg:col-span-2 space-y-6">
            {/* Recent Admin Actions */}
            <GlassCard variant="default">
              <h2 className="font-display font-semibold text-xl text-cream mb-4">
                Recent Admin Actions
              </h2>
              <div className="space-y-3">
                <div className="flex justify-between items-start p-4 bg-navy-light/20 rounded-lg border-l-4 border-l-gold-primary">
                  <div>
                    <div className="text-cream font-semibold">User Added: Ahmed Hassan</div>
                    <div className="text-text-muted text-sm">Role: Member</div>
                  </div>
                  <div className="text-gold-accent text-xs font-bold">2h ago</div>
                </div>
                <div className="flex justify-between items-start p-4 bg-navy-light/20 rounded-lg border-l-4 border-l-gold-primary">
                  <div>
                    <div className="text-cream font-semibold">Role Changed: Sarah Mikhael</div>
                    <div className="text-text-muted text-sm">Member → Moderator</div>
                  </div>
                  <div className="text-gold-accent text-xs font-bold">5h ago</div>
                </div>
                <div className="flex justify-between items-start p-4 bg-navy-light/20 rounded-lg border-l-4 border-l-gold-primary">
                  <div>
                    <div className="text-cream font-semibold">Settings Updated</div>
                    <div className="text-text-muted text-sm">Attendance policy modified</div>
                  </div>
                  <div className="text-gold-accent text-xs font-bold">1d ago</div>
                </div>
              </div>
            </GlassCard>

            {/* Permissions Table */}
            <GlassCard variant="default">
              <h2 className="font-display font-semibold text-xl text-cream mb-4">Role Permissions</h2>
              <DataTable
                columns={[
                  { key: 'permission', label: 'Permission' },
                  { key: 'admin', label: 'Admin' },
                  { key: 'moderator', label: 'Moderator' },
                  { key: 'member', label: 'Member' },
                ]}
                data={[
                  { permission: 'View Dashboard', admin: '✓', moderator: '✓', member: '✓' },
                  { permission: 'Manage Members', admin: '✓', moderator: '✓', member: '✗' },
                  { permission: 'View Reports', admin: '✓', moderator: '✓', member: '✗' },
                  { permission: 'Edit Settings', admin: '✓', moderator: '✗', member: '✗' },
                  { permission: 'Audit Logs', admin: '✓', moderator: '✗', member: '✗' },
                ]}
              />
            </GlassCard>
          </div>

          {/* Sidebar - Right */}
          <div className="space-y-6">
            {/* Quick Stats */}
            <GlassCard variant="stat">
              <div className="text-gold-accent text-xs font-bold uppercase tracking-wider mb-2">
                Total Users
              </div>
              <div className="text-cream text-3xl font-display font-bold mb-1">263</div>
              <div className="text-text-muted text-sm font-body">Active accounts</div>
            </GlassCard>

            {/* Admin Actions */}
            <GlassCard variant="default">
              <h3 className="font-display font-semibold text-lg text-gold-accent mb-4">
                Admin Actions
              </h3>
              <div className="space-y-2 flex flex-col">
                <CopticButton variant="primary" className="text-sm">
                  Add New User
                </CopticButton>
                <CopticButton variant="secondary" className="text-sm">
                  Edit Roles
                </CopticButton>
                <CopticButton variant="secondary" className="text-sm">
                  View Audit Log
                </CopticButton>
                <CopticButton variant="text" className="text-sm">
                  System Settings
                </CopticButton>
              </div>
            </GlassCard>

            {/* System Health */}
            <GlassCard variant="with-top-border">
              <h3 className="font-display font-semibold text-gold-accent text-sm uppercase mb-3">
                System Health
              </h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between items-center">
                  <span className="text-text-muted">API Status</span>
                  <span className="inline-block w-2 h-2 bg-green-500 rounded-full" />
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-text-muted">Database</span>
                  <span className="inline-block w-2 h-2 bg-green-500 rounded-full" />
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-text-muted">Storage</span>
                  <span className="inline-block w-2 h-2 bg-green-500 rounded-full" />
                </div>
              </div>
            </GlassCard>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminPanel;
