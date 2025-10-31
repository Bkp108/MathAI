// frontend/src/components/ChatWindow.jsx
import React, { useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';

export default function ChatWindow({ messages, loading, onMessageAction }) {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const exampleQuestions = [
    "Solve for x: 2x + 5 = 13",
    "Find the derivative of x²",
    "Calculate area of circle r=5",
    "What is the Pythagorean theorem?"
  ];

  return (
    <div className="flex-1 overflow-y-auto">
      {messages.length === 0 ? (
        /* Empty State */
        <div className="h-full flex flex-col items-center justify-center px-4">
          <h2 className="text-4xl font-semibold mb-8 text-center">
            What can I help with?
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-2xl">
            {exampleQuestions.map((example, idx) => (
              <button
                key={idx}
                onClick={() => {
                  // This will be handled by parent component
                  const event = new CustomEvent('exampleClick', { 
                    detail: example 
                  });
                  window.dispatchEvent(event);
                }}
                className="p-4 bg-gray-800 hover:bg-gray-750 rounded-xl text-left transition-colors border border-gray-700"
              >
                <div className="text-sm text-gray-300">{example}</div>
              </button>
            ))}
          </div>
        </div>
      ) : (
        /* Messages */
        <div className="max-w-3xl mx-auto px-4 py-6 space-y-6">
          {messages.map((message) => (
            <MessageBubble 
              key={message.id} 
              message={message}
              onAction={onMessageAction}
            />
          ))}
          
          {/* Loading Indicator */}
          {loading && (
            <div className="mr-auto bg-gray-800 rounded-2xl px-4 py-3">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0s'}}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      )}
    </div>
  );
}