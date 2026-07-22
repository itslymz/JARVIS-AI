import { useState, useCallback } from 'react';
import axios from 'axios';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = useCallback(
    async (content: string) => {
      setIsLoading(true);
      
      try {
        // Add user message
        const userMessage: Message = {
          role: 'user',
          content,
          timestamp: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, userMessage]);

        // Send to backend
        const response = await axios.post(
          `${process.env.NEXT_PUBLIC_API_URL}/api/v1/chat/message`,
          { content, conversation_id: null }
        );

        // Add assistant response
        const assistantMessage: Message = {
          role: 'assistant',
          content: response.data.content,
          timestamp: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } catch (error) {
        console.error('Failed to send message:', error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  return { messages, isLoading, sendMessage };
}
