// frontend/src/components/InputArea.jsx
import React, { useState } from 'react';
import { Send, Mic, Plus } from 'lucide-react';

export default function InputArea({ onSend, loading, disabled }) {
  const [inputValue, setInputValue] = useState('');

  const handleSend = () => {
    if (inputValue.trim() && !loading) {
      onSend(inputValue);
      setInputValue('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-gray-800 p-4">
      <div className="max-w-3xl mx-auto">
        <div className="bg-gray-800 rounded-2xl border border-gray-700 focus-within:border-gray-600 transition-colors">
          <div className="flex items-end gap-2 p-2">
            <button 
              className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
              title="Attach file"
            >
              <Plus size={20} className="text-gray-400" />
            </button>
            
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask any math question..."
              className="flex-1 bg-transparent outline-none resize-none text-gray-100 placeholder-gray-500 px-2 py-2 max-h-32"
              rows={1}
              disabled={disabled || loading}
            />
            
            <button 
              className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
              title="Voice input"
            >
              <Mic size={20} className="text-gray-400" />
            </button>
            
            <button 
              onClick={handleSend}
              disabled={!inputValue.trim() || loading || disabled}
              className={`p-2 rounded-lg transition-colors ${
                inputValue.trim() && !loading && !disabled
                  ? 'bg-blue-600 hover:bg-blue-700' 
                  : 'bg-gray-700'
              }`}
            >
              <Send size={20} className={
                inputValue.trim() && !loading && !disabled
                  ? 'text-white' 
                  : 'text-gray-500'
              } />
            </button>
          </div>
        </div>
        
        {/* Feedback Learning Toggle */}
        <div className="mt-3 flex items-center justify-center gap-4">
          <label className="flex items-center gap-2 text-sm text-gray-400 cursor-pointer">
            <input
              type="checkbox"
              defaultChecked={true}
              className="rounded"
            />
            Enable Feedback Learning
          </label>
        </div>
      </div>
    </div>
  );
}