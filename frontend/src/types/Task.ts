/** Task type definitions for Todo application */

export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
  user_id: string;
  due_date?: string;
  priority: number; // 1=highest, 3=lowest
}

export interface TaskCreate {
  title: string;
  description?: string;
  user_id: string;
  due_date?: string;
  priority?: number;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
  due_date?: string;
  priority?: number;
}

export interface TaskFilterOptions {
  status: 'all' | 'pending' | 'completed';
  limit?: number;
  offset?: number;
}