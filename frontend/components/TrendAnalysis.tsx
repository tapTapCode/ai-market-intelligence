'use client';

import { useState } from 'react';
import { analysisAPI } from '@/lib/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface TrendResult {
  id: string;
  industry: string;
  time_period: string;
  analysis: {
    emerging_trends: Array<{
      trend: string;
      description: string;
      impact: string;
    }>;
    declining_trends: Array<{
      trend: string;
      description: string;
      impact: string;
    }>;
    summary: string;
    key_insights: string[];
    predictions: string[];
  };
}

export default function TrendAnalysis() {
  const [industry, setIndustry] = useState('');
  const [timePeriod, setTimePeriod] = useState('current');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<TrendResult | null>(null);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!industry) {
      setError('Please enter an industry');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const data = await analysisAPI.analyzeTrends({
        industry,
        time_period: timePeriod,
        use_rag: true,
      });
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Failed to analyze trends');
    } finally {
      setLoading(false);
    }
  };

  const chartData = result ? [
    {
      name: 'Emerging',
      High: result.analysis.emerging_trends.filter(t => t.impact === 'high').length,
      Medium: result.analysis.emerging_trends.filter(t => t.impact === 'medium').length,
      Low: result.analysis.emerging_trends.filter(t => t.impact === 'low').length,
    },
    {
      name: 'Declining',
      High: result.analysis.declining_trends.filter(t => t.impact === 'high').length,
      Medium: result.analysis.declining_trends.filter(t => t.impact === 'medium').length,
      Low: result.analysis.declining_trends.filter(t => t.impact === 'low').length,
    },
  ] : [];

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4">Market Trend Analysis</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
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
          
          <div>
            <label className="block text-sm font-medium mb-2">Time Period</label>
            <input
              type="text"
              value={timePeriod}
              onChange={(e) => setTimePeriod(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., Q1 2024"
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
          {loading ? 'Analyzing...' : 'Analyze Trends'}
        </button>
      </div>

      {result && (
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-bold mb-2">{result.industry} - {result.time_period}</h3>
            <p className="text-gray-600">{result.analysis.summary}</p>
          </div>

          {/* Trends Chart */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h4 className="text-lg font-semibold mb-4">Trend Impact Distribution</h4>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="High" fill="#ef4444" />
                <Bar dataKey="Medium" fill="#f59e0b" />
                <Bar dataKey="Low" fill="#10b981" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Emerging Trends */}
          <div className="bg-green-50 p-6 rounded-lg border border-green-200">
            <div className="flex items-center mb-4">
              <TrendingUp className="text-green-600 mr-2" size={24} />
              <h4 className="text-lg font-semibold text-green-800">Emerging Trends</h4>
            </div>
            <div className="space-y-4">
              {result.analysis.emerging_trends.map((trend, idx) => (
                <div key={idx} className="bg-white p-4 rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <h5 className="font-semibold text-gray-800">{trend.trend}</h5>
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      trend.impact === 'high' ? 'bg-red-100 text-red-700' :
                      trend.impact === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-green-100 text-green-700'
                    }`}>
                      {trend.impact} impact
                    </span>
                  </div>
                  <p className="text-gray-600 text-sm">{trend.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Declining Trends */}
          {result.analysis.declining_trends.length > 0 && (
            <div className="bg-orange-50 p-6 rounded-lg border border-orange-200">
              <div className="flex items-center mb-4">
                <TrendingDown className="text-orange-600 mr-2" size={24} />
                <h4 className="text-lg font-semibold text-orange-800">Declining Trends</h4>
              </div>
              <div className="space-y-4">
                {result.analysis.declining_trends.map((trend, idx) => (
                  <div key={idx} className="bg-white p-4 rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <h5 className="font-semibold text-gray-800">{trend.trend}</h5>
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        trend.impact === 'high' ? 'bg-red-100 text-red-700' :
                        trend.impact === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                        'bg-green-100 text-green-700'
                      }`}>
                        {trend.impact} impact
                      </span>
                    </div>
                    <p className="text-gray-600 text-sm">{trend.description}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Key Insights */}
          <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
            <h4 className="text-lg font-semibold text-blue-800 mb-3">Key Insights</h4>
            <ul className="space-y-2">
              {result.analysis.key_insights.map((insight, idx) => (
                <li key={idx} className="text-gray-700">• {insight}</li>
              ))}
            </ul>
          </div>

          {/* Predictions */}
          {result.analysis.predictions.length > 0 && (
            <div className="bg-purple-50 p-6 rounded-lg border border-purple-200">
              <h4 className="text-lg font-semibold text-purple-800 mb-3">Predictions</h4>
              <ul className="space-y-2">
                {result.analysis.predictions.map((prediction, idx) => (
                  <li key={idx} className="text-gray-700">• {prediction}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
