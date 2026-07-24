import React, { useState } from 'react';
import { ArrowLeft, Check, Layers, Loader2 } from 'lucide-react';
import { STRINGS } from '../constants/strings';

export default function PreviewCards({ url, sections, domStats, onExtract, onBack, loading }) {
  const [selectedIds, setSelectedIds] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  const filteredSections = sections.filter(sec => {
    const term = searchTerm.toLowerCase();
    const tagMatch = sec.tag?.toLowerCase().includes(term);
    const classMatch = sec.class?.toLowerCase().includes(term);
    const previewMatch = sec.preview?.toLowerCase().includes(term);
    return tagMatch || classMatch || previewMatch;
  });

  const toggleSection = (sectionInfo) => {
    const isSelected = selectedIds.some(s => s.section_id === sectionInfo.section_id);
    if (isSelected) {
      setSelectedIds(selectedIds.filter(s => s.section_id !== sectionInfo.section_id));
    } else {
      setSelectedIds([...selectedIds, sectionInfo]);
    }
  };

  const handleExtract = () => {
    // If none selected, we extract full page
    onExtract(selectedIds.length > 0 ? selectedIds : null);
  };

  return (
    <div className="animate-fade-in" style={{ paddingBottom: '100px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-md)' }}>
        <button className="btn-secondary" onClick={onBack} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <ArrowLeft size={18} /> {STRINGS.PREVIEW.BACK_BUTTON}
        </button>
        <div>
          <h2 style={{ fontSize: '1.5rem', marginBottom: '4px' }}>{STRINGS.PREVIEW.HEADER_TITLE}</h2>
          <p style={{ color: 'var(--muted-platinum)', fontSize: '0.9rem' }}>{STRINGS.PREVIEW.ANALYZING_LABEL}{url}</p>
        </div>
        <div style={{ width: '100px' }}></div> {/* Spacer for center alignment */}
      </div>

      {domStats && (
        <div className="glass-card" style={{ marginBottom: '24px', padding: '16px', display: 'flex', gap: '24px', flexWrap: 'wrap', justifyContent: 'center' }}>
          <div style={{ textAlign: 'center' }}><strong style={{ color: 'var(--quantum-cyan)', fontSize: '1.2rem' }}>{domStats.articles}</strong><div style={{ fontSize: '0.8rem', color: 'var(--muted-platinum)', textTransform: 'uppercase' }}>{STRINGS.PREVIEW.STATS.ARTICLES}</div></div>
          <div style={{ textAlign: 'center' }}><strong style={{ color: 'var(--quantum-cyan)', fontSize: '1.2rem' }}>{domStats.cards}</strong><div style={{ fontSize: '0.8rem', color: 'var(--muted-platinum)', textTransform: 'uppercase' }}>{STRINGS.PREVIEW.STATS.CARDS}</div></div>
          <div style={{ textAlign: 'center' }}><strong style={{ color: 'var(--quantum-cyan)', fontSize: '1.2rem' }}>{domStats.images}</strong><div style={{ fontSize: '0.8rem', color: 'var(--muted-platinum)', textTransform: 'uppercase' }}>{STRINGS.PREVIEW.STATS.IMAGES}</div></div>
          <div style={{ textAlign: 'center' }}><strong style={{ color: 'var(--quantum-cyan)', fontSize: '1.2rem' }}>{domStats.links}</strong><div style={{ fontSize: '0.8rem', color: 'var(--muted-platinum)', textTransform: 'uppercase' }}>{STRINGS.PREVIEW.STATS.LINKS}</div></div>
          <div style={{ textAlign: 'center' }}><strong style={{ color: 'var(--quantum-cyan)', fontSize: '1.2rem' }}>{domStats.tables}</strong><div style={{ fontSize: '0.8rem', color: 'var(--muted-platinum)', textTransform: 'uppercase' }}>{STRINGS.PREVIEW.STATS.TABLES}</div></div>
          <div style={{ textAlign: 'center' }}><strong style={{ color: 'var(--quantum-cyan)', fontSize: '1.2rem' }}>{domStats.forms}</strong><div style={{ fontSize: '0.8rem', color: 'var(--muted-platinum)', textTransform: 'uppercase' }}>{STRINGS.PREVIEW.STATS.FORMS}</div></div>
        </div>
      )}

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <input 
          type="text" 
          placeholder={STRINGS.PREVIEW.SEARCH_PLACEHOLDER}
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            padding: '8px 16px',
            borderRadius: '6px',
            border: '1px solid rgba(148, 163, 184, 0.3)',
            background: 'rgba(15, 23, 42, 0.4)',
            color: 'var(--starlight-white)',
            width: '300px',
            fontSize: '0.95rem',
            outline: 'none'
          }}
          onFocus={(e) => e.target.style.borderColor = 'var(--quantum-cyan)'}
          onBlur={(e) => e.target.style.borderColor = 'rgba(148, 163, 184, 0.3)'}
        />
        <button 
          onClick={() => {
            const filteredIds = filteredSections.map(s => s.section_id);
            const allFilteredSelected = filteredIds.every(id => selectedIds.some(s => s.section_id === id));
            
            if (allFilteredSelected && filteredSections.length > 0) {
              // Deselect the filtered ones
              setSelectedIds(selectedIds.filter(s => !filteredIds.includes(s.section_id)));
            } else {
              // Select the filtered ones
              const newSelected = [...selectedIds];
              filteredSections.forEach(sec => {
                if (!newSelected.some(s => s.section_id === sec.section_id)) {
                  newSelected.push(sec);
                }
              });
              setSelectedIds(newSelected);
            }
          }}
          style={{
            background: 'rgba(6, 182, 212, 0.1)',
            border: '1px solid var(--quantum-cyan)',
            color: 'var(--quantum-cyan)',
            padding: '8px 16px',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '0.9rem',
            fontWeight: 'bold',
            transition: 'all 0.2s'
          }}
          onMouseOver={(e) => e.currentTarget.style.background = 'rgba(6, 182, 212, 0.2)'}
          onMouseOut={(e) => e.currentTarget.style.background = 'rgba(6, 182, 212, 0.1)'}
        >
          {(() => {
            const filteredIds = filteredSections.map(s => s.section_id);
            const allFilteredSelected = filteredIds.every(id => selectedIds.some(s => s.section_id === id));
            return allFilteredSelected && filteredSections.length > 0 ? STRINGS.PREVIEW.DESELECT_ALL : STRINGS.PREVIEW.SELECT_ALL;
          })()}
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 'var(--space-sm)' }}>
        {filteredSections.map((sec) => (
          <div 
            key={sec.section_id} 
            className="glass-card" 
            style={{ 
              cursor: 'pointer',
              borderColor: selectedIds.some(s => s.section_id === sec.section_id) ? 'var(--quantum-cyan)' : undefined,
              boxShadow: selectedIds.some(s => s.section_id === sec.section_id) ? '0 0 15px rgba(6,182,212,0.3)' : undefined
            }}
            onClick={() => toggleSection(sec)}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Layers size={18} color="var(--quantum-cyan)" />
                <strong style={{ color: 'var(--starlight-white)', textTransform: 'uppercase', letterSpacing: '1px', fontSize: '0.8rem' }}>
                  {sec.tag} {sec.class ? `.${sec.class.split(' ')[0]}` : ''}
                </strong>
              </div>
              <input 
                type="checkbox" 
                className="custom-checkbox"
                checked={selectedIds.some(s => s.section_id === sec.section_id)}
                readOnly
              />
            </div>
            <p style={{ fontSize: '0.85rem', color: 'var(--muted-platinum)', display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
              {sec.preview}
            </p>
          </div>
        ))}
      </div>

      {sections.length === 0 && (
        <div style={{ textAlign: 'center', padding: '60px', color: 'var(--muted-platinum)' }}>
          <p>{STRINGS.PREVIEW.EMPTY_SECTIONS}</p>
        </div>
      )}

      {/* Floating Action Button */}
      <div style={{ position: 'fixed', bottom: '40px', left: '50%', transform: 'translateX(-50%)', zIndex: 100 }}>
        <button 
          className="btn-primary" 
          onClick={handleExtract}
          disabled={loading}
          style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '16px 32px', fontSize: '1.1rem', boxShadow: '0 8px 32px rgba(16,185,129,0.3)' }}
        >
          {loading ? <Loader2 className="lucide-spin" size={24} /> : <Check size={24} />}
          {loading ? STRINGS.PREVIEW.BUTTON_EXTRACTING : `${STRINGS.PREVIEW.BUTTON_EXTRACT_PREFIX}${selectedIds.length > 0 ? selectedIds.length + STRINGS.PREVIEW.SELECTED_SECTIONS_SUFFIX : STRINGS.PREVIEW.FULL_PAGE_LABEL}`}
        </button>
      </div>
    </div>
  );
}

