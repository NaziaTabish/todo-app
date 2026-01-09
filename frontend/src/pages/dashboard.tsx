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
    const verifyAuth = async () => {
      const isAuth = await checkAuthStatus();
      if (!isAuth) {
        router.push('/login');
      }
    };

    verifyAuth();
  }, [router, checkAuthStatus]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return null; // Redirect is happening in effect
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Welcome, {user.first_name || user.username}!
            </h1>
            <p className="text-gray-600">
              Manage your tasks and stay productive
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Your Tasks</h2>
              <Link
                href="/tasks/new"
                className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
              >
                Add New Task
              </Link>
            </div>

            <TaskList userId={user.id} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;