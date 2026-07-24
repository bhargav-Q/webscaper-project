import { API_ENDPOINTS } from './config';

export const previewWebsite = async (url) => {
  const response = await fetch(API_ENDPOINTS.PREVIEW, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url })
  });
  return await response.json();
};

export const scrapeWebsite = async (url, selectedSections) => {
  const response = await fetch(API_ENDPOINTS.SCRAPE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      url,
      selected_sections: selectedSections 
    })
  });
  return await response.json();
};
