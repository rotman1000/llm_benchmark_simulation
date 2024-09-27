import React, { useState } from 'react';
import { getRankingsByMetric } from '../api/rankingService';

const Ranking = () => {
  const [rankings, setRankings] = useState([]);
  const [metric, setMetric] = useState('TTFT');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchRankings = async () => {
    setLoading(true);  // Set loading state when fetching starts
    setError(null);    // Clear any previous error
    try {
      const data = await getRankingsByMetric(metric);
      setRankings(data.rankings);  // Update rankings with the correct data
    } catch (error) {
      setError('Error fetching the rankings. Please try again later.');
    } finally {
      setLoading(false);  // Stop loading once the process is complete
    }
  };

  const handleMetricChange = (e) => {
    setMetric(e.target.value); // Change metric when user selects a new one
  };

  return (
    <div>
      <h2>LLM Rankings for {metric.toUpperCase()}</h2>

      <label htmlFor="metric">Select a Metric: </label>
      <select id="metric" value={metric} onChange={handleMetricChange}>
        <option value="TTFT">Time to First Token (TTFT)</option>
        <option value="TPS">Tokens Per Second (TPS)</option>
        <option value="e2e_latency">End-to-End Latency (e2e_latency)</option>
        <option value="RPS">Requests Per Second (RPS)</option>
      </select>

      <button onClick={fetchRankings} disabled={loading}>
        {loading ? 'Fetching...' : 'Fetch Rankings'}
      </button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <ul>
        {rankings.length > 0 ? (
          rankings.map((llm, index) => (
            <li key={index}>
              {index + 1}. {llm.llm} - Mean: {llm.mean.toFixed(2)} {/* Access the correct fields */}
            </li>
          ))
        ) : (
          !loading && <p>No rankings to display. Click "Fetch Rankings" to load.</p>
        )}
      </ul>
    </div>
  );
};

export default Ranking;
