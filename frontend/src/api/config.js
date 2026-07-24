const DEFAULT_API_BASE_URL = 'http://localhost:8000';

export const getApiBaseUrl = () => {
  return import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE_URL;
};

export const API_ENDPOINTS = {
  PREVIEW: `${getApiBaseUrl()}/api/preview`,
  SCRAPE: `${getApiBaseUrl()}/api/scrape`,
  HEALTH: `${getApiBaseUrl()}/api/health`
};
