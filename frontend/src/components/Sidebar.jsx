// frontend/src/components/Sidebar.jsx
import React from 'react';
import { Plus, BarChart3, Info, User, Settings } from 'lucide-react';

export default function Sidebar({ 
  showSidebar, 
  messages, 
  onNewChat, 
  onNavigate,
  currentTab 
}) {
  const recentChats = messages
    .filter(m => m.role === 'user')
    .slice(-10)
    .reverse();

  return (
    <div className={`${showSidebar ? 'w-64' : 'w-0'} bg-gray-900 border-r border-gray-800 transition-all duration-300 overflow-hidden flex flex-col`}>
      {/* New Chat Button */}
      <div className="p-4 border-b border-gray-800">
        <button 
          onClick={onNewChat}
          className="w-full flex items-center gap-3 px-4 py-3 rounded-lg bg-gray-800 hover:bg-gray-750 transition-colors"
        >
          <Plus size={18} />
          <span className="font-medium">New Chat</span>
        </button>
      </div>

      {/* Chat History */}
      <div className="flex-1 overflow-y-auto p-3">
        <div className="space-y-1">
          {recentChats.map((msg, idx) => (
            <button
              key={idx}
              className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-800 transition-colors text-sm text-gray-300 truncate"
            >
              {msg.content}
            </button>
          ))}
        </div>
      </div>

      {/* Navigation Menu */}
      <div className="border-t border-gray-800 p-3 space-y-1">
        <button 
          onClick={() => onNavigate('stats')}
          className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm ${
            currentTab === 'stats' ? 'bg-gray-800' : 'hover:bg-gray-800'
          }`}
        >
          <BarChart3 size={18} />
          <span>Analytics</span>
        </button>
        
        <button 
          onClick={() => onNavigate('about')}
          className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm ${
            currentTab === 'about' ? 'bg-gray-800' : 'hover:bg-gray-800'
          }`}
        >
          <Info size={18} />
          <span>About</span>
        </button>
        
        <button 
          className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-800 transition-colors text-sm"
        >
          <User size={18} />
          <span>Account</span>
        </button>
        
        <button 
          className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-800 transition-colors text-sm"
        >
          <Settings size={18} />
          <span>Settings</span>
        </button>
      </div>
    </div>
  );
}