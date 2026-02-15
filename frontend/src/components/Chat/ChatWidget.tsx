/**
 * Chat widget component - floating chat panel.
 * Phase III: AI-Powered Todo Chatbot
 * 
 * Features:
 * - Glassmorphism styling matching the app design
 * - Quick action suggestions for new users
 * - Keyboard shortcuts (Escape to close, Enter to send)
 * - Smooth animations and transitions
 * - Help command support
 */

'use client';

import React, { useRef, useEffect, useState } from 'react';
import { useChat } from '../../context/ChatContext';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';

// Quick action suggestions for empty state
const QUICK_ACTIONS = [
  { label: '➕ Add a task', command: 'add ' },
  { label: '📋 Show tasks', command: 'show my tasks' },
  { label: '✅ Complete task', command: 'done with ' },
  { label: '🗑️ Delete task', command: 'delete ' },
  { label: '❓ Help', command: 'help' },
];

const ChatWidget: React.FC = () => {
  const { messages, isLoading, isOpen, sendMessage, clearMessages, toggleChat } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [inputValue, setInputValue] = useState('');

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle escape key to close chat
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        toggleChat();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, toggleChat]);

  const handleQuickAction = (command: string) => {
    if (command === 'show my tasks' || command === 'help') {
      sendMessage(command);
    } else {
      setInputValue(command);
    }
  };

  const handleSendMessage = (message: string) => {
    // Handle help command locally
    if (message.toLowerCase().trim() === 'help') {
      // Let the agent handle it for a more natural response
      sendMessage('What can you help me with?');
    } else {
      sendMessage(message);
    }
    setInputValue('');
  };

  if (!isOpen) {
    return (
      <button
        onClick={toggleChat}
        className="fixed bottom-6 right-6 w-16 h-16 rounded-full bg-gradient-to-br from-primary-500 to-primary-700 text-white shadow-xl hover:shadow-2xl hover:scale-105 transition-all duration-300 flex items-center justify-center z-50 group"
        aria-label="Open chat assistant"
      >
        <svg className="w-7 h-7 group-hover:scale-110 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
        {/* Pulse animation indicator */}
        <span className="absolute top-0 right-0 w-4 h-4 bg-green-400 rounded-full border-2 border-white animate-pulse" />
      </button>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 w-[400px] h-[550px] glass rounded-3xl shadow-2xl flex flex-col overflow-hidden z-50 border border-white/20 animate-slide-up">
      {/* Gradient Background Glow */}
      <div className="absolute top-0 right-0 -mt-20 -mr-20 w-64 h-64 bg-primary-500/20 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-0 -mb-20 -ml-20 w-48 h-48 bg-primary-400/10 rounded-full blur-3xl pointer-events-none" />

      {/* Header */}
      <div className="relative flex items-center justify-between px-5 py-4 bg-gradient-to-r from-primary-600 to-primary-700 text-white">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-white/20 backdrop-blur-sm flex items-center justify-center shadow-inner">
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <div>
            <h3 className="font-bold text-base font-display">Todo Assistant</h3>
            <p className="text-xs text-primary-200 flex items-center gap-1">
              <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
              Ready to help with your tasks
            </p>
          </div>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={clearMessages}
            className="p-2 hover:bg-white/20 rounded-xl transition-all hover:scale-105"
            title="Clear chat history"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
          <button
            onClick={toggleChat}
            className="p-2 hover:bg-white/20 rounded-xl transition-all hover:scale-105"
            title="Close chat (Esc)"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      {/* Messages Area */}
      <div className="relative flex-1 overflow-y-auto p-4 bg-gradient-to-b from-gray-50/80 to-white/80">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-gray-600 px-4">
            {/* Welcome Icon */}
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-100 to-primary-200 flex items-center justify-center mb-4 shadow-lg">
              <svg className="w-8 h-8 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <h4 className="text-lg font-bold font-display text-gray-800 mb-1">Hi there! 👋</h4>
            <p className="text-sm text-gray-500 text-center mb-6">
              I can help you manage your tasks with natural language. Try one of these:
            </p>

            {/* Quick Actions Grid */}
            <div className="w-full space-y-2">
              {QUICK_ACTIONS.map((action, idx) => (
                <button
                  key={idx}
                  onClick={() => handleQuickAction(action.command)}
                  className="w-full text-left px-4 py-3 rounded-xl bg-white/80 border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-all text-sm font-medium text-gray-700 hover:text-primary-700 shadow-sm hover:shadow-md"
                >
                  {action.label}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg) => (
              <ChatMessage
                key={msg.id}
                role={msg.role}
                content={msg.content}
                timestamp={msg.timestamp}
                toolUsed={msg.toolUsed}
              />
            ))}
            {isLoading && (
              <div className="flex justify-start mb-3 animate-fade-in">
                <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
                  <div className="flex items-center gap-1.5">
                    <div className="w-2.5 h-2.5 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <div className="w-2.5 h-2.5 bg-primary-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <div className="w-2.5 h-2.5 bg-primary-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input Area */}
      <ChatInput
        onSend={handleSendMessage}
        isLoading={isLoading}
        placeholder="Type a message... (Enter to send)"
        value={inputValue}
        onChange={setInputValue}
      />

      {/* Footer hint */}
      <div className="px-4 py-2 text-center text-xs text-gray-400 bg-gray-50/50 border-t border-gray-100">
        Press <kbd className="px-1.5 py-0.5 bg-gray-200 rounded text-gray-600 font-mono">Esc</kbd> to close • Type <span className="font-medium text-primary-500">help</span> for commands
      </div>
    </div>
  );
};

export default ChatWidget;
