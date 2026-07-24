import React, { useState } from 'react';
import { Search, Loader2, Sparkles } from 'lucide-react';
import { STRINGS } from '../constants/strings';

export default function HeroSection({ onAnalyze, loading }) {
  const [url, setUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url) onAnalyze(url);
  };

  return (
    <div className="hero-container animate-fade-in">
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
        <Sparkles color="var(--quantum-cyan)" size={32} />
        <h2 style={{ color: 'var(--quantum-cyan)', letterSpacing: '2px', textTransform: 'uppercase', fontSize: '1rem' }}>{STRINGS.HERO.SYSTEM_TAG}</h2>
      </div>
      
      <h1 className="hero-title">{STRINGS.HERO.TITLE}</h1>
      <p className="hero-subtitle">
        {STRINGS.HERO.SUBTITLE}
      </p>

      <form onSubmit={handleSubmit} className="hero-input-group">
        <div style={{ position: 'relative', flex: 1 }}>
          <Search size={20} color="var(--muted-platinum)" style={{ position: 'absolute', left: '20px', top: '18px' }} />
          <input 
            type="text" 
            className="hero-input" 
            placeholder={STRINGS.HERO.INPUT_PLACEHOLDER}
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            style={{ paddingLeft: '56px', width: '100%', boxSizing: 'border-box' }}
            disabled={loading}
          />
        </div>
        <button type="submit" className="btn-primary" disabled={loading} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {loading ? (
            <>
              <Loader2 className="lucide-spin" size={20} /> {STRINGS.HERO.BUTTON_ANALYZING}
            </>
          ) : (
            STRINGS.HERO.BUTTON_ANALYZE
          )}
        </button>
      </form>
    </div>
  );
}

