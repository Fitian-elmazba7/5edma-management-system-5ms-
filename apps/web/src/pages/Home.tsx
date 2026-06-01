import React from 'react';
import { useNavigate } from 'react-router-dom';
import { GlassCard, CopticButton } from '../components/coptic';

const Home: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-navy-bg via-navy-deep to-navy-bg">
      {/* Navigation Bar */}
      <nav className="bg-navy-bg/60 backdrop-blur-glass border-b border-gold-primary/20 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gold-primary rounded-sm flex items-center justify-center text-navy-bg font-bold text-lg">
              ⊕
            </div>
            <span className="text-cream font-display font-medium text-sm">5EDMA</span>
          </div>
          <div className="flex gap-4">
            <CopticButton variant="text" onClick={() => navigate('/login')}>
              Login
            </CopticButton>
            <CopticButton variant="primary" onClick={() => navigate('/registration')}>
              Join Community
            </CopticButton>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="py-20 md:py-32 relative overflow-hidden">
        <div className="max-w-6xl mx-auto px-6 flex flex-col items-center text-center gap-8">
          {/* Logo/Icon */}
          <div className="w-24 h-24 bg-gold-primary/20 rounded-2xl flex items-center justify-center border-2 border-gold-primary/40 backdrop-blur-sm">
            <div className="text-6xl text-gold-primary">✡</div>
          </div>

          {/* Headline */}
          <div className="space-y-4 max-w-3xl">
            <h1 className="font-display font-bold text-5xl md:text-6xl text-cream leading-tight">
              Welcome to 5EDMA Community
            </h1>
            <p className="font-body text-xl text-text-muted">
              A modern management system for Coptic Orthodox youth and community engagement
            </p>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 pt-6">
            <CopticButton variant="primary" onClick={() => navigate('/registration')}>
              Start Exploring
            </CopticButton>
            <CopticButton variant="secondary" onClick={() => navigate('/login')}>
              Sign In
            </CopticButton>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 md:py-24 bg-navy-deep/20">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="font-display font-bold text-3xl md:text-4xl text-cream text-center mb-12">
            Key Features
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Feature 1 */}
            <GlassCard variant="default" className="flex flex-col gap-4">
              <div className="w-12 h-12 bg-gold-primary/20 rounded-lg flex items-center justify-center border border-gold-primary/40">
                <span className="text-gold-primary text-xl">👥</span>
              </div>
              <h3 className="font-display font-semibold text-xl text-cream">Member Management</h3>
              <p className="font-body text-text-muted">
                Easily manage community members, track attendance, and organize groups
              </p>
            </GlassCard>

            {/* Feature 2 */}
            <GlassCard variant="default" className="flex flex-col gap-4">
              <div className="w-12 h-12 bg-gold-primary/20 rounded-lg flex items-center justify-center border border-gold-primary/40">
                <span className="text-gold-primary text-xl">📊</span>
              </div>
              <h3 className="font-display font-semibold text-xl text-cream">Analytics & Reports</h3>
              <p className="font-body text-text-muted">
                Comprehensive reporting and analytics for community insights and decisions
              </p>
            </GlassCard>

            {/* Feature 3 */}
            <GlassCard variant="default" className="flex flex-col gap-4">
              <div className="w-12 h-12 bg-gold-primary/20 rounded-lg flex items-center justify-center border border-gold-primary/40">
                <span className="text-gold-primary text-xl">🔐</span>
              </div>
              <h3 className="font-display font-semibold text-xl text-cream">Secure & Private</h3>
              <p className="font-body text-text-muted">
                Enterprise-grade security protecting your community data with role-based access
              </p>
            </GlassCard>

            {/* Feature 4 */}
            <GlassCard variant="default" className="flex flex-col gap-4">
              <div className="w-12 h-12 bg-gold-primary/20 rounded-lg flex items-center justify-center border border-gold-primary/40">
                <span className="text-gold-primary text-xl">📱</span>
              </div>
              <h3 className="font-display font-semibold text-xl text-cream">Mobile Responsive</h3>
              <p className="font-body text-text-muted">
                Access your community information anytime, anywhere on any device
              </p>
            </GlassCard>

            {/* Feature 5 */}
            <GlassCard variant="default" className="flex flex-col gap-4">
              <div className="w-12 h-12 bg-gold-primary/20 rounded-lg flex items-center justify-center border border-gold-primary/40">
                <span className="text-gold-primary text-xl">⚡</span>
              </div>
              <h3 className="font-display font-semibold text-xl text-cream">Fast & Reliable</h3>
              <p className="font-body text-text-muted">
                Built on modern cloud infrastructure for consistent performance and uptime
              </p>
            </GlassCard>

            {/* Feature 6 */}
            <GlassCard variant="default" className="flex flex-col gap-4">
              <div className="w-12 h-12 bg-gold-primary/20 rounded-lg flex items-center justify-center border border-gold-primary/40">
                <span className="text-gold-primary text-xl">🎨</span>
              </div>
              <h3 className="font-display font-semibold text-xl text-cream">Beautiful Design</h3>
              <p className="font-body text-text-muted">
                Inspired by Coptic heritage with modern aesthetics for an elegant experience
              </p>
            </GlassCard>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 md:py-24">
        <div className="max-w-3xl mx-auto px-6 text-center">
          <GlassCard variant="default" className="space-y-6">
            <h2 className="font-display font-bold text-3xl text-cream">
              Ready to Join?
            </h2>
            <p className="font-body text-lg text-text-muted">
              Start managing your community with 5EDMA today. Simple, powerful, and built for faith communities.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
              <CopticButton variant="primary" onClick={() => navigate('/registration')}>
                Create Account
              </CopticButton>
              <CopticButton variant="secondary" onClick={() => navigate('/login')}>
                Sign In
              </CopticButton>
            </div>
          </GlassCard>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gold-primary/20 bg-navy-bg/40 py-8">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <p className="font-body text-text-muted text-sm">
            © 2026 5EDMA Community Management. Built with faith and code.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Home;
