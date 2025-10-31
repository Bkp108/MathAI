// frontend/src/components/AnalyticsView.jsx
import React, { useEffect, useState } from 'react';
import apiService from '../services/api';

export default function AnalyticsView({ messages }) {
  const [stats, setStats] = useState({
    total_feedback: 0,
    average_rating: 0,
    rating_distribution: {}
  });

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const data = await apiService.getFeedbackStats();
      setStats(data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  const totalQueries = messages.filter(m => m.role === 'user').length;

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h2 className="text-2xl font-semibold text-gray-100 mb-6">
        📊 Performance Analytics
      </h2>
      
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <div className="text-gray-400 text-sm mb-2">Total Queries</div>
          <div className="text-3xl font-bold text-gray-100">
            {totalQueries}
          </div>
        </div>
        
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <div className="text-gray-400 text-sm mb-2">Average Rating</div>
          <div className="text-3xl font-bold text-gray-100">
            {stats.average_rating.toFixed(1)}/5.0
          </div>
        </div>
        
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <div className="text-gray-400 text-sm mb-2">Total Feedback</div>
          <div className="text-3xl font-bold text-gray-100">
            {stats.total_feedback}
          </div>
        </div>
      </div>

      {/* Rating Distribution */}
      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
        <h3 className="text-lg font-semibold text-gray-100 mb-4">
          Rating Distribution
        </h3>
        <div className="space-y-3">
          {[5, 4, 3, 2, 1].map(star => {
            const count = stats.rating_distribution[star] || 0;
            const percentage = stats.total_feedback > 0 
              ? (count / stats.total_feedback) * 100 
              : 0;
            
            return (
              <div key={star} className="flex items-center gap-3">
                <span className="text-gray-400 w-8">{star}★</span>
                <div className="flex-1 bg-gray-700 rounded-full h-3">
                  <div 
                    className="bg-blue-500 h-3 rounded-full transition-all" 
                    style={{ width: `${percentage}%` }}
                  />
                </div>
                <span className="text-gray-400 text-sm w-12">
                  {count}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}