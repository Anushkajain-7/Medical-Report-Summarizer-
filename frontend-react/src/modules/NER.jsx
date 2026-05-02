import React, { useState } from 'react';
import { extractEntities } from '../services/api';
import { Search, Loader2, Database } from 'lucide-react';
import Card from '../components/ui/Card';
import EntityTag from '../components/ui/EntityTag';

const NER = () => {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleExtract = async () => {
    if (text.length < 10) {
      setError('Insufficient data volume for entity extraction.');
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

  return (
    <div className="flex flex-col gap-16 max-w-5xl mx-auto py-12 fade-in">
      <div className="text-center space-y-6">
        <span className="label-uppercase tracking-[0.5em]">Linguistic Analysis</span>
        <h1 className="text-6xl font-display text-premium-burgundy italic">Clinical Extraction</h1>
        <p className="text-premium-text-secondary font-medium uppercase tracking-widest text-[10px]">
          Structured medical entity identification using BioClinicalBERT architectures.
        </p>
      </div>

      <Card title="Source Protocol" subtitle="Direct Entry">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste medical text for taxonomy extraction..."
          className="w-full min-h-[200px] bg-premium-bg border border-premium-border p-8 text-sm font-sans text-premium-text-primary focus:outline-none focus:border-premium-burgundy transition-all duration-500 leading-relaxed resize-none"
        />
        
        {error && (
          <div className="mt-6 p-4 border border-premium-accent bg-premium-accent/5 text-premium-accent text-[10px] font-bold uppercase tracking-widest flex items-center gap-3">
             <span className="w-1.5 h-1.5 rounded-full bg-premium-accent" />
             {error}
          </div>
        )}

        <div className="flex justify-end mt-8">
           <button
            onClick={handleExtract}
            disabled={loading || !text}
            className="premium-btn flex items-center gap-3"
          >
            {loading ? <Loader2 size={16} className="animate-spin" /> : <Search size={16} />}
            {loading ? 'Analyzing...' : 'Run Extraction'}
          </button>
        </div>
      </Card>

      {result && result.entities && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 slide-up">
          {['DISEASE', 'DRUG', 'SYMPTOM', 'TREATMENT'].map(category => {
            const items = result.entities[category] || [];
            return (
              <Card key={category} title={category} subtitle="Taxonomy Category">
                <div className="flex flex-wrap gap-3">
                  {items.length > 0 ? items.map((item, i) => (
                    <EntityTag key={i} label={item} category={category} />
                  )) : (
                    <span className="text-[10px] font-bold uppercase tracking-widest text-premium-text-muted italic">No instances detected</span>
                  )}
                </div>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default NER;
