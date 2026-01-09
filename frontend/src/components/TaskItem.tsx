/** Individual task item component for Todo application */

import React from 'react';
import { Task } from '../types/Task';

interface TaskItemProps {
  task: Task;
  onToggle: () => void;
  onDelete: () => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onToggle, onDelete }) => {
  const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  return (
    <div className={`border rounded-lg p-4 shadow-sm ${
      task.completed
        ? 'bg-green-50 border-green-200'
        : 'bg-white border-gray-200'
    }`}>
      <div className="flex items-start">
        {/* Checkbox */}
        <div className="flex items-center mr-3 mt-1">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={onToggle}
            className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
          />
        </div>

        {/* Task Content */}
        <div className="flex-grow">
          <div className="flex justify-between">
            <h3 className={`text-lg font-medium ${
              task.completed ? 'line-through text-gray-500' : 'text-gray-900'
            }`}>
              {task.title}
            </h3>

            {/* Priority Indicator */}
            <div className={`ml-2 px-2 py-1 rounded text-xs font-medium ${
              task.priority === 1
                ? 'bg-red-100 text-red-800'
                : task.priority === 2
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-green-100 text-green-800'
            }`}>
              {task.priority === 1 ? 'High' : task.priority === 2 ? 'Medium' : 'Low'}
            </div>
          </div>

          {task.description && (
            <p className={`mt-1 text-gray-600 ${
              task.completed ? 'line-through' : ''
            }`}>
              {task.description}
            </p>
          )}

          <div className="mt-2 flex flex-wrap gap-2 text-sm text-gray-500">
            <span>Created: {formatDate(task.created_at)}</span>
            {task.updated_at !== task.created_at && (
              <span>Updated: {formatDate(task.updated_at)}</span>
            )}
            {task.due_date && (
              <span className="text-orange-600 font-medium">
                Due: {formatDate(task.due_date)}
              </span>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex space-x-2 ml-4">
          <button
            onClick={onDelete}
            className="text-red-600 hover:text-red-800 focus:outline-none"
            aria-label="Delete task"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default TaskItem;