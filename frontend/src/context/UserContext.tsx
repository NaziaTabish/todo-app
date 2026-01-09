/** User context for managing authentication state in Todo application */

'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User } from '../types/User';
import AuthService from '../services/auth';

interface UserContextType {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (userData: any) => Promise<void>;
  checkAuthStatus: () => Promise<boolean>;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkInitialAuthStatus();
  }, []);

  const checkInitialAuthStatus = async () => {
    if (AuthService.isAuthenticated()) {
      try {
        const userData = await AuthService.getCurrentUser();
        setUser(userData);
      } catch (error) {
        console.error('Failed to get current user:', error);
        // If token is invalid, log out the user
        AuthService.logout();
      }
    }
    setLoading(false);
  };

  const checkAuthStatus = async (): Promise<boolean> => {
    if (!AuthService.isAuthenticated()) {
      return false;
    }

    try {
      const userData = await AuthService.getCurrentUser();
      setUser(userData);
      return true;
    } catch (error) {
      console.error('Failed to verify auth status:', error);
      logout();
      return false;
    }
  };

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      const response = await AuthService.login({ email, password });
      setUser(response.user);
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    setLoading(true);
    try {
      await AuthService.logout();
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData: any) => {
    setLoading(true);
    try {
      const response = await AuthService.register(userData);
      setUser(response.user);
    } finally {
      setLoading(false);
    }
  };

  const value: UserContextType = {
    user,
    loading,
    isAuthenticated: !!user,
    login,
    logout,
    register,
    checkAuthStatus
  };

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = (): UserContextType => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};