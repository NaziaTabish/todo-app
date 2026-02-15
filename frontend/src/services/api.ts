/** API client configuration for Todo application */

import axios, { AxiosInstance } from 'axios';

// Base API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers!.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear auth token and redirect to login
      localStorage.removeItem('access_token');
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;

// Export specific API functions
export const authApi = {
  register: (userData: any) => apiClient.post('/auth/register', userData),
  login: (credentials: any) => apiClient.post('/auth/login', credentials),
  logout: () => apiClient.post('/auth/logout'),
  getCurrentUser: () => apiClient.get('/auth/me'),
};

export const tasksApi = {
  getTasks: (userId: string, params?: any) =>
    apiClient.get(`/users/${userId}/tasks`, { params }),

  createTask: (userId: string, taskData: any) =>
    apiClient.post(`/users/${userId}/tasks`, taskData),

  getTask: (userId: string, taskId: string) =>
    apiClient.get(`/users/${userId}/tasks/${taskId}`),

  updateTask: (userId: string, taskId: string, taskData: any) =>
    apiClient.put(`/users/${userId}/tasks/${taskId}`, taskData),

  deleteTask: (userId: string, taskId: string) =>
    apiClient.delete(`/users/${userId}/tasks/${taskId}`),

  toggleTaskCompletion: (userId: string, taskId: string) =>
    apiClient.patch(`/users/${userId}/tasks/${taskId}/complete`),
};
