/** Authentication utilities for Todo application */

import { User, AuthResponse, LoginCredentials } from '../types/User';
import { tasksApi, authApi } from './api';

class AuthService {
  /**
   * Store the authentication token
   */
  setToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token);
    }
  }

  /**
   * Store user data in localStorage
   */
  setUserData(user: any): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('user_data', JSON.stringify(user));
    }
  }

  /**
   * Get the stored authentication token
   */
  getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('access_token');
    }
    return null;
  }

  /**
   * Remove the authentication token
   */
  removeToken(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return this.getToken() !== null;
  }

  /**
   * Register a new user
   */
  async register(userData: any): Promise<AuthResponse> {
    try {
      const response = await authApi.register(userData);
      const { access_token, user } = response.data;

      // Store the token and user data
      this.setToken(access_token);
      this.setUserData(user);

      return { access_token, token_type: 'bearer', user };
    } catch (error: any) {
      const detail = error.response?.data?.detail;
      let message = 'Registration failed';

      if (typeof detail === 'string') {
        message = detail;
      } else if (Array.isArray(detail)) {
        // Handle standard FastAPI validation errors
        message = detail.map((err: any) => err.msg || JSON.stringify(err)).join(', ');
      } else if (typeof detail === 'object' && detail !== null) {
        message = JSON.stringify(detail);
      } else if (error.message) {
        message = error.message;
      }

      throw new Error(message);
    }
  }

  /**
   * Login user
   */
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      const response = await authApi.login(credentials);
      const { access_token, user } = response.data;

      // Store the token and user data
      this.setToken(access_token);
      this.setUserData(user);

      return { access_token, token_type: 'bearer', user };
    } catch (error: any) {
      const detail = error.response?.data?.detail;
      let message = 'Login failed';

      if (typeof detail === 'string') {
        message = detail;
      } else if (Array.isArray(detail)) {
        // Handle standard FastAPI validation errors
        message = detail.map((err: any) => err.msg || JSON.stringify(err)).join(', ');
      } else if (typeof detail === 'object' && detail !== null) {
        message = JSON.stringify(detail);
      } else if (error.message) {
        message = error.message;
      }

      throw new Error(message);
    }
  }

  /**
   * Logout user
   */
  async logout(): Promise<void> {
    try {
      await authApi.logout();
    } catch (error) {
      // Even if logout API fails, clear local token
      console.error('Logout API call failed:', error);
    } finally {
      this.removeToken();
      if (typeof window !== 'undefined') {
        localStorage.removeItem('user_data');
      }
    }
  }

  /**
   * Get current user info
   */
  async getCurrentUser(): Promise<User> {
    try {
      const response = await authApi.getCurrentUser();
      this.setUserData(response.data);
      return response.data;
    } catch (error) {
      throw new Error('Failed to get user information');
    }
  }

  /**
   * Refresh token if expired
   * Note: For JWT tokens, we typically handle expiration by requiring re-login
   * or using refresh tokens if implemented on the backend
   */
  async refreshToken(): Promise<string | null> {
    if (!this.isAuthenticated()) {
      return null;
    }

    try {
      // In a real implementation, you'd call a refresh token endpoint
      // For now, we'll just return the current token if it exists
      return this.getToken();
    } catch (error) {
      // If refresh fails, user needs to re-login
      this.removeToken();
      throw error;
    }
  }
}

export default new AuthService();