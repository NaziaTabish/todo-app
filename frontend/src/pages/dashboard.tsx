/** Dashboard page for Todo application */

'use client';

import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Navbar from '../components/Layout/Navbar';
import TaskList from '../components/TaskList';
import { useUser } from '../context/UserContext';

const DashboardPage: React.FC = () => {
  const router = useRouter();
  const { user, loading, isAuthenticated, checkAuthStatus } = useUser();

  React.useEffect(() => {
    let mounted = true;

    const verifyAuth = async () => {
      // If we already have a user, we are authenticated
      if (user) return;

      const isAuth = await checkAuthStatus();
      if (mounted && !isAuth) {
        router.push('/login');
      }
    };

    if (!loading) {
      verifyAuth();
    }

    return () => {
      mounted = false;
    };
  }, [router, checkAuthStatus, user, loading]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return null; // Redirect is happening in effect
  }

  return (
    <div className="min-h-screen text-gray-800 pb-20">
      <Navbar />

      <main className="container mx-auto px-4 pt-24 md:pt-32">
        <div className="max-w-5xl mx-auto space-y-8">

          {/* Welcome Section */}
          <div className="glass rounded-3xl p-8 md:p-10 shadow-lg animate-fade-in relative overflow-hidden">
            <div className="absolute top-0 right-0 -mt-20 -mr-20 w-64 h-64 bg-primary-500/10 rounded-full blur-3xl pointer-events-none"></div>

            <div className="relative z-10">
              <h1 className="text-4xl md:text-5xl font-bold font-display mb-3 bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
                Hello, {user.first_name || user.username}!
              </h1>
              <p className="text-lg text-gray-600 max-w-xl">
                You've got this! Manage your tasks efficiently and keep track of your progress.
              </p>
            </div>
          </div>

          {/* Tasks Section */}
          <div className="glass rounded-3xl shadow-lg p-6 md:p-8 animate-slide-up" style={{ animationDelay: '0.1s' }}>
            <div className="flex flex-col sm:flex-row justify-between items-center mb-8 gap-4">
              <div className="flex items-center gap-3">
                <div className="bg-primary-100 p-2 rounded-xl text-primary-600">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                  </svg>
                </div>
                <h2 className="text-2xl font-bold font-display text-gray-900">Your Tasks</h2>
              </div>

              <Link
                href="/tasks/new"
                className="group flex items-center gap-2 bg-primary-600 hover:bg-primary-700 text-white font-medium py-2.5 px-5 rounded-xl transition-all shadow-md shadow-primary-600/20 hover:shadow-lg hover:shadow-primary-600/30 hover:-translate-y-0.5"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 transition-transform group-hover:rotate-90" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Add New Task
              </Link>
            </div>

            <TaskList userId={user.id} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;