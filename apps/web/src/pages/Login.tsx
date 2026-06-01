import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { GlassCard, CopticButton, CopticInput } from '../components/coptic';

const Login: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    if (email && password) {
      navigate('/dashboard');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-navy-bg via-navy-deep to-navy-bg flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-gold-primary rounded-lg flex items-center justify-center text-navy-bg font-bold text-3xl mx-auto mb-4">
            ⊕
          </div>
          <h1 className="font-display font-bold text-3xl text-cream">5EDMA</h1>
          <p className="font-body text-text-muted mt-2">Community Management</p>
        </div>

        {/* Login Form */}
        <GlassCard variant="default" className="space-y-6">
          <div>
            <h2 className="font-display font-bold text-2xl text-cream mb-1">Welcome Back</h2>
            <p className="font-body text-text-muted text-sm">Sign in to your account</p>
          </div>

          <div className="space-y-4">
            <CopticInput
              label="Email Address"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <CopticInput
              label="Password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <div className="flex items-center justify-between text-sm">
            <label className="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" className="w-4 h-4" />
              <span className="font-body text-text-muted">Remember me</span>
            </label>
            <a href="#" className="font-body text-gold-primary hover:text-gold-accent transition-colors">
              Forgot password?
            </a>
          </div>

          <CopticButton variant="primary" onClick={handleLogin} className="w-full">
            Sign In
          </CopticButton>

          <div className="text-center text-sm">
            <span className="font-body text-text-muted">Don't have an account? </span>
            <button
              onClick={() => navigate('/registration')}
              className="font-body text-gold-primary hover:text-gold-accent transition-colors font-semibold"
            >
              Create one
            </button>
          </div>
        </GlassCard>

        {/* Footer */}
        <div className="text-center mt-6 text-sm font-body text-text-muted">
          <p>Protected with enterprise-grade security</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
