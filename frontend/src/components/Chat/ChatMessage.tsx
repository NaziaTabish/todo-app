/**
 * Chat message component for displaying individual messages.
 * Phase III: AI-Powered Todo Chatbot
 * 
 * Features premium styling with gradient user messages and glass effect for assistant.
 */

import React from 'react';

interface ChatMessageProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
  toolUsed?: string;
}

const ChatMessage: React.FC<ChatMessageProps> = ({
  role,
  content,
  timestamp,
  toolUsed,
}) => {
  const isUser = role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 animate-fade-in`}>
      <div
        className={`max-w-[85%] rounded-2xl px-4 py-3 shadow-md ${isUser
            ? 'bg-gradient-to-br from-primary-500 to-primary-700 text-white rounded-br-md'
            : 'bg-white border border-gray-100 text-gray-800 rounded-bl-md'
          }`}
      >
        <p className={`text-sm leading-relaxed whitespace-pre-wrap ${isUser ? 'text-white' : 'text-gray-700'}`}>
          {content}
        </p>

        {toolUsed && (
          <div className={`mt-2 pt-2 border-t ${isUser ? 'border-white/20' : 'border-gray-100'}`}>
            <span className={`inline-flex items-center gap-1.5 text-xs font-medium ${isUser ? 'text-primary-100' : 'text-primary-600'
              }`}>
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              {toolUsed.replace('_', ' ')}
            </span>
          </div>
        )}

        {timestamp && (
          <div className={`mt-1.5 text-xs ${isUser ? 'text-primary-200' : 'text-gray-400'}`}>
            {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;

