// frontend/src/hooks/useChat.js
import { useState, useCallback } from 'react';
import apiService from '../services/api';

export default function useChat() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId] = useState(() => `session_${Date.now()}`);

  const sendMessage = useCallback(async (messageText) => {
    if (!messageText.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: messageText,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setLoading(true);
    setError(null);

    try {
      // Call API
      const response = await apiService.chat(messageText, sessionId, true);

      // Add AI response
      const aiMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.solution || response.message,
        timestamp: new Date().toLocaleTimeString(),
        metadata: response.metadata,
        blocked: response.blocked
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      console.error('Chat error:', err);
      setError(err.message || 'Failed to send message');

      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: '❌ Error: Could not generate solution. Please check if the backend is running on http://localhost:8000',
        timestamp: new Date().toLocaleTimeString(),
        blocked: false
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  }, [sessionId]);

  const submitFeedback = useCallback(async (message, feedbackData) => {
    try {
      // Find the user message that corresponds to this AI message
      const messageIndex = messages.findIndex(m => m.id === message.id);
      const userMessage = messages[messageIndex - 1];

      if (!userMessage) {
        console.error('Could not find corresponding user message');
        return false;
      }

      await apiService.submitFeedback({
        query: userMessage.content,
        solution: message.content,
        rating: feedbackData.rating,
        comment: feedbackData.comment,
        improved_solution: feedbackData.improved_solution
      });

      return true;
    } catch (err) {
      console.error('Feedback error:', err);
      setError(err.message || 'Failed to submit feedback');
      return false;
    }
  }, [messages]);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return {
    messages,
    loading,
    error,
    sendMessage,
    clearMessages,
    submitFeedback
  };
}