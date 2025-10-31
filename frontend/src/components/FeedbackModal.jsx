import React, { useState } from 'react';
import { X } from 'lucide-react';

export default function FeedbackModal({ isOpen, onClose, onSubmit, message }) {
  const [rating, setRating] = useState(3);
  const [comment, setComment] = useState('');
  const [improvedSolution, setImprovedSolution] = useState('');

  const handleSubmit = () => {
    onSubmit({
      rating,
      comment: comment || null,
      improved_solution: improvedSolution || null
    });
    
    // Reset form
    setRating(3);
    setComment('');
    setImprovedSolution('');
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-gray-900 rounded-xl p-6 w-full max-w-lg border border-gray-800">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-semibold">💬 Provide Feedback</h3>
          <button 
            onClick={onClose} 
            className="p-1 hover:bg-gray-800 rounded"
          >
            <X size={20} />
          </button>
        </div>

        {/* Form */}
        <div className="space-y-4">
          {/* Rating */}
          <div>
            <label className="block text-sm text-gray-400 mb-2">
              Rate this solution (1-5)
            </label>
            <input 
              type="range" 
              min="1" 
              max="5" 
              value={rating}
              onChange={(e) => setRating(parseInt(e.target.value))}
              className="w-full" 
            />
            <div className="text-center text-2xl mt-2">
              {'⭐'.repeat(rating)}
            </div>
          </div>

          {/* Comment */}
          <div>
            <label className="block text-sm text-gray-400 mb-2">
              Comments (optional)
            </label>
            <textarea 
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              className="w-full bg-gray-800 rounded-lg px-3 py-2 border border-gray-700 outline-none focus:border-gray-600"
              rows={3}
              placeholder="Share your thoughts..."
            />
          </div>

          {/* Improved Solution */}
          <div>
            <label className="block text-sm text-gray-400 mb-2">
              Improved solution (optional)
            </label>
            <textarea 
              value={improvedSolution}
              onChange={(e) => setImprovedSolution(e.target.value)}
              className="w-full bg-gray-800 rounded-lg px-3 py-2 border border-gray-700 outline-none focus:border-gray-600"
              rows={4}
              placeholder="Suggest a better solution..."
            />
          </div>

          {/* Submit Button */}
          <button 
            onClick={handleSubmit}
            className="w-full bg-blue-600 hover:bg-blue-700 py-2 rounded-lg font-medium transition-colors"
          >
            📤 Submit Feedback
          </button>
        </div>
      </div>
    </div>
  );
}