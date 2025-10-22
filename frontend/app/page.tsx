'use client';

import { useState } from 'react';
import SWOTAnalysis from '@/components/SWOTAnalysis';
import TrendAnalysis from '@/components/TrendAnalysis';
import { BarChart3, Target } from 'lucide-react';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'swot' | 'trends'>('swot');

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            AI Market Intelligence Dashboard
          </h1>
          <p className="text-gray-600">
            Generate insights using LLM-powered analysis and RAG
          </p>
        </header>

        {/* Navigation Tabs */}
        <div className="flex space-x-4 mb-6">
          <button
            onClick={() => setActiveTab('swot')}
            className={`flex items-center px-6 py-3 rounded-lg font-medium transition ${
              activeTab === 'swot'
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-white text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Target className="mr-2" size={20} />
            SWOT Analysis
          </button>
          <button
            onClick={() => setActiveTab('trends')}
            className={`flex items-center px-6 py-3 rounded-lg font-medium transition ${
              activeTab === 'trends'
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-white text-gray-600 hover:bg-gray-100'
            }`}
          >
            <BarChart3 className="mr-2" size={20} />
            Trend Analysis
          </button>
        </div>

        {/* Content */}
        <div className="max-w-7xl">
          {activeTab === 'swot' && <SWOTAnalysis />}
          {activeTab === 'trends' && <TrendAnalysis />}
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-gray-500 text-sm">
          <p>Built with FastAPI, Next.js, OpenAI, Pinecone & MongoDB</p>
          <p className="mt-2">Portfolio project by Jumar Juaton</p>
        </footer>
      </div>
    </main>
  );
}
