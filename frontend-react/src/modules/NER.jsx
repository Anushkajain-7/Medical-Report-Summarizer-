import React, { useState } from 'react';
import { extractEntities } from '../services/api';
import { List, Loader2, Search } from 'lucide-react';

const NER = () => {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleExtract = async () => {
    if (text.length < 10) {
      setError('Text is too short for NER extraction.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await extractEntities(text);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getEntityStyles = (type) => {
    switch(type) {
      case 'DISEASE': return { bg: 'rgba(244, 63, 94, 0.1)', color: 'var(--accent-rose)', border: 'rgba(244, 63, 94, 0.2)', icon: '' };
      case 'DRUG': return { bg: 'rgba(99, 102, 241, 0.1)', color: 'var(--accent-indigo)', border: 'rgba(99, 102, 241, 0.2)', icon: '' };
      case 'SYMPTOM': return { bg: 'rgba(245, 158, 11, 0.1)', color: 'var(--accent-amber)', border: 'rgba(245, 158, 11, 0.2)', icon: '' };
      case 'TREATMENT': return { bg: 'rgba(16, 185, 129, 0.1)', color: 'var(--accent-emerald)', border: 'rgba(16, 185, 129, 0.2)', icon: '' };
      default: return { bg: 'rgba(255, 255, 255, 0.1)', color: 'white', border: 'rgba(255, 255, 255, 0.2)', icon: '' };
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', maxWidth: '900px', margin: '0 auto' }}>
      <div>
        <h1 style={{ fontSize: '2rem', fontWeight: 800, marginBottom: '0.5rem' }}>Clinical <span className="gradient-text">NER</span></h1>
        <p style={{ color: 'var(--text-secondary)' }}>Extract medical entities (Diseases, Drugs, Symptoms, Treatments) using BERT.</p>
      </div>

      <div className="card" style={{ padding: '1.5rem' }}>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste medical text here to extract entities..."
          style={{
            width: '100%', minHeight: '150px', background: 'var(--bg-input)', border: '1px solid var(--border)',
            borderRadius: 'var(--radius-md)', padding: '1rem', color: 'var(--text-primary)', fontFamily: 'var(--font-mono)',
            fontSize: '0.85rem', resize: 'vertical', outline: 'none', transition: 'var(--transition)'
          }}
          onFocus={(e) => e.target.style.borderColor = 'var(--border-focus)'}
          onBlur={(e) => e.target.style.borderColor = 'var(--border)'}
        />

        {error && (
          <div style={{ marginTop: '1rem', padding: '1rem', background: 'rgba(244, 63, 94, 0.1)', color: 'var(--accent-rose)', borderRadius: 'var(--radius-sm)', fontSize: '0.85rem' }}>
            {error}
          </div>
        )}

        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1.5rem' }}>
          <button
            onClick={handleExtract}
            disabled={loading || !text}
            style={{
              background: 'var(--gradient-main)', color: 'white', padding: '10px 24px', borderRadius: 'var(--radius-sm)',
              fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px', opacity: loading || !text ? 0.6 : 1,
              cursor: loading || !text ? 'not-allowed' : 'pointer'
            }}
          >
            {loading ? <Loader2 size={18} style={{ animation: 'spin 1s linear infinite' }} /> : <Search size={18} />}
            {loading ? 'Extracting...' : 'Extract Entities'}
          </button>
        </div>
      </div>

      {result && result.entities && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem', animation: 'fadeInUp 0.4s ease' }}>
          {['DISEASE', 'DRUG', 'SYMPTOM', 'TREATMENT'].map(category => {
            const items = result.entities[category] || [];
            const style = getEntityStyles(category);
            
            return (
              <div key={category} className="card" style={{ padding: '1.25rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '1rem', borderBottom: `1px solid var(--border)`, paddingBottom: '0.75rem' }}>
                  {style.icon && <span style={{ fontSize: '1.2rem' }}>{style.icon}</span>}
                  <span style={{ fontWeight: 700, color: style.color, letterSpacing: '0.5px' }}>{category}</span>
                  <span style={{ marginLeft: 'auto', background: style.bg, color: style.color, padding: '2px 8px', borderRadius: '50px', fontSize: '0.75rem', fontWeight: 600 }}>
                    {items.length}
                  </span>
                </div>
                
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {items.length > 0 ? items.map((item, i) => (
                    <span key={i} style={{ 
                      background: style.bg, color: style.color, border: `1px solid ${style.border}`, 
                      padding: '4px 10px', borderRadius: '6px', fontSize: '0.8rem', fontWeight: 500 
                    }}>
                      {item}
                    </span>
                  )) : (
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontStyle: 'italic' }}>No entities found.</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default NER;
