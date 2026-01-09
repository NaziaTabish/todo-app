/** Task list component for Todo application */

'use client';

import React, { useState, useEffect } from 'react';
import TaskItem from './TaskItem';
import { Task, TaskFilterOptions } from '../types/Task';
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
      let errorMessage = 'Failed to update task';
      if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.message) {
        errorMessage = err.message;
      }
      setError(errorMessage);
    }
  };

  const handleTaskDelete = async (taskId: string) => {
    try {
      await tasksApi.deleteTask(userId, taskId);
      // Refresh the task list
      fetchTasks();
    } catch (err: any) {
      console.error('Error deleting task:', err);
      let errorMessage = 'Failed to delete task';
      if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.message) {
        errorMessage = err.message;
      }
      setError(errorMessage);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        {error}
      </div>
    );
  }

  return (
    <div>
      {/* Filter Controls */}
      <div className="flex space-x-4 mb-6">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-md ${
            filter === 'all'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          All Tasks
        </button>
        <button
          onClick={() => setFilter('pending')}
          className={`px-4 py-2 rounded-md ${
            filter === 'pending'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Pending
        </button>
        <button
          onClick={() => setFilter('completed')}
          className={`px-4 py-2 rounded-md ${
            filter === 'completed'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Completed
        </button>
      </div>

      {/* Task List */}
      <div className="space-y-4">
        {tasks.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-500">No tasks found. Add a new task to get started!</p>
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
    </div>
  );
};

export default TaskList;