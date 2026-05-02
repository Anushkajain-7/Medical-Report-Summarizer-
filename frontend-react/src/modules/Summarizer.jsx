import React, { useState } from 'react';
import { summarizeText } from '../services/api';
import { FileText, Loader2, Copy } from 'lucide-react';

const Summarizer = () => {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);

  const handleSummarize = async () => {
    if (text.length < 50) {
      setError('Text is too short for summarization (minimum 50 characters).');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await summarizeText(text);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (result?.summary) {
      navigator.clipboard.writeText(result.summary);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', maxWidth: '900px', margin: '0 auto' }}>
      <div>
        <h1 style={{ fontSize: '2rem', fontWeight: 800, marginBottom: '0.5rem' }}>Abstractive <span className="gradient-text">Summarizer</span></h1>
        <p style={{ color: 'var(--text-secondary)' }}>Test the BART-based summarization pipeline directly by providing raw medical text.</p>
      </div>

      <div className="card" style={{ padding: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 600 }}>
            <FileText size={18} color="var(--accent-indigo)" />
            Input Text
          </div>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{text.length} characters</span>
        </div>
        
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste medical text here..."
          style={{
            width: '100%', minHeight: '200px', background: 'var(--bg-input)', border: '1px solid var(--border)',
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
            onClick={handleSummarize}
            disabled={loading || !text}
            style={{
              background: 'var(--gradient-main)', color: 'white', padding: '10px 24px', borderRadius: 'var(--radius-sm)',
              fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px', opacity: loading || !text ? 0.6 : 1,
              cursor: loading || !text ? 'not-allowed' : 'pointer', transition: 'var(--transition)'
            }}
          >
            {loading ? <Loader2 size={18} style={{ animation: 'spin 1s linear infinite' }} /> : <FileText size={18} />}
            {loading ? 'Summarizing...' : 'Summarize Text'}
          </button>
        </div>
      </div>

      {result && (
        <div className="card" style={{ padding: '1.5rem', animation: 'fadeInUp 0.4s ease' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border)', paddingBottom: '1rem', marginBottom: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 600 }}>
              <div style={{ padding: '6px 12px', background: 'rgba(99, 102, 241, 0.1)', color: 'var(--accent-indigo)', borderRadius: '50px', fontSize: '0.75rem' }}>
                {result.model || 'BART'}
              </div>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Status: {result.status || 'Success'}</span>
            </div>
            
            <button
              onClick={handleCopy}
              style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem', color: 'var(--accent-cyan)', padding: '6px 12px', background: 'rgba(6, 182, 212, 0.1)', borderRadius: 'var(--radius-sm)' }}
            >
              <Copy size={14} />
              {copied ? 'Copied!' : 'Copy Summary'}
            </button>
          </div>
          
          <div style={{ fontSize: '0.95rem', lineHeight: 1.8, color: 'var(--text-primary)' }}>
            {result.summary}
          </div>
        </div>
      )}
    </div>
  );
};

export default Summarizer;
