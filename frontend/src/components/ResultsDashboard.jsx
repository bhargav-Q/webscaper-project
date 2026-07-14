import React, { useState } from 'react';
import { Download, RefreshCw, CheckCircle2, Link, FileText, Image as ImageIcon } from 'lucide-react';

export default function ResultsDashboard({ report, onNewScrape }) {
  const [activeTab, setActiveTab] = useState('headings');

  const { title, summary, data } = report;

  const downloadCSV = () => {
    // Basic CSV download logic for the currently active tab
    const items = data[activeTab];
    if (!items || items.length === 0) return;

    let csvContent = "data:text/csv;charset=utf-8,";
    
    // Header row
    const keys = typeof items[0] === 'string' ? ['value'] : Object.keys(items[0]);
    csvContent += keys.join(",") + "\n";

    // Data rows
    items.forEach(item => {
      if (typeof item === 'string') {
        csvContent += `"${item.replace(/"/g, '""')}"\n`;
      } else {
        const row = keys.map(k => `"${(item[k] || '').replace(/"/g, '""')}"`);
        csvContent += row.join(",") + "\n";
      }
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `quantana_${activeTab}_extract.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const tabs = [
    { id: 'headings', label: 'Headings', icon: <FileText size={16} />, count: summary.headings },
    { id: 'links', label: 'Links', icon: <Link size={16} />, count: summary.links },
    { id: 'images', label: 'Images', icon: <ImageIcon size={16} />, count: summary.images },
    { id: 'paragraphs', label: 'Paragraphs', icon: <FileText size={16} />, count: summary.paragraphs },
    { id: 'emails', label: 'Emails', icon: <CheckCircle2 size={16} />, count: summary.emails },
  ];

  return (
    <div className="animate-fade-in">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 'var(--space-md)' }}>
        <div>
          <h2 style={{ fontSize: '2rem', marginBottom: '8px' }}>Extraction Complete</h2>
          <p style={{ color: 'var(--quantum-cyan)', fontSize: '1.1rem', fontWeight: 500 }}>Source: {title}</p>
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button className="btn-secondary" onClick={onNewScrape} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <RefreshCw size={18} /> New Scrape
          </button>
          <button className="btn-primary" onClick={downloadCSV} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Download size={18} /> Export {activeTab.charAt(0).toUpperCase() + activeTab.slice(1)}
          </button>
        </div>
      </div>

      <div className="glass-card" style={{ marginBottom: 'var(--space-lg)' }}>
        {/* Tabs */}
        <div style={{ display: 'flex', borderBottom: '1px solid rgba(148, 163, 184, 0.2)', marginBottom: 'var(--space-md)' }}>
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                background: 'none',
                border: 'none',
                padding: '12px 24px',
                color: activeTab === tab.id ? 'var(--electric-teal)' : 'var(--muted-platinum)',
                borderBottom: activeTab === tab.id ? '2px solid var(--electric-teal)' : '2px solid transparent',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                fontFamily: 'var(--font-body)',
                fontWeight: activeTab === tab.id ? 600 : 400,
                transition: 'all 0.2s'
              }}
            >
              {tab.icon} {tab.label} <span style={{ background: activeTab === tab.id ? 'rgba(16, 185, 129, 0.2)' : 'rgba(148, 163, 184, 0.1)', padding: '2px 8px', borderRadius: '12px', fontSize: '0.8rem' }}>{tab.count}</span>
            </button>
          ))}
        </div>

        {/* Table Content */}
        <div className="data-table-container">
          <table className="data-table">
            <thead>
              <tr>
                {activeTab === 'headings' && (
                  <><th>Level</th><th>Text</th></>
                )}
                {activeTab === 'links' && (
                  <><th>Text</th><th>URL</th></>
                )}
                {activeTab === 'images' && (
                  <><th>Source</th><th>Alt Text</th></>
                )}
                {(activeTab === 'paragraphs' || activeTab === 'emails') && (
                  <th>Value</th>
                )}
              </tr>
            </thead>
            <tbody>
              {data[activeTab]?.length > 0 ? (
                data[activeTab].map((item, i) => (
                  <tr key={i}>
                    {activeTab === 'headings' && (
                      <><td style={{ width: '80px', color: 'var(--electric-teal)' }}>{item.level}</td><td>{item.text}</td></>
                    )}
                    {activeTab === 'links' && (
                      <><td style={{ maxWidth: '300px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{item.text}</td>
                      <td><a href={item.url} target="_blank" rel="noreferrer" style={{ color: 'var(--quantum-cyan)' }}>{item.url}</a></td></>
                    )}
                    {activeTab === 'images' && (
                      <><td style={{ maxWidth: '300px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{item.src}</td><td>{item.alt}</td></>
                    )}
                    {(activeTab === 'paragraphs' || activeTab === 'emails') && (
                      <td>{item}</td>
                    )}
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={2} style={{ textAlign: 'center', padding: '32px', color: 'var(--muted-platinum)' }}>No data extracted for this category.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
