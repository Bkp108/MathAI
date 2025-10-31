// frontend/src/components/SettingsPanel.jsx
import React, { useState } from 'react';
import { X } from 'lucide-react';

export default function SettingsPanel({ isOpen, onClose }) {
  const [temperature, setTemperature] = useState(0.3);
  const [theme, setTheme] = useState('dark');

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-gray-900 rounded-xl p-6 w-full max-w-md border border-gray-800">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-semibold">Settings</h3>
          <button onClick={onClose} className="p-1 hover:bg-gray-800 rounded">
            <X size={20} />
          </button>
        </div>
        
        <div className="space-y-4">
          {/* Theme */}
          <div>
            <label className="block text-sm text-gray-400 mb-2">Theme</label>
            <select 
              value={theme}
              onChange={(e) => setTheme(e.target.value)}
              className="w-full bg-gray-800 rounded-lg px-3 py-2 border border-gray-700 outline-none"
            >
              <option value="dark">Dark</option>
              <option value="light">Light</option>
              <option value="system">System</option>
            </select>
          </div>

          {/* Model Temperature */}
          <div>
            <label className="block text-sm text-gray-400 mb-2">
              Model Temperature: {temperature}
            </label>
            <input 
              type="range" 
              min="0" 
              max="1" 
              step="0.1"
              value={temperature}
              onChange={(e) => setTemperature(parseFloat(e.target.value))}
              className="w-full" 
            />
            <div className="text-xs text-gray-500 mt-1">
              Lower = more focused, Higher = more creative
            </div>
          </div>

          {/* Save Button */}
          <button 
            onClick={onClose}
            className="w-full bg-blue-600 hover:bg-blue-700 py-2 rounded-lg font-medium transition-colors"
          >
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
}