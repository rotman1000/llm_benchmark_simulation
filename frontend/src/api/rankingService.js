import axios from 'axios';

// Define the base URL for the API
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;
const API_KEY = process.env.REACT_APP_API_KEY;

/**
 * Function to fetch rankings for a given metric.
 * @param {string} metric - The metric to rank the LLMs by (e.g., 'ttft', 'tps', 'e2e_latency', 'rps').
 * @returns {Promise} - A promise that resolves to the API response data.
 */
export const getRankingsByMetric = async (metric) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/rankings/${metric}`,
      {headers: {
        'api-key': `${API_KEY}` 
      }}
    );
    return response.data;
  } catch (error) {
    console.log(error)
    throw new Error('Error fetching rankings data.');
  }
};
