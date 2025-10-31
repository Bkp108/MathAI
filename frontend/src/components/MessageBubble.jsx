// frontend/src/components/MessageBubble.jsx
import React from 'react';
import { Copy, ThumbsUp, ThumbsDown, MoreHorizontal } from 'lucide-react';

export default function MessageBubble({ message, onAction }) {
  const isUser = message.role === 'user';
  
  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
  };

  return (
    <div className={`${isUser ? 'ml-auto max-w-xl' : 'mr-auto'}`}>
      {/* Message Content */}
      <div className={`${
        isUser 
          ? 'bg-blue-600 text-white' 
          : 'bg-gray-800 text-gray-100'
      } rounded-2xl px-4 py-3`}>
        <div className="text-sm whitespace-pre-wrap">{message.content}</div>
        
        {message.metadata && (
          <div className="mt-2 pt-2 border-t border-gray-700 text-xs opacity-70">
            <div>Source: {message.metadata.source}</div>
            {message.metadata.confidence && (
              <div>Confidence: {(message.metadata.confidence * 100).toFixed(1)}%</div>
            )}
          </div>
        )}
      </div>

      {/* Action Buttons (AI messages only) */}
      {!isUser && !message.blocked && (
        <div className="flex items-center gap-2 mt-2 ml-2">
          <button 
            onClick={handleCopy}
            className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
            title="Copy"
          >
            <Copy size={16} className="text-gray-400" />
          </button>
          
          <button 
            onClick={() => onAction(message, 'like')}
            className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
            title="Like"
          >
            <ThumbsUp size={16} className="text-gray-400" />
          </button>
          
          <button 
            onClick={() => onAction(message, 'dislike')}
            className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
            title="Dislike"
          >
            <ThumbsDown size={16} className="text-gray-400" />
          </button>
          
          <button 
            onClick={() => onAction(message, 'feedback')}
            className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
            title="Give Feedback"
          >
            <MoreHorizontal size={16} className="text-gray-400" />
          </button>
        </div>
      )}
      
      {/* Timestamp */}
      <div className="text-xs text-gray-500 mt-1 ml-2">
        {message.timestamp}
      </div>
    </div>
  );
}