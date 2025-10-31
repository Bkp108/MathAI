// frontend/src/App.jsx
import React, { useState, useEffect } from 'react';
import { Menu } from 'lucide-react';

// Import components
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import InputArea from './components/InputArea';
import FeedbackModal from './components/FeedbackModal';
import AnalyticsView from './components/AnalyticsView';
import AboutView from './components/AboutView';
import SettingsPanel from './components/SettingsPanel';

// Import custom hook
import useChat from './hooks/useChat';

export default function App() {
  const [showSidebar, setShowSidebar] = useState(true);
  const [currentTab, setCurrentTab] = useState('chat');
  const [feedbackMode, setFeedbackMode] = useState(false);
  const [selectedMessage, setSelectedMessage] = useState(null);
  const [showSettings, setShowSettings] = useState(false);

  // Use custom chat hook
  const {
    messages,
    loading,
    error,
    sendMessage,
    clearMessages,
    submitFeedback
  } = useChat();

  // Handle example question clicks
  useEffect(() => {
    const handleExampleClick = (e) => {
      sendMessage(e.detail);
    };

    window.addEventListener('exampleClick', handleExampleClick);
    return () => window.removeEventListener('exampleClick', handleExampleClick);
  }, [sendMessage]);

  const handleNewChat = () => {
    clearMessages();
    setCurrentTab('chat');
  };

  const handleNavigate = (tab) => {
    setCurrentTab(tab);
  };

  const handleMessageAction = (message, action) => {
    if (action === 'feedback') {
      setSelectedMessage(message);
      setFeedbackMode(true);
    } else if (action === 'like' || action === 'dislike') {
      // Quick feedback without modal
      submitFeedback(message, {
        rating: action === 'like' ? 5 : 2,
        comment: null,
        improved_solution: null
      });
    }
  };

  const handleFeedbackSubmit = async (feedbackData) => {
    if (selectedMessage) {
      const success = await submitFeedback(selectedMessage, feedbackData);
      
      if (success) {
        alert('✅ Feedback submitted! Thank you for helping us improve.');
      } else {
        alert('❌ Failed to submit feedback. Please try again.');
      }
    }
    
    setFeedbackMode(false);
    setSelectedMessage(null);
  };

  return (
    <div className="flex h-screen bg-gray-950 text-white">
      {/* Sidebar */}
      <Sidebar 
        showSidebar={showSidebar}
        messages={messages}
        onNewChat={handleNewChat}
        onNavigate={handleNavigate}
        currentTab={currentTab}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="h-14 border-b border-gray-800 flex items-center justify-between px-4">
          <div className="flex items-center gap-3">
            <button 
              onClick={() => setShowSidebar(!showSidebar)}
              className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
            >
              <Menu size={20} />
            </button>
            <h1 className="text-lg font-semibold">🧮 MathAI</h1>
          </div>
          
          {error && (
            <div className="text-sm text-red-400">
              Error: {error}
            </div>
          )}
        </div>

        {/* Content */}
        {currentTab === 'chat' ? (
          <>
            <ChatWindow 
              messages={messages}
              loading={loading}
              onMessageAction={handleMessageAction}
            />
            <InputArea 
              onSend={sendMessage}
              loading={loading}
              disabled={false}
            />
          </>
        ) : currentTab === 'stats' ? (
          <AnalyticsView messages={messages} />
        ) : currentTab === 'about' ? (
          <AboutView />
        ) : null}
      </div>

      {/* Modals */}
      <FeedbackModal 
        isOpen={feedbackMode}
        onClose={() => setFeedbackMode(false)}
        onSubmit={handleFeedbackSubmit}
        message={selectedMessage}
      />

      <SettingsPanel 
        isOpen={showSettings}
        onClose={() => setShowSettings(false)}
      />
    </div>
  );
}