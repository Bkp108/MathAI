// frontend/src/components/MessageBubble.jsx - FIXED VERSION
import React from 'react';
import { Copy, ThumbsUp, ThumbsDown, MoreHorizontal } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';

export default function MessageBubble({ message, onAction }) {
  const isUser = message.role === 'user';
  
  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    console.log('✅ Copied to clipboard');
  };

  const handleLike = () => {
    console.log('👍 Like clicked for message:', message.id);
    onAction(message, 'like');
  };

  const handleDislike = () => {
    console.log('👎 Dislike clicked for message:', message.id);
    onAction(message, 'dislike');
  };

  const handleFeedback = () => {
    console.log('💬 Feedback clicked for message:', message.id);
    onAction(message, 'feedback');
  };

  return (
    <div className={`${isUser ? 'ml-auto max-w-xl' : 'mr-auto'}`}>
      {/* Message Content */}
      <div className={`${
        isUser 
          ? 'bg-blue-600 text-white' 
          : 'bg-gray-800 text-gray-100'
      } rounded-2xl px-4 py-3`}>
        {isUser ? (
          <div className="text-sm whitespace-pre-wrap">{message.content}</div>
        ) : (
          <div className="text-sm prose prose-invert prose-sm max-w-none">
            <ReactMarkdown
              remarkPlugins={[remarkGfm, remarkMath]}
              rehypePlugins={[rehypeKatex]}
              components={{
                // Custom styling for markdown elements
                p: ({node, ...props}) => <p className="mb-2 last:mb-0" {...props} />,
                ul: ({node, ...props}) => <ul className="list-disc pl-4 mb-2" {...props} />,
                ol: ({node, ...props}) => <ol className="list-decimal pl-4 mb-2" {...props} />,
                li: ({node, ...props}) => <li className="mb-1" {...props} />,
                code: ({node, inline, ...props}) => 
                  inline ? (
                    <code className="bg-gray-700 px-1 py-0.5 rounded text-blue-300" {...props} />
                  ) : (
                    <code className="block bg-gray-700 p-2 rounded my-2" {...props} />
                  ),
                h3: ({node, ...props}) => <h3 className="text-base font-semibold mt-2 mb-1" {...props} />,
                strong: ({node, ...props}) => <strong className="font-semibold text-blue-300" {...props} />,
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        )}
        
        {message.metadata && (
          <div className="mt-2 pt-2 border-t border-gray-700 text-xs opacity-70">
            <div>Source: {message.metadata.source}</div>
            {message.metadata.confidence !== undefined && (
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
            onClick={handleLike}
            className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
            title="Like this response"
          >
            <ThumbsUp size={16} className="text-gray-400 hover:text-green-400" />
          </button>
          
          <button 
            onClick={handleDislike}
            className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
            title="Dislike this response"
          >
            <ThumbsDown size={16} className="text-gray-400 hover:text-red-400" />
          </button>
          
          <button 
            onClick={handleFeedback}
            className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
            title="Provide detailed feedback"
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