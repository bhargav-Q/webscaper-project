import React, { useState } from 'react';
import HeroSection from './components/HeroSection';
import PreviewCards from './components/PreviewCards';
import ResultsDashboard from './components/ResultsDashboard';
import { APP_STATES } from './constants/appConstants';
import { STRINGS } from './constants/strings';
import { previewWebsite, scrapeWebsite } from './api/scraperService';
import './App.css';

function App() {
  const [appState, setAppState] = useState(APP_STATES.HERO);
  const [url, setUrl] = useState('');
  const [sections, setSections] = useState([]);
  const [domStats, setDomStats] = useState(null);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (inputUrl) => {
    setUrl(inputUrl);
    setLoading(true);
    try {
      const data = await previewWebsite(inputUrl);
      if (data.success) {
        setSections(data.sections);
        setDomStats(data.dom_stats);
        setAppState(APP_STATES.PREVIEW);
      } else {
        alert(STRINGS.ALERTS.ERROR_PREFIX + data.error);
      }
    } catch (err) {
      console.error(err);
      alert(STRINGS.ALERTS.NETWORK_ERROR);
    }
    setLoading(false);
  };

  const handleExtract = async (selectedSections) => {
    setLoading(true);
    try {
      const data = await scrapeWebsite(url, selectedSections);
      if (data.success) {
        setReport(data.report);
        setAppState(APP_STATES.RESULTS);
      } else {
        alert(STRINGS.ALERTS.ERROR_PREFIX + data.error);
      }
    } catch (err) {
      console.error(err);
      alert(STRINGS.ALERTS.NETWORK_ERROR);
    }
    setLoading(false);
  };

  const resetFlow = () => {
    setAppState(APP_STATES.HERO);
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
        {appState === APP_STATES.HERO && (
          <HeroSection 
            onAnalyze={handleAnalyze} 
            loading={loading} 
          />
        )}
        
        {appState === APP_STATES.PREVIEW && (
          <PreviewCards 
            url={url} 
            sections={sections} 
            domStats={domStats}
            onExtract={handleExtract} 
            onBack={resetFlow} 
            loading={loading} 
          />
        )}
        
        {appState === APP_STATES.RESULTS && (
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

