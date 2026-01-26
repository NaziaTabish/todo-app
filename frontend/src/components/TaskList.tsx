/** Task list component for Todo application */

'use client';

import React, { useState, useEffect } from 'react';
import TaskItem from './TaskItem';
import { Task } from '../types/Task';
import { tasksApi } from '../services/api';

interface TaskListProps {
  userId: string;
}

const TaskList: React.FC<TaskListProps> = ({ userId }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');

  useEffect(() => {
    fetchTasks();
  }, [userId, filter]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await tasksApi.getTasks(userId, { status: filter });
      setTasks(response.data.tasks || response.data);
    } catch (err: any) {
      console.error('Error fetching tasks:', err);
      let errorMessage = 'Failed to load tasks';
      if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.message) {
        errorMessage = err.message;
      }
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskToggle = async (taskId: string) => {
    try {
      await tasksApi.toggleTaskCompletion(userId, taskId);
      // Refresh the task list
      fetchTasks();
    } catch (err: any) {
      console.error('Error toggling task:', err);
      setError('Failed to update task');
    }
  };

  const handleTaskDelete = async (taskId: string) => {
    try {
      await tasksApi.deleteTask(userId, taskId);
      // Refresh the task list
      fetchTasks();
    } catch (err: any) {
      console.error('Error deleting task:', err);
      setError('Failed to delete task');
    }
  };

  const FilterButton = ({ active, onClick, label }: { active: boolean, onClick: () => void, label: string }) => (
    <button
      onClick={onClick}
      className={`px-5 py-2 rounded-full text-sm font-medium transition-all duration-200 ${active
          ? 'bg-primary-600 text-white shadow-md shadow-primary-600/20'
          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
        }`}
    >
      {label}
    </button>
  );

  return (
    <div>
      <div className="flex justify-between items-center mb-6 flex-wrap gap-4">
        <div className="flex space-x-2 bg-gray-50 p-1 rounded-full border border-gray-200">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${filter === 'all' ? 'bg-white text-primary-700 shadow-sm' : 'text-gray-500 hover:text-gray-700'
              }`}
          >
            All
          </button>
          <button
            onClick={() => setFilter('pending')}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${filter === 'pending' ? 'bg-white text-primary-700 shadow-sm' : 'text-gray-500 hover:text-gray-700'
              }`}
          >
            Pending
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${filter === 'completed' ? 'bg-white text-primary-700 shadow-sm' : 'text-gray-500 hover:text-gray-700'
              }`}
          >
            Completed
          </button>
        </div>

        <span className="text-sm text-gray-500 font-medium">
          {tasks.length} {tasks.length === 1 ? 'Task' : 'Tasks'}
        </span>
      </div>

      {loading ? (
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary-600"></div>
        </div>
      ) : error ? (
        <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-xl flex items-center gap-2">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {error}
        </div>
      ) : (
        <div className="space-y-3">
          {tasks.length === 0 ? (
            <div className="text-center py-16 bg-gray-50/50 rounded-2xl border border-dashed border-gray-200">
              <div className="text-4xl mb-4">📝</div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No tasks found</h3>
              <p className="text-gray-500">
                {filter === 'all'
                  ? "Get started by adding a new task!"
                  : `No ${filter} tasks to display.`}
              </p>
            </div>
          ) : (
            tasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onToggle={() => handleTaskToggle(task.id)}
                onDelete={() => handleTaskDelete(task.id)}
              />
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default TaskList;