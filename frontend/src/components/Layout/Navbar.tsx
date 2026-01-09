/** Navigation bar component for Todo application */

'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useUser } from '../../context/UserContext';

const Navbar: React.FC = () => {
  const pathname = usePathname();
  const router = useRouter();
  const { user, isAuthenticated, logout } = useUser();

  const handleLogout = async () => {
    try {
      await logout();
      router.push('/login');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  return (
    <nav className="bg-blue-600 text-white shadow-md">
      <div className="container mx-auto px-4 py-3">
        <div className="flex justify-between items-center">
          <div className="text-xl font-bold">
            <Link href="/" className="hover:text-blue-200 transition-colors">
              Todo App
            </Link>
          </div>

          <div className="flex items-center space-x-4">
            {!isAuthenticated ? (
              <>
                <Link href="/login" className="hover:text-blue-200 transition-colors">
                  Login
                </Link>
                <Link href="/register" className="hover:text-blue-200 transition-colors">
                  Register
                </Link>
              </>
            ) : (
              <>
                <Link href="/dashboard" className="hover:text-blue-200 transition-colors">
                  Dashboard
                </Link>
                <span className="hidden md:inline text-sm">
                  Hi, {user?.first_name || user?.username}!
                </span>
                <button
                  onClick={handleLogout}
                  className="hover:text-blue-200 transition-colors"
                >
                  Logout
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;