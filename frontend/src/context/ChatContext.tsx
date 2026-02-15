/**
 * Chat context provider for managing chat state across components.
 * Phase III: AI-Powered Todo Chatbot
 */

'use client';

import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  toolUsed?: string;
  taskAffected?: {
    id: number;
    title: string;
    completed: boolean;
  };
}

interface ChatContextType {
  messages: ChatMessage[];
  isLoading: boolean;
  isOpen: boolean;
  addMessage: (message: Omit<ChatMessage, 'id' | 'timestamp'>) => void;
  sendMessage: (content: string) => Promise<void>;
  clearMessages: () => void;
  toggleChat: () => void;
  setIsOpen: (open: boolean) => void;
  lastTaskUpdate: number;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export function ChatProvider({ children }: { children: ReactNode }) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [lastTaskUpdate, setLastTaskUpdate] = useState(0);

  // Load history on mount
  React.useEffect(() => {
    const loadHistory = async () => {
      try {
        const { chatService } = await import('../services/chat');
        const history = await chatService.getHistory();

        if (history && history.messages) {
          const mappedMessages: ChatMessage[] = history.messages.map((msg: any) => ({
            id: msg.id,
            role: msg.role,
            content: msg.content,
            timestamp: new Date(msg.timestamp),
            toolUsed: msg.tool_calls && msg.tool_calls.length > 0 ? msg.tool_calls[0].name : undefined,
          }));
          setMessages(mappedMessages);
        }
      } catch (error: any) {
        // Silently fail if no history or error (e.g. 404 new session or endpoint missing)
        // If the backend doesn't support chat (404), we just don't show history
        console.log('Chat history not available:', error.response?.status || error.message);
      }
    };

    loadHistory();
  }, []);

  const addMessage = useCallback((message: Omit<ChatMessage, 'id' | 'timestamp'>) => {
    const newMessage: ChatMessage = {
      ...message,
      id: crypto.randomUUID(),
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, newMessage]);
  }, []);

  const sendMessage = useCallback(async (content: string) => {
    // Add user message immediately
    addMessage({ role: 'user', content });
    setIsLoading(true);

    try {
      // Import chat service dynamically to avoid SSR issues
      const { chatService } = await import('../services/chat');
      const response = await chatService.sendMessage(content);

      addMessage({
        role: 'assistant',
        content: response.message,
        toolUsed: response.tool_used || undefined,
        taskAffected: response.task_affected || undefined,
      });

      // Trigger task update if a task was modified
      if (response.task_affected) {
        setLastTaskUpdate(prev => prev + 1);
      }
    } catch (error: any) {
      console.error('Chat error:', error);

      let errorMessage = "I'm having trouble right now. Please try again in a moment.";

      // Check if it's a 404 (Backend doesn't support chat)
      if (error.response?.status === 404) {
        errorMessage = "The AI Chat feature is not enabled on this server (404: Endpoint not found).";
      }

      addMessage({
        role: 'assistant',
        content: errorMessage,
      });
    } finally {
      setIsLoading(false);
    }
  }, [addMessage]);

  const clearMessages = useCallback(async () => {
    try {
      const { chatService } = await import('../services/chat');
      await chatService.clearHistory();
      setMessages([]);
    } catch (error) {
      console.error('Failed to clear history:', error);
    }
  }, []);

  const toggleChat = useCallback(() => {
    setIsOpen(prev => !prev);
  }, []);

  return (
    <ChatContext.Provider
      value={{
        messages,
        isLoading,
        isOpen,
        addMessage,
        sendMessage,
        clearMessages,
        toggleChat,
        setIsOpen,
        lastTaskUpdate,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
}
