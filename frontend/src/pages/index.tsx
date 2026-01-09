/** Landing page for Todo application */

'use client';

import React from 'react';
import Link from 'next/link';
import Navbar from '../components/Layout/Navbar';
import AuthService from '../services/auth';

const HomePage: React.FC = () => {
  const isAuthenticated = AuthService.isAuthenticated();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Navbar />

      <main className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Stay Organized, Boost Productivity
          </h1>
          <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
            A simple and elegant todo application that helps you manage your tasks efficiently.
            Secure, intuitive, and designed for productivity.
          </p>

          <div className="flex flex-col sm:flex-row justify-center gap-4 mb-16">
            {!isAuthenticated ? (
              <>
                <Link
                  href="/register"
                  className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg shadow-md transition-colors duration-300 text-lg"
                >
                  Get Started
                </Link>
                <Link
                  href="/login"
                  className="bg-white hover:bg-gray-100 text-blue-600 font-bold py-3 px-8 rounded-lg shadow-md transition-colors duration-300 text-lg border border-blue-600"
                >
                  Sign In
                </Link>
              </>
            ) : (
              <Link
                href="/dashboard"
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg shadow-md transition-colors duration-300 text-lg"
              >
                Go to Dashboard
              </Link>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-blue-600 text-3xl mb-4">✓</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Easy Task Management</h3>
              <p className="text-gray-600">
                Create, update, and manage your tasks with a simple and intuitive interface.
              </p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-blue-600 text-3xl mb-4">🔒</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Secure & Private</h3>
              <p className="text-gray-600">
                Your data is protected with industry-standard security measures.
              </p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-blue-600 text-3xl mb-4">📱</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Always Accessible</h3>
              <p className="text-gray-600">
                Access your tasks from any device, anywhere, anytime.
              </p>
            </div>
          </div>
        </div>
      </main>

      <footer className="bg-gray-800 text-white py-8">
        <div className="container mx-auto px-4 text-center">
          <p>© {new Date().getFullYear()} Todo App. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;