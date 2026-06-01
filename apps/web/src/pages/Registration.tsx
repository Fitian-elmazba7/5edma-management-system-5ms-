import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { GlassCard, CopticButton, CopticInput } from '../components/coptic';

const Registration: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  const handleRegister = () => {
    const newErrors: Record<string, string> = {};
    
    if (!formData.name) newErrors.name = 'Name is required';
    if (!formData.email) newErrors.email = 'Email is required';
    if (!formData.password) newErrors.password = 'Password is required';
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    if (Object.keys(newErrors).length === 0) {
      navigate('/dashboard');
    } else {
      setErrors(newErrors);
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
          <p className="font-body text-text-muted mt-2">Join Our Community</p>
        </div>

        {/* Registration Form */}
        <GlassCard variant="default" className="space-y-6">
          <div>
            <h2 className="font-display font-bold text-2xl text-cream mb-1">Create Account</h2>
            <p className="font-body text-text-muted text-sm">Join the 5EDMA community today</p>
          </div>

          <div className="space-y-4">
            <CopticInput
              label="Full Name"
              type="text"
              placeholder="Your full name"
              value={formData.name}
              onChange={(e) => handleChange('name', e.target.value)}
              error={errors.name}
            />

            <CopticInput
              label="Email Address"
              type="email"
              placeholder="you@example.com"
              value={formData.email}
              onChange={(e) => handleChange('email', e.target.value)}
              error={errors.email}
            />

            <CopticInput
              label="Password"
              type="password"
              placeholder="••••••••"
              value={formData.password}
              onChange={(e) => handleChange('password', e.target.value)}
              error={errors.password}
            />

            <CopticInput
              label="Confirm Password"
              type="password"
              placeholder="••••••••"
              value={formData.confirmPassword}
              onChange={(e) => handleChange('confirmPassword', e.target.value)}
              error={errors.confirmPassword}
            />
          </div>

          <label className="flex items-start gap-3 cursor-pointer">
            <input type="checkbox" className="w-4 h-4 mt-1" required />
            <span className="font-body text-text-muted text-sm">
              I agree to the Terms of Service and Privacy Policy
            </span>
          </label>

          <CopticButton variant="primary" onClick={handleRegister} className="w-full">
            Create Account
          </CopticButton>

          <div className="text-center text-sm">
            <span className="font-body text-text-muted">Already have an account? </span>
            <button
              onClick={() => navigate('/login')}
              className="font-body text-gold-primary hover:text-gold-accent transition-colors font-semibold"
            >
              Sign in
            </button>
          </div>
        </GlassCard>

        {/* Footer */}
        <div className="text-center mt-6 text-sm font-body text-text-muted">
          <p>Your community awaits</p>
        </div>
      </div>
    </div>
  );
};

export default Registration;
