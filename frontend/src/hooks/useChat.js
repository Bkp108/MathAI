// frontend/src/hooks/useChat.js - FIXED VERSION
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
      console.log('📤 Sending message:', messageText);
      
      // Call API
      const response = await apiService.chat(messageText, sessionId, true);
      
      console.log('📥 Received response:', response);

      // Check if response has solution
      if (!response.solution && !response.error) {
        throw new Error('No solution received from backend');
      }

      // Add AI response
      const aiMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.solution || response.error || 'No response',
        timestamp: new Date().toLocaleTimeString(),
        metadata: response.metadata,
        blocked: response.blocked,
        query: response.query // Store original query for feedback
      };

      setMessages(prev => [...prev, aiMessage]);
      
    } catch (err) {
      console.error('❌ Chat error:', err);
      setError(err.message || 'Failed to send message');

      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: `❌ Error: ${err.message}\n\nPlease check:\n1. Backend is running on http://localhost:8000\n2. GEMINI_API_KEY is set correctly\n3. Network connection is working`,
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
      console.log('📤 Submitting feedback for message:', message.id);
      
      // Find the user message that corresponds to this AI message
      const messageIndex = messages.findIndex(m => m.id === message.id);
      
      if (messageIndex === -1) {
        console.error('❌ Message not found in history');
        return false;
      }

      // Get the previous message (should be user's query)
      const userMessage = messages[messageIndex - 1];
      
      // Also check if message has stored query
      const query = message.query || (userMessage && userMessage.role === 'user' ? userMessage.content : null);

      if (!query) {
        console.error('❌ Could not find corresponding user message');
        alert('Could not find the original question for this response');
        return false;
      }

      console.log('📝 Feedback data:', {
        query,
        solution: message.content,
        rating: feedbackData.rating
      });

      // Submit feedback
      const response = await apiService.submitFeedback({
        query: query,
        solution: message.content,
        rating: feedbackData.rating,
        comment: feedbackData.comment || null,
        improved_solution: feedbackData.improved_solution || null
      });

      console.log('✅ Feedback submitted:', response);
      return true;
      
    } catch (err) {
      console.error('❌ Feedback error:', err);
      setError(err.message || 'Failed to submit feedback');
      alert(`Failed to submit feedback: ${err.message}`);
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