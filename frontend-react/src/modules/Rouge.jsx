import React, { useState } from 'react';
import { computeRouge } from '../services/api';
import { BarChart2, Loader2, FileText, Sparkles } from 'lucide-react';
import Card from '../components/ui/Card';

const Rouge = () => {
  const [reference, setReference] = useState('');
  const [hypothesis, setHypothesis] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleEvaluate = async () => {
    if (!reference || !hypothesis) {
      setError('Neural evaluation requires both Reference and Hypothesis manuscripts.');
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
    <div className="flex flex-col items-center gap-4 bg-premiumBg p-8 border border-premiumNeutral">
      <span className="label-uppercase mb-0 tracking-[0.4em] text-premiumPrimary">{label}</span>
      <div className="text-5xl font-display text-premiumPrimary italic">
        {data.f1.toFixed(3)}
      </div>
      <div className="flex gap-6 pt-4 border-t border-premiumNeutral w-full justify-center">
        <div className="flex flex-col items-center">
           <span className="text-[8px] font-bold text-premiumText-muted uppercase tracking-widest">Prec</span>
           <span className="text-[10px] font-bold">{data.precision.toFixed(3)}</span>
        </div>
        <div className="flex flex-col items-center">
           <span className="text-[8px] font-bold text-premiumText-muted uppercase tracking-widest">Rec</span>
           <span className="text-[10px] font-bold">{data.recall.toFixed(3)}</span>
        </div>
      </div>
    </div>
  );

  return (
    <div className="flex flex-col gap-16 max-w-6xl mx-auto py-12 fade-in">
      <div className="text-center space-y-6">
        <span className="label-uppercase tracking-[0.5em]">Linguistic Evaluation</span>
        <h1 className="text-6xl font-display text-premiumPrimary italic">ROUGE Metrics</h1>
        <p className="text-premiumText-secondary font-medium uppercase tracking-widest text-[10px]">
          Computational comparison of generated abstracts against reference ground-truth.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card title="Reference Manuscript" subtitle="Ground Truth">
          <textarea
            value={reference}
            onChange={(e) => setReference(e.target.value)}
            placeholder="Deposit original clinical text..."
            className="w-full min-h-[250px] bg-premiumBg border border-premiumNeutral p-8 text-sm font-sans text-premiumText-primary focus:outline-none focus:border-premiumPrimary transition-all duration-500 leading-relaxed resize-none"
          />
        </Card>

        <Card title="Hypothesis Manuscript" subtitle="Model Output">
          <textarea
            value={hypothesis}
            onChange={(e) => setHypothesis(e.target.value)}
            placeholder="Deposit generated summary text..."
            className="w-full min-h-[250px] bg-premiumBg border border-premiumAccent/20 p-8 text-sm font-sans text-premiumText-primary focus:outline-none focus:border-premiumPrimary transition-all duration-500 leading-relaxed resize-none"
          />
        </Card>
      </div>

      {error && (
        <div className="p-4 border border-premiumAccent bg-premiumAccent/5 text-premiumAccent text-[10px] font-bold uppercase tracking-widest flex items-center gap-3 max-w-md mx-auto">
           <span className="w-1.5 h-1.5 rounded-full bg-premiumAccent" />
           {error}
        </div>
      )}

      <div className="flex justify-center">
        <button
          onClick={handleEvaluate}
          disabled={loading || !reference || !hypothesis}
          className="premiumBtn flex items-center gap-4"
        >
          {loading ? <Loader2 size={16} className="animate-spin" /> : <BarChart2 size={16} />}
          {loading ? 'Evaluating...' : 'Compute Evaluation Metrics'}
        </button>
      </div>

      {result && result.scores && (
        <div className="slide-up">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
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
