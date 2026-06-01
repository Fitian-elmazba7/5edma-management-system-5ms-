import React, { useEffect, useState } from 'react';
import { useNavigation } from '../context/NavigationContext';
import { GlassCard, CopticButton, CopticInput, DataTable } from '../components/coptic';

const Users: React.FC = () => {
  const { setCurrentSection } = useNavigation();
  const [searchTerm, setSearchTerm] = useState('');
  const [users, setUsers] = useState([
    { id: 1, name: 'Ahmed Hassan', email: 'ahmed@example.com', role: 'Admin', status: 'Active' },
    { id: 2, name: 'Sarah Mikhael', email: 'sarah@example.com', role: 'Moderator', status: 'Active' },
    { id: 3, name: 'John Girgis', email: 'john@example.com', role: 'Member', status: 'Active' },
    { id: 4, name: 'Mary Kamel', email: 'mary@example.com', role: 'Member', status: 'Inactive' },
  ]);

  useEffect(() => {
    setCurrentSection('admin');
  }, [setCurrentSection]);

  const filteredUsers = users.filter(user =>
    user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-navy-bg p-6 md:p-8">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="font-display font-bold text-4xl text-cream mb-2">Users</h1>
          <p className="font-body text-text-muted text-lg">Manage community members and permissions</p>
        </div>

        {/* Controls */}
        <GlassCard variant="default">
          <div className="flex flex-col md:flex-row gap-4 items-start md:items-end">
            <div className="flex-1">
              <CopticInput
                label="Search Users"
                type="text"
                placeholder="Search by name or email..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            <div className="flex gap-2">
              <CopticButton variant="primary">Add User</CopticButton>
              <CopticButton variant="secondary">Import</CopticButton>
            </div>
          </div>
        </GlassCard>

        {/* Users Table */}
        <GlassCard variant="default">
          <h2 className="font-display font-semibold text-xl text-cream mb-4">
            {filteredUsers.length} Users
          </h2>
          <DataTable
            columns={[
              { key: 'name', label: 'Name' },
              { key: 'email', label: 'Email' },
              { key: 'role', label: 'Role' },
              { key: 'status', label: 'Status', render: (status) => (
                <span className={`inline-block px-3 py-1 rounded-full text-xs font-bold ${
                  status === 'Active' 
                    ? 'bg-green-500/20 text-green-300' 
                    : 'bg-gray-500/20 text-gray-300'
                }`}>
                  {status}
                </span>
              )},
            ]}
            data={filteredUsers}
          />
        </GlassCard>
      </div>
    </div>
  );
};

export default Users;
