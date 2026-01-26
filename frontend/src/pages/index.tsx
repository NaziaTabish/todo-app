/** Landing page for Todo application */

'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Navbar from '../components/Layout/Navbar';
import AuthService from '../services/auth';

const HomePage: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setIsAuthenticated(AuthService.isAuthenticated());
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <Navbar />

      <main className="relative pt-32 pb-20 overflow-hidden">
        <div className="container mx-auto px-6 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-block mb-6 px-4 py-1.5 rounded-full border border-primary-200 bg-primary-50 text-primary-700 text-sm font-medium animate-fade-in">
              ✨ Simple. Powerful. Secure.
            </div>

            <h1 className="text-5xl md:text-7xl font-bold font-display tracking-tight mb-8 text-gray-900 leading-tight animate-slide-up">
              Organize your work,<br />
              <span className="text-primary-600">amplify your life.</span>
            </h1>

            <p className="text-xl text-gray-600 mb-12 max-w-2xl mx-auto leading-relaxed animate-slide-up" style={{ animationDelay: '0.1s' }}>
              The clear choice for staying organized. Manage tasks with a tool that feels as good as it looks.
            </p>

            <div className="flex flex-col sm:flex-row justify-center gap-6 mb-24 animate-slide-up" style={{ animationDelay: '0.2s' }}>
              {!isAuthenticated ? (
                <>
                  <Link
                    href="/register"
                    className="px-8 py-4 bg-primary-600 hover:bg-primary-700 text-white rounded-2xl font-bold text-lg shadow-xl shadow-primary-600/20 hover:-translate-y-1 transition-all duration-300"
                  >
                    Start for Free
                  </Link>
                  <Link
                    href="/login"
                    className="px-8 py-4 bg-white hover:bg-gray-50 border border-gray-200 text-gray-700 rounded-2xl font-bold text-lg hover:-translate-y-1 transition-all duration-300 shadow-sm"
                  >
                    Welcome Back
                  </Link>
                </>
              ) : (
                <Link
                  href="/dashboard"
                  className="px-8 py-4 bg-primary-600 hover:bg-primary-700 text-white rounded-2xl font-bold text-lg shadow-xl shadow-primary-600/20 hover:-translate-y-1 transition-all duration-300"
                >
                  Go to Dashboard
                </Link>
              )}
            </div>

            {/* Feature Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-left animate-slide-up" style={{ animationDelay: '0.3s' }}>
              <FeatureCard
                icon="⚡"
                title="Instant Sync"
                description="Your tasks stay updated across all your devices in real-time."
              />
              <FeatureCard
                icon="🎨"
                title="Clean Design"
                description="A distraction-free interface that puts your content first."
              />
              <FeatureCard
                icon="🛡️"
                title="Serious Security"
                description="Enterprise-grade encryption keeps your personal data private."
              />
            </div>
          </div>
        </div>
      </main>

      <footer className="border-t border-gray-200 mt-12 bg-white">
        <div className="container mx-auto px-6 py-12 text-center text-gray-500">
          <p>© {new Date().getFullYear()} Todo App. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

const FeatureCard = ({ icon, title, description }: { icon: string, title: string, description: string }) => (
  <div className="p-8 rounded-3xl bg-white border border-gray-100 shadow-lg shadow-gray-200/50 hover:shadow-xl transition-shadow duration-300">
    <div className="text-4xl mb-4">{icon}</div>
    <h3 className="text-xl font-bold text-gray-900 mb-2 font-display">{title}</h3>
    <p className="text-gray-600 leading-relaxed">{description}</p>
  </div>
);

export default HomePage;