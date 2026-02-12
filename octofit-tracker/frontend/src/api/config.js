/**
 * API Configuration
 * Centralizes API base URL construction for consistency across components
 */

const getApiBaseUrl = () => {
  const codespaceName = process.env.REACT_APP_CODESPACE_NAME;
  
  if (codespaceName) {
    // GitHub Codespaces environment
    // Check if it already includes the full domain or just the codespace name
    if (codespaceName.includes('.app.github.dev')) {
      // Full URL already provided
      return `https://${codespaceName}/api`;
    } else {
      // Just codespace name - construct full URL with port and domain
      return `https://${codespaceName}-8000.app.github.dev/api`;
    }
  }
  
  // Local development
  return 'http://localhost:8000/api';
};

export const API_BASE_URL = getApiBaseUrl();

export const API_ENDPOINTS = {
  USERS: `${API_BASE_URL}/users/`,
  TEAMS: `${API_BASE_URL}/teams/`,
  ACTIVITIES: `${API_BASE_URL}/activities/`,
  LEADERBOARD: `${API_BASE_URL}/leaderboard/`,
  WORKOUTS: `${API_BASE_URL}/workouts/`,
};
