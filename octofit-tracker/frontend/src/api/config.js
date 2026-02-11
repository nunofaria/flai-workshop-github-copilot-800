/**
 * API Configuration
 * Centralizes API base URL construction for consistency across components
 */

const getApiBaseUrl = () => {
  const codespace = process.env.REACT_APP_CODESPACE_NAME || 'localhost:8000';
  const protocol = process.env.REACT_APP_CODESPACE_NAME ? 'https' : 'http';
  return `${protocol}://${codespace}/api`;
};

export const API_BASE_URL = getApiBaseUrl();

export const API_ENDPOINTS = {
  USERS: `${API_BASE_URL}/users/`,
  TEAMS: `${API_BASE_URL}/teams/`,
  ACTIVITIES: `${API_BASE_URL}/activities/`,
  LEADERBOARD: `${API_BASE_URL}/leaderboard/`,
  WORKOUTS: `${API_BASE_URL}/workouts/`,
};
