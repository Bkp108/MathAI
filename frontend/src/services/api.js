/**
 * API Service for MathAI
 */
import axios from 'axios';

// Use environment variable or fallback to localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

console.log('🔗 API Base URL:', API_BASE_URL); // Debug log

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log('📤 API Request:', config.method.toUpperCase(), config.url); // Debug log
    
    // Add session ID if exists
    try {
      const sessionId = localStorage.getItem('session_id');
      if (sessionId) {
        config.headers['X-Session-ID'] = sessionId;
      }
    } catch (error) {
      console.warn('localStorage not available:', error);
    }
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log('✅ API Response:', response.config.url, response.status); // Debug log
    return response.data;
  },
  (error) => {
    console.error('❌ API Error:', {
      url: error.config?.url,
      status: error.response?.status,
      message: error.message,
      data: error.response?.data
    });
    
    // Return a more user-friendly error
    let message = 'An error occurred';
    
    if (error.code === 'ECONNABORTED') {
      message = 'Request timeout - server is taking too long to respond';
    } else if (error.code === 'ERR_NETWORK') {
      message = 'Network error - cannot connect to server. Is the backend running on http://localhost:8000?';
    } else if (error.response) {
      // Server responded with error
      message = error.response.data?.detail || error.response.data?.message || error.message;
    } else if (error.request) {
      // Request made but no response
      message = 'No response from server - is the backend running?';
    } else {
      message = error.message;
    }
    
    return Promise.reject(new Error(message));
  }
);

export const apiService = {
  // ========== Health ==========
  health: () => api.get('/health'),

  // ========== Chat ==========
  chat: (message, sessionId = null, useFeedbackLearning = true) => {
    console.log('💬 Sending chat message:', { message, sessionId, useFeedbackLearning });
    return api.post('/chat', {
      message,
      session_id: sessionId,
      use_feedback_learning: useFeedbackLearning
    });
  },

  getChatHistory: (sessionId, limit = 50) =>
    api.get('/chat/history', { params: { session_id: sessionId, limit } }),

  // ========== Feedback ==========
  submitFeedback: (data) => api.post('/feedback', data),

  getFeedbackStats: () => api.get('/feedback/stats'),

  getPositiveFeedback: (minRating = 4) =>
    api.get('/feedback/positive', { params: { min_rating: minRating } }),

  // ========== Knowledge Base ==========
  searchKB: (query, topK = 3, scoreThreshold = 0.5) =>
    api.post('/kb/search', {
      query,
      top_k: topK,
      score_threshold: scoreThreshold
    }),

  getKBStats: () => api.get('/kb/stats'),

  // ========== Web Search ==========
  webSearch: (query) => api.post('/web/search', { query }),

  // ========== Analytics ==========
  getAnalytics: (days = 7) =>
    api.get('/analytics', { params: { days } }),

  // ========== Utility ==========
  improveSolution: (query, solution, feedback, improvedSuggestion = null) =>
    api.post('/improve', {
      query,
      solution,
      feedback,
      improved_suggestion: improvedSuggestion
    })
};

export default apiService;