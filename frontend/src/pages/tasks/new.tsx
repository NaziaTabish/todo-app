/** Create new task page for Todo application */

'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import Navbar from '../../components/Layout/Navbar';
import TaskForm from '../../components/TaskForm';
import { useUser } from '../../context/UserContext';

const NewTaskPage: React.FC = () => {
  const router = useRouter();
  const { user, isAuthenticated, loading } = useUser();

  React.useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/login');
    }
  }, [loading, isAuthenticated, router]);

  const handleSave = () => {
    router.push('/dashboard');
  };

  const handleCancel = () => {
    router.push('/dashboard');
  };

  if (loading || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pb-20">
      <Navbar />

      <div className="container mx-auto px-4 pt-24 md:pt-32">
        <div className="max-w-2xl mx-auto">
          <div className="glass rounded-3xl p-8 md:p-10 shadow-lg animate-fade-in relative">

            <div className="flex items-center gap-4 mb-8">
              <button
                onClick={handleCancel}
                className="p-2 rounded-xl hover:bg-black/5 transition-colors"
                aria-label="Go back"
              >
                <svg className="w-6 h-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
              </button>
              <h1 className="text-3xl font-bold font-display text-gray-900">Create New Task</h1>
            </div>

            <TaskForm
              userId={user.id}
              onSave={handleSave}
              onCancel={handleCancel}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default NewTaskPage;