import React, { useState } from 'react';
import { summarizeText } from '../services/api';
import { FileText, Copy, Sparkles, Loader2 } from 'lucide-react';
import Card from '../components/ui/Card';

const Summarizer = () => {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);

  const handleSummarize = async () => {
    if (text.length < 50) {
      setError('Neural pipeline requires at least 50 characters for meaningful synthesis.');
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
    <div className="flex flex-col gap-16 max-w-4xl mx-auto py-12 fade-in">
      <div className="text-center space-y-6">
        <span className="label-uppercase tracking-[0.5em]">Direct Access Node</span>
        <h1 className="text-6xl font-display text-premium-burgundy italic">Abstractive Summarizer</h1>
        <p className="text-premium-text-secondary font-medium uppercase tracking-widest text-[10px]">
          Direct interface for the BART-large-CNN neural architecture.
        </p>
      </div>

      <Card title="Input Manuscript" subtitle="Direct Entry">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste medical text for direct synthesis..."
          className="w-full min-h-[300px] bg-premium-bg border border-premium-border p-8 text-sm font-sans text-premium-text-primary focus:outline-none focus:border-premium-burgundy transition-all duration-500 leading-relaxed resize-none"
        />
        
        {error && (
          <div className="mt-6 p-4 border border-premium-accent bg-premium-accent/5 text-premium-accent text-[10px] font-bold uppercase tracking-widest flex items-center gap-3">
             <span className="w-1.5 h-1.5 rounded-full bg-premium-accent" />
             {error}
          </div>
        )}

        <div className="flex justify-between items-center mt-8">
           <span className="label-uppercase mb-0">{text.length} Characters Detected</span>
           <button
            onClick={handleSummarize}
            disabled={loading || !text}
            className="premium-btn flex items-center gap-3"
          >
            {loading ? <Loader2 size={16} className="animate-spin" /> : <Sparkles size={16} />}
            {loading ? 'Synthesizing...' : 'Run Summarization'}
          </button>
        </div>
      </Card>

      {result && (
        <Card 
          title="Synthesized Abstract" 
          subtitle="Model Output" 
          className="slide-up shadow-2xl"
          rightElement={
            <button
              onClick={handleCopy}
              className="text-[10px] font-bold uppercase tracking-widest text-premium-burgundy border-b border-premium-burgundy pb-1 hover:text-premium-maroon transition-colors"
            >
              {copied ? 'Copied' : 'Copy Abstract'}
            </button>
          }
        >
          <div className="text-lg font-display text-premium-burgundy leading-relaxed italic">
            {result.summary}
          </div>
          <div className="mt-8 pt-8 border-t border-premium-border flex justify-between items-center">
             <span className="label-uppercase mb-0">Model Instance: {result.model || 'BART-CNN'}</span>
             <span className="label-uppercase mb-0">Status: {result.status || 'Verified'}</span>
          </div>
        </Card>
      )}
    </div>
  );
};

export default Summarizer;
