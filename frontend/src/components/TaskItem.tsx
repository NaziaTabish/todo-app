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

  const priorityConfig = {
    1: { label: 'High', color: 'bg-red-100 text-red-700' },
    2: { label: 'Medium', color: 'bg-orange-100 text-orange-700' },
    3: { label: 'Low', color: 'bg-green-100 text-green-700' },
  };

  return (
    <div className={`group relative p-5 rounded-xl border transition-all duration-200 ${task.completed
        ? 'bg-gray-50 border-gray-200'
        : 'bg-white border-gray-200 shadow-sm hover:shadow-md hover:border-primary-200'
      }`}>
      <div className="flex items-start gap-4">
        {/* Custom Checkbox */}
        <div className="pt-1">
          <label className="relative flex items-center justify-center p-0.5 rounded-full cursor-pointer">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={onToggle}
              className="peer appearance-none w-5 h-5 border-2 border-gray-300 rounded-md checked:bg-primary-600 checked:border-primary-600 transition-colors focus:ring-2 focus:ring-primary-200 focus:outline-none"
            />
            <svg
              className="absolute w-3.5 h-3.5 text-white pointer-events-none opacity-0 peer-checked:opacity-100 transition-opacity duration-200"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth="3"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          </label>
        </div>

        {/* Content */}
        <div className="flex-grow min-w-0">
          <div className="flex flex-wrap items-center justify-between gap-2 mb-1">
            <h3 className={`text-lg font-semibold truncate pr-8 ${task.completed ? 'text-gray-500 line-through Decoration-gray-400' : 'text-gray-900'
              }`}>
              {task.title}
            </h3>

            <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold ${priorityConfig[task.priority as keyof typeof priorityConfig]?.color || 'bg-gray-100 text-gray-600'
              }`}>
              {priorityConfig[task.priority as keyof typeof priorityConfig]?.label}
            </span>
          </div>

          {task.description && (
            <p className={`text-sm text-gray-600 mb-3 ${task.completed ? 'line-through opacity-70' : ''
              }`}>
              {task.description}
            </p>
          )}

          <div className="flex flex-wrap items-center gap-4 text-xs text-gray-500">
            <div className="flex items-center gap-1.5">
              <svg className="w-3.5 h-3.5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span>{formatDate(task.created_at)}</span>
            </div>

            {task.due_date && (
              <div className="flex items-center gap-1.5 text-orange-600 font-medium">
                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>Due: {formatDate(task.due_date)}</span>
              </div>
            )}
          </div>
        </div>

        {/* Delete Button */}
        <button
          onClick={onDelete}
          className="absolute top-4 right-4 p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all"
          aria-label="Delete task"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default TaskItem;