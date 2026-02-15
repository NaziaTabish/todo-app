import apiClient from './api';

export interface ChatResponse {
  message: string;
  tool_used: string | null;
  task_affected: any;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  tool_calls?: Array<{ name: string }>;
}

export interface ChatHistoryResponse {
  messages: ChatMessage[];
  session_created: string;
  last_activity: string;
}

class ChatService {
  /**
   * Send a chat message to the AI agent.
   * @param message User's natural language message
   * @returns Agent's response with optional task information
   */
  async sendMessage(message: string): Promise<ChatResponse> {
    try {
      const response = await apiClient.post('/v1/chat', {
        message: message
      });

      const data = response.data;

      return {
        message: data.message,
        tool_used: data.tool_used,
        task_affected: data.task_affected
      };
    } catch (error: any) {
      if (error.response?.status === 404) {
        return {
          message: "The AI Chat feature is not enabled on this server (404: Endpoint not found).",
          tool_used: null,
          task_affected: null
        };
      }
      throw error;
    }
  }

  /**
   * Get chat history for the current session.
   */
  async getHistory(): Promise<ChatHistoryResponse> {
    try {
      const response = await apiClient.get<ChatHistoryResponse>('/v1/chat/history');
      return response.data;
    } catch (error: any) {
      if (error.response?.status === 404) {
        return {
          messages: [],
          session_created: new Date().toISOString(),
          last_activity: new Date().toISOString()
        };
      }
      throw error;
    }
  }

  /**
   * Clear chat history for the current session.
   */
  async clearHistory(): Promise<{ message: string }> {
    try {
      const response = await apiClient.delete('/v1/chat/history');
      return response.data;
    } catch (error: any) {
      if (error.response?.status === 404) {
        return { message: "Chat history not available" };
      }
      throw error;
    }
  }
}

export const chatService = new ChatService();
