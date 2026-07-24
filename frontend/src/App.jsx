import React, { useState } from 'react';
import HeroSection from './components/HeroSection';
import PreviewCards from './components/PreviewCards';
import ResultsDashboard from './components/ResultsDashboard';
import './App.css';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

function App() {
  const [appState, setAppState] = useState('HERO'); // HERO, PREVIEW, RESULTS
  const [url, setUrl] = useState('');
  const [sections, setSections] = useState([]);
  const [domStats, setDomStats] = useState(null);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (inputUrl) => {
    setUrl(inputUrl);
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/preview`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: inputUrl })
      });
      const data = await response.json();
      if (data.success) {
        setSections(data.sections);
        setDomStats(data.dom_stats);
        setAppState('PREVIEW');
      } else {
        alert("Error: " + data.error);
      }
    } catch (err) {
      alert("Failed to connect to backend.");
    }
    setLoading(false);
  };

  const handleExtract = async (selectedSections) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/scrape`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          url: url,
          selected_sections: selectedSections 
        })
      });
      const data = await response.json();
      if (data.success) {
        setReport(data.report);
        setAppState('RESULTS');
      } else {
        alert("Error: " + data.error);
      }
    } catch (err) {
      alert("Failed to connect to backend.");
    }
    setLoading(false);
  };

  const resetFlow = () => {
    setAppState('HERO');
    setUrl('');
    setSections([]);
    setDomStats(null);
    setReport(null);
  };

  return (
    <>
      <div className="ambient-bg"></div>
      <div className="ambient-glow"></div>
      
      <main className="container animate-fade-in" style={{ padding: '40px 0' }}>
        {appState === 'HERO' && (
          <HeroSection 
            onAnalyze={handleAnalyze} 
            loading={loading} 
          />
        )}
        
        {appState === 'PREVIEW' && (
          <PreviewCards 
            url={url} 
            sections={sections} 
            domStats={domStats}
            onExtract={handleExtract} 
            onBack={resetFlow} 
            loading={loading} 
          />
        )}
        
        {appState === 'RESULTS' && (
          <ResultsDashboard 
            report={report} 
            onNewScrape={resetFlow} 
          />
        )}
      </main>
    </>
  );
}

export default App;
