/** Authentication utilities for Todo application */

import { User, AuthResponse, LoginCredentials } from '../types/User';
import { tasksApi, authApi } from './api';

class AuthService {
  /**
   * Store the authentication token
   */
  setToken(token: string): void {
    localStorage.setItem('access_token', token);
  }

  /**
   * Get the stored authentication token
   */
  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  /**
   * Remove the authentication token
   */
  removeToken(): void {
    localStorage.removeItem('access_token');
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

      // Store the token
      this.setToken(access_token);

      return { access_token, token_type: 'bearer', user };
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Registration failed');
    }
  }

  /**
   * Login user
   */
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      const response = await authApi.login(credentials);
      const { access_token, user } = response.data;

      // Store the token
      this.setToken(access_token);

      return { access_token, token_type: 'bearer', user };
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Login failed');
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
    }
  }

  /**
   * Get current user info
   */
  async getCurrentUser(): Promise<User> {
    try {
      const response = await authApi.getCurrentUser();
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