'use client';

import { useState } from 'react';
import { analysisAPI } from '@/lib/api';
import { TrendingUp, TrendingDown, AlertCircle, Target } from 'lucide-react';

interface SWOTResult {
  id: string;
  company_name: string;
  industry: string;
  analysis: {
    strengths: string[];
    weaknesses: string[];
    opportunities: string[];
    threats: string[];
    summary: string;
    recommendations: string[];
  };
}

export default function SWOTAnalysis() {
  const [companyName, setCompanyName] = useState('');
  const [industry, setIndustry] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SWOTResult | null>(null);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!companyName || !industry) {
      setError('Please fill in all fields');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const data = await analysisAPI.generateSWOT({
        company_name: companyName,
        industry,
        use_rag: true,
      });
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Failed to generate analysis');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4">SWOT Analysis Generator</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium mb-2">Company Name</label>
            <input
              type="text"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., Tesla"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-2">Industry</label>
            <input
              type="text"
              value={industry}
              onChange={(e) => setIndustry(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., clean_tech"
            />
          </div>
        </div>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition"
        >
          {loading ? 'Analyzing...' : 'Generate SWOT Analysis'}
        </button>
      </div>

      {result && (
        <div className="space-y-4">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-bold mb-2">{result.company_name}</h3>
            <p className="text-gray-600 mb-4">{result.analysis.summary}</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-green-50 p-6 rounded-lg border border-green-200">
              <div className="flex items-center mb-3">
                <TrendingUp className="text-green-600 mr-2" />
                <h4 className="text-lg font-semibold text-green-800">Strengths</h4>
              </div>
              <ul className="space-y-2">
                {result.analysis.strengths.map((item, idx) => (
                  <li key={idx} className="text-gray-700">• {item}</li>
                ))}
              </ul>
            </div>

            <div className="bg-red-50 p-6 rounded-lg border border-red-200">
              <div className="flex items-center mb-3">
                <TrendingDown className="text-red-600 mr-2" />
                <h4 className="text-lg font-semibold text-red-800">Weaknesses</h4>
              </div>
              <ul className="space-y-2">
                {result.analysis.weaknesses.map((item, idx) => (
                  <li key={idx} className="text-gray-700">• {item}</li>
                ))}
              </ul>
            </div>

            <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
              <div className="flex items-center mb-3">
                <Target className="text-blue-600 mr-2" />
                <h4 className="text-lg font-semibold text-blue-800">Opportunities</h4>
              </div>
              <ul className="space-y-2">
                {result.analysis.opportunities.map((item, idx) => (
                  <li key={idx} className="text-gray-700">• {item}</li>
                ))}
              </ul>
            </div>

            <div className="bg-yellow-50 p-6 rounded-lg border border-yellow-200">
              <div className="flex items-center mb-3">
                <AlertCircle className="text-yellow-600 mr-2" />
                <h4 className="text-lg font-semibold text-yellow-800">Threats</h4>
              </div>
              <ul className="space-y-2">
                {result.analysis.threats.map((item, idx) => (
                  <li key={idx} className="text-gray-700">• {item}</li>
                ))}
              </ul>
            </div>
          </div>

          {result.analysis.recommendations.length > 0 && (
            <div className="bg-purple-50 p-6 rounded-lg border border-purple-200">
              <h4 className="text-lg font-semibold text-purple-800 mb-3">
                Recommendations
              </h4>
              <ul className="space-y-2">
                {result.analysis.recommendations.map((item, idx) => (
                  <li key={idx} className="text-gray-700">• {item}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
