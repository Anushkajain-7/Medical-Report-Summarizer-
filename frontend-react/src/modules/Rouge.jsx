import React, { useState } from 'react';
import { computeRouge } from '../services/api';
import { Type, Loader2, BarChart2 } from 'lucide-react';

const Rouge = () => {
  const [reference, setReference] = useState('');
  const [hypothesis, setHypothesis] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleEvaluate = async () => {
    if (!reference || !hypothesis) {
      setError('Both Reference and Hypothesis texts are required.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await computeRouge(reference, hypothesis);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const renderMetric = (label, data) => (
    <div style={{ 
      background: 'rgba(245, 158, 11, 0.05)', border: '1px solid rgba(245, 158, 11, 0.15)', 
      borderRadius: 'var(--radius-md)', padding: '1.25rem', textAlign: 'center' 
    }}>
      <div style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--accent-amber)', marginBottom: '0.5rem', letterSpacing: '0.5px' }}>
        {label}
      </div>
      <div style={{ fontSize: '2rem', fontWeight: 800, fontFamily: 'var(--font-mono)', color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
        {data.f1.toFixed(3)}
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
        <span>P: {data.precision.toFixed(3)}</span>
        <span>R: {data.recall.toFixed(3)}</span>
      </div>
    </div>
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', maxWidth: '1000px', margin: '0 auto' }}>
      <div>
        <h1 style={{ fontSize: '2rem', fontWeight: 800, marginBottom: '0.5rem' }}>ROUGE <span className="gradient-text">Evaluator</span></h1>
        <p style={{ color: 'var(--text-secondary)' }}>Compare a generated summary (hypothesis) against an original text (reference).</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        <div className="card" style={{ padding: '1.5rem' }}>
          <div style={{ fontWeight: 600, marginBottom: '1rem', color: 'var(--text-primary)' }}>Reference Text (Original)</div>
          <textarea
            value={reference}
            onChange={(e) => setReference(e.target.value)}
            placeholder="Paste original text here..."
            style={{
              width: '100%', minHeight: '200px', background: 'var(--bg-input)', border: '1px solid var(--border)',
              borderRadius: 'var(--radius-md)', padding: '1rem', color: 'var(--text-primary)', fontFamily: 'var(--font-mono)',
              fontSize: '0.85rem', resize: 'vertical', outline: 'none'
            }}
          />
        </div>

        <div className="card" style={{ padding: '1.5rem' }}>
          <div style={{ fontWeight: 600, marginBottom: '1rem', color: 'var(--accent-cyan)' }}>Hypothesis Text (Summary)</div>
          <textarea
            value={hypothesis}
            onChange={(e) => setHypothesis(e.target.value)}
            placeholder="Paste generated summary here..."
            style={{
              width: '100%', minHeight: '200px', background: 'var(--bg-input)', border: '1px solid rgba(6, 182, 212, 0.3)',
              borderRadius: 'var(--radius-md)', padding: '1rem', color: 'var(--text-primary)', fontFamily: 'var(--font-mono)',
              fontSize: '0.85rem', resize: 'vertical', outline: 'none'
            }}
          />
        </div>
      </div>

      {error && (
        <div style={{ padding: '1rem', background: 'rgba(244, 63, 94, 0.1)', color: 'var(--accent-rose)', borderRadius: 'var(--radius-sm)' }}>
          {error}
        </div>
      )}

      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <button
          onClick={handleEvaluate}
          disabled={loading || !reference || !hypothesis}
          style={{
            background: 'var(--gradient-main)', color: 'white', padding: '12px 32px', borderRadius: 'var(--radius-sm)',
            fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px', opacity: loading || !reference || !hypothesis ? 0.6 : 1,
            cursor: loading || !reference || !hypothesis ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? <Loader2 size={18} style={{ animation: 'spin 1s linear infinite' }} /> : <BarChart2 size={18} />}
          {loading ? 'Evaluating...' : 'Compute ROUGE Scores'}
        </button>
      </div>

      {result && result.scores && (
        <div className="card" style={{ padding: '2rem', animation: 'fadeInUp 0.4s ease', marginTop: '1rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem' }}>
            {renderMetric('ROUGE-1', result.scores.rouge1)}
            {renderMetric('ROUGE-2', result.scores.rouge2)}
            {renderMetric('ROUGE-L', result.scores.rougeL)}
          </div>
        </div>
      )}
    </div>
  );
};

export default Rouge;
