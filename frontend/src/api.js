import axios from 'axios';

// Base URL for the backend API. During development this will point to the
// local FastAPI server. In production you may deploy the backend to a
// separate host and update this accordingly.
const API_BASE_URL = 'http://localhost:8000';

/**
 * Fetch bet suggestions from the backend.
 *
 * @param {string} date - ISO date string (YYYY-MM-DD). If omitted, the
 *   backend will use the current date.
 * @param {number} limit - Maximum number of suggestions to return.
 * @returns {Promise<object>} Response containing `date` and `suggestions`.
 */
export async function fetchSuggestions(date, limit = 10) {
  const params = {};
  if (date) params.query_date = date;
  if (limit) params.limit = limit;
  const response = await axios.get(`${API_BASE_URL}/api/suggestions`, { params });
  return response.data;
}