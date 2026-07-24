import React from 'react';
import { Download, RefreshCw, Layers } from 'lucide-react';
import { STRINGS } from '../constants/strings';
import { DATA_CONFIG } from '../constants/dataConfig';

export default function ResultsDashboard({ report, onNewScrape }) {
  const { title, summary, data } = report;
  const records = data.records || [];

  const allKeysSet = new Set();
  records.forEach(r => Object.keys(r).forEach(k => allKeysSet.add(k)));
  const standardOrder = DATA_CONFIG.STANDARD_COLUMN_ORDER;
  const displayKeys = Array.from(allKeysSet).sort((a, b) => {
      const idxA = standardOrder.indexOf(a);
      const idxB = standardOrder.indexOf(b);
      if (idxA !== -1 && idxB !== -1) return idxA - idxB;
      if (idxA !== -1) return -1;
      if (idxB !== -1) return 1;
      return a.localeCompare(b);
  });

  const downloadCSV = () => {
    if (records.length === 0) return;
    
    let csvContent = DATA_CONFIG.EXPORT.CSV_MIME_HEADER;
    csvContent += displayKeys.join(",") + "\n";

    records.forEach(item => {
      const row = displayKeys.map(k => {
        const val = item[k] || '';
        // Escape quotes by doubling them, wrap field in quotes
        return `"${String(val).replace(/"/g, '""')}"`;
      });
      csvContent += row.join(",") + "\n";
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", DATA_CONFIG.EXPORT.CSV_FILENAME);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const downloadJSON = () => {
    if (records.length === 0) return;
    const jsonStr = JSON.stringify(records, null, DATA_CONFIG.EXPORT.JSON_INDENT_SPACES);
    const dataStr = DATA_CONFIG.EXPORT.JSON_MIME_HEADER + encodeURIComponent(jsonStr);
    const link = document.createElement("a");
    link.setAttribute("href", dataStr);
    link.setAttribute("download", DATA_CONFIG.EXPORT.JSON_FILENAME);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="animate-fade-in">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 'var(--space-md)' }}>
        <div>
          <h2 style={{ fontSize: '2rem', marginBottom: '8px' }}>{STRINGS.RESULTS.HEADER_TITLE}</h2>
          <p style={{ color: 'var(--quantum-cyan)', fontSize: '1.1rem', fontWeight: 500 }}>{STRINGS.RESULTS.SOURCE_LABEL}{title}</p>
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button className="btn-secondary" onClick={onNewScrape} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <RefreshCw size={18} /> {STRINGS.RESULTS.BUTTON_NEW_SCRAPE}
          </button>
          <button className="btn-secondary" onClick={downloadJSON} style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--electric-teal)', borderColor: 'var(--electric-teal)' }}>
            <Download size={18} /> {STRINGS.RESULTS.BUTTON_JSON}
          </button>
          <button className="btn-primary" onClick={downloadCSV} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Download size={18} /> {STRINGS.RESULTS.BUTTON_EXPORT_CSV}
          </button>
        </div>
      </div>

      <div className="glass-card" style={{ marginBottom: 'var(--space-lg)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '16px 24px', borderBottom: '1px solid rgba(148, 163, 184, 0.2)' }}>
          <Layers color="var(--quantum-cyan)" size={24} />
          <h3 style={{ margin: 0 }}>{STRINGS.RESULTS.TABLE_CARD_TITLE} <span style={{ background: 'rgba(16, 185, 129, 0.2)', color: 'var(--electric-teal)', padding: '4px 12px', borderRadius: '12px', fontSize: '0.9rem', marginLeft: '12px' }}>{summary.total_records}{STRINGS.RESULTS.ITEMS_SUFFIX}</span></h3>
        </div>

        <div className="data-table-container">
          <table className="data-table">
            <thead>
              <tr>
                {displayKeys.map(k => (
                  <th key={k} style={{ textTransform: 'capitalize' }}>{k}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {records.length > 0 ? (
                records.map((item, i) => (
                  <tr key={i}>
                    {displayKeys.map(k => {
                      const val = item[k];
                      if (!val) return <td key={k} style={{ color: 'var(--muted-platinum)' }}>-</td>;
                      
                      if (DATA_CONFIG.HIGHLIGHT_COLUMNS.PRIMARY.includes(k)) return <td key={k} style={{ color: 'var(--electric-teal)', fontWeight: 500 }}>{val}</td>;
                      if (DATA_CONFIG.HIGHLIGHT_COLUMNS.BOLD.includes(k)) return <td key={k} style={{ color: 'var(--starlight-white)', fontWeight: 'bold' }}>{val}</td>;
                      if (DATA_CONFIG.HIGHLIGHT_COLUMNS.LINK.includes(k)) return <td key={k} style={{ maxWidth: '200px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}><a href={val} target="_blank" rel="noreferrer" style={{ color: 'var(--quantum-cyan)' }}>{val}</a></td>;
                      if (DATA_CONFIG.HIGHLIGHT_COLUMNS.TEXT_MUTED.includes(k)) return <td key={k} style={{ maxWidth: '200px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', color: 'var(--muted-platinum)' }}>{val}</td>;
                      
                      return (
                        <td key={k} style={{ fontSize: '0.9rem', lineHeight: '1.4', maxWidth: '300px' }}>
                          <div style={{ maxHeight: '100px', overflow: 'hidden', display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical' }}>
                            {val}
                          </div>
                        </td>
                      );
                    })}
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={displayKeys.length || 1} style={{ textAlign: 'center', padding: '32px', color: 'var(--muted-platinum)' }}>{STRINGS.RESULTS.NO_DATA}</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

