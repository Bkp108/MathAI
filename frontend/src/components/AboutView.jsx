// frontend/src/components/AboutView.jsx
import React from 'react';

export default function AboutView() {
  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h2 className="text-2xl font-semibold text-gray-100 mb-6">
        ℹ️ About MathAI
      </h2>
      
      {/* Features */}
      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 mb-6">
        <h3 className="text-lg font-semibold text-gray-100 mb-3">
          Features
        </h3>
        <ul className="space-y-2 text-gray-300">
          <li>✅ Smart routing: Knowledge Base → Web Search → LLM</li>
          <li>✅ Input/Output guardrails for safety</li>
          <li>✅ Human-in-the-loop feedback</li>
          <li>✅ Continuous learning from feedback</li>
          <li>✅ FREE Gemini 1.5 Flash API</li>
          <li>✅ Vector database with semantic search</li>
          <li>✅ Real-time analytics dashboard</li>
        </ul>
      </div>

      {/* Technology Stack */}
      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 mb-6">
        <h3 className="text-lg font-semibold text-gray-100 mb-3">
          Technology Stack
        </h3>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <div className="text-gray-400 mb-2">Backend</div>
            <ul className="space-y-1 text-gray-300">
              <li>• FastAPI</li>
              <li>• Google Gemini AI</li>
              <li>• Qdrant Vector DB</li>
              <li>• Tavily Search</li>
              <li>• SQLite</li>
            </ul>
          </div>
          <div>
            <div className="text-gray-400 mb-2">Frontend</div>
            <ul className="space-y-1 text-gray-300">
              <li>• React 18</li>
              <li>• Vite</li>
              <li>• Tailwind CSS</li>
              <li>• Lucide Icons</li>
              <li>• Axios</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Sample Questions */}
      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
        <h3 className="text-lg font-semibold text-gray-100 mb-3">
          Sample Questions
        </h3>
        <ul className="space-y-2 text-gray-300">
          <li>• "Solve for x: 2x + 5 = 13"</li>
          <li>• "Find the derivative of x²"</li>
          <li>• "Calculate the area of a circle with radius 5"</li>
          <li>• "What is the Pythagorean theorem?"</li>
          <li>• "Integrate sin(x)dx"</li>
          <li>• "Factor x² + 5x + 6"</li>
        </ul>
      </div>
    </div>
  );
}