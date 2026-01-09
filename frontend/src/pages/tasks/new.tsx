/** Create new task page for Todo application */

'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import Navbar from '../../components/Layout/Navbar';
import TaskForm from '../../components/TaskForm';
import AuthService from '../../services/auth';

const NewTaskPage: React.FC = () => {
  const router = useRouter();

  const handleSave = () => {
    router.push('/dashboard');
  };

  const handleCancel = () => {
    router.push('/dashboard');
  };

  // Get user ID from auth service
  const getUser = () => {
    try {
      // This is a simplified approach - in a real app you'd use a context or better auth management
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/login');
        return null;
      }
      // Decode token to get user ID (simplified)
      // In a real app you'd have better token decoding
      return 'current_user_id'; // This would come from the token or context
    } catch (error) {
      router.push('/login');
      return null;
    }
  };

  // For now, we'll use a placeholder user ID - in a real app this would come from context
  const userId = typeof window !== 'undefined' ? localStorage.getItem('user_id') || 'placeholder_user_id' : 'placeholder_user_id';

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h1 className="text-2xl font-bold text-gray-900 mb-6">Create New Task</h1>

            <TaskForm
              userId={userId}
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