import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { NavigationProvider } from './context/NavigationContext';
import { TopBar } from './components/TopBar';
import { NavigationSidebar } from './components/NavigationSidebar';
import Dashboard from './pages/Dashboard';
import Home from './pages/Home';
import Login from './pages/Login';
import Registration from './pages/Registration';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <NavigationProvider>
      <Router>
        <div className="flex flex-col min-h-screen bg-navy-bg">
          {/* Top Navigation Bar */}
          <TopBar
            onMenuClick={() => setSidebarOpen(!sidebarOpen)}
            userName="User"
          />

          {/* Main Content with Sidebar */}
          <div className="flex flex-1 overflow-hidden">
            {/* Navigation Sidebar */}
            <NavigationSidebar
              isOpen={sidebarOpen}
              onClose={() => setSidebarOpen(false)}
            />

            {/* Main Content Area */}
            <main className="flex-1 overflow-y-auto">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/registration" element={<Registration />} />
                <Route path="/dashboard" element={<Dashboard />} />
                {/* Additional routes will be added in Phase 4 */}
              </Routes>
            </main>
          </div>
        </div>
      </Router>
    </NavigationProvider>
  );
}

export default App;
