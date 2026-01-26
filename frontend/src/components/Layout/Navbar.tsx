/** Navigation bar component for Todo application */

'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useUser } from '../../context/UserContext';

const Navbar: React.FC = () => {
  const pathname = usePathname();
  const router = useRouter();
  const { user, loading, isAuthenticated, logout } = useUser();

  const handleLogout = async () => {
    try {
      await logout();
      router.push('/login');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const navClasses = "fixed top-0 left-0 right-0 z-50 bg-white shadow-sm border-b border-gray-100 py-4";

  const linkClasses = (isActive: boolean) =>
    `text-sm font-semibold transition-colors duration-200 ${isActive ? 'text-primary-600' : 'text-gray-600 hover:text-primary-600'
    }`;

  if (loading) return null;

  return (
    <nav className={navClasses}>
      <div className="container mx-auto px-6">
        <div className="flex justify-between items-center">
          <div className="text-2xl font-bold font-display tracking-tight text-gray-900">
            <Link href="/" className="flex items-center gap-2">
              <span className="bg-gradient-to-tr from-primary-600 to-indigo-500 text-transparent bg-clip-text">
                Todo
              </span>
              <span>App</span>
            </Link>
          </div>

          <div className="flex items-center space-x-8">
            {!isAuthenticated ? (
              <>
                <Link href="/login" className={linkClasses(pathname === '/login')}>
                  Sign In
                </Link>
                <Link
                  href="/register"
                  className="px-6 py-2.5 rounded-full text-sm font-bold bg-primary-600 text-white hover:bg-primary-700 shadow-md hover:shadow-lg transition-all transform hover:-translate-y-0.5"
                >
                  Get Started
                </Link>
              </>
            ) : (
              <>
                <Link href="/dashboard" className={linkClasses(pathname === '/dashboard')}>
                  Dashboard
                </Link>
                <div className="flex items-center gap-4 pl-6 border-l border-gray-200">
                  <span className="text-sm font-medium hidden md:inline text-gray-700">
                    {user?.first_name || user?.username}
                  </span>
                  <button
                    onClick={handleLogout}
                    className="text-sm font-medium hover:underline text-gray-500 hover:text-red-500"
                  >
                    Logout
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;