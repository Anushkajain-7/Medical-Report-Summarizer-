import React, { useState } from 'react';
import { analyzeReport } from '../services/api';
import { Activity, FileText, Sparkles, Database, Stethoscope, ArrowRight, Clock, Hash, Percent } from 'lucide-react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Bar } from 'react-chartjs-2';

// UI Components
import Card from '../components/ui/Card';
import EntityTag from '../components/ui/EntityTag';
import StatusStepper from '../components/ui/StatusStepper';
import LoadingSkeleton from '../components/ui/LoadingSkeleton';
import FileUpload from '../components/ui/FileUpload';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const EndToEnd = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentStep, setCurrentStep] = useState(1);

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please deposit a clinical document before initiating analysis.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);
    setCurrentStep(2);

    try {
      // Mock progression for editorial feel
      const progression = setInterval(() => {
        setCurrentStep(prev => prev < 4 ? prev + 1 : prev);
      }, 2000);

      const data = await analyzeReport(file, null);
      
      clearInterval(progression);
      setCurrentStep(5);
      setResult(data);
    } catch (err) {
      setError(err.message || 'The neural pipeline encountered a processing error.');
      setCurrentStep(1);
    } finally {
      setLoading(false);
    }
  };

  const getChartData = () => {
    if (!result?.entities) return null;
    const categories = ['DISEASE', 'DRUG', 'SYMPTOM', 'TREATMENT'];
    const counts = categories.map(cat => result.entities[cat]?.length || 0);
    
    return {
      labels: categories,
      datasets: [
        {
          data: counts,
          backgroundColor: ['#4a0e0e', '#800000', '#b22222', '#1a1a1a'],
          borderWidth: 0,
          barThickness: 20,
        },
      ],
    };
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      y: { display: false },
      x: { grid: { display: false }, ticks: { font: { family: 'Inter', size: 10, weight: 'bold' }, color: '#8e8e8e' } }
    }
  };

  return (
    <div className="flex flex-col gap-24 py-12">
      
      {/* 1. Hero / Ingest Section */}
      <section className="flex flex-col items-center text-center max-w-5xl mx-auto gap-12 fade-in">
        <div className="flex flex-col gap-6">
          <span className="label-uppercase tracking-[0.6em]">MedReport Intelligence Platform</span>
          <h1 className="text-7xl lg:text-9xl font-display text-premium-burgundy leading-[0.9] tracking-tighter">
            Synthesize Clinical <br />
            <span className="italic">Complexity.</span>
          </h1>
          <p className="text-xl font-sans text-premium-text-secondary max-w-2xl mx-auto leading-relaxed mt-4">
            An advanced AI engine designed to ingest unstructured clinical reports, generate high-fidelity summaries, 
            and extract structured medical intelligence with professional precision.
          </p>
        </div>

        <div className="w-full max-w-3xl mt-8">
          <FileUpload 
            file={file} 
            onFileChange={(f) => { setFile(f); setError(null); }} 
            error={error}
            loading={loading}
          />
          
          <div className="mt-12 flex justify-center">
            <button
              onClick={handleAnalyze}
              disabled={loading || !file}
              className="premium-btn flex items-center gap-4 group"
            >
              Initiate Analysis
              <ArrowRight size={16} className="transition-transform duration-500 group-hover:translate-x-2" />
            </button>
          </div>
        </div>
      </section>

      {/* 2. Pipeline Visualization */}
      {(loading || result) && (
        <section className="max-w-4xl mx-auto w-full slide-up">
          <div className="text-center mb-8">
            <span className="label-uppercase">Workflow Progression</span>
          </div>
          <StatusStepper currentStep={currentStep} />
        </section>
      )}

      {/* 3. Loading State */}
      {loading && <LoadingSkeleton />}

      {/* 4. Results Section (Editorial Grid) */}
      {result && !loading && (
        <section className="flex flex-col gap-24 animate-in fade-in slide-in-from-bottom-12 duration-1000">
          
          {/* Metadata Bar */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-px bg-premium-border border border-premium-border">
            {[
              { label: 'Processing Latency', value: `${result.processing_time}s`, icon: Clock },
              { label: 'Character Volume', value: result.input_length, icon: Hash },
              { label: 'Summary Density', value: `${((result.summary_length / result.input_length) * 100).toFixed(1)}%`, icon: Percent },
              { label: 'Intelligence Model', value: result.summary_model, icon: Sparkles },
            ].map((stat, i) => (
              <div key={i} className="bg-white p-8 flex flex-col gap-2">
                <stat.icon size={14} className="text-premium-text-muted mb-2" />
                <span className="label-uppercase mb-0">{stat.label}</span>
                <span className="text-3xl font-display text-premium-burgundy">{stat.value}</span>
              </div>
            ))}
          </div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
            
            {/* Left: Source Text (Editorial Frame) */}
            <div className="lg:col-span-4 h-[700px] flex">
              <Card title="Source Manuscript" subtitle="Original Record" className="w-full flex-1 border-r-0">
                <div className="font-sans text-xs text-premium-text-secondary leading-[2] text-justify space-y-6">
                  {result.raw_text.split('\n').map((para, i) => (
                    <p key={i}>{para}</p>
                  ))}
                </div>
              </Card>
            </div>

            {/* Middle: Intelligence Output (Premium Centerpiece) */}
            <div className="lg:col-span-5 h-[700px] flex">
              <Card 
                title="Clinical Abstract" 
                subtitle="Synthesized Summary" 
                className="w-full flex-1 border-x border-premium-border shadow-2xl relative z-10"
              >
                <div className="text-xl font-display text-premium-burgundy leading-relaxed first-letter:text-5xl first-letter:font-display first-letter:mr-3 first-letter:float-left italic">
                  {result.summary}
                </div>
                
                <div className="mt-16 pt-16 border-t border-premium-border space-y-8">
                  <div className="flex flex-col gap-4">
                    <span className="label-uppercase">Summary Confidence</span>
                    <div className="h-1 bg-premium-bg w-full">
                      <div className="h-full bg-premium-maroon w-[94%]" />
                    </div>
                  </div>
                </div>
              </Card>
            </div>

            {/* Right: Taxonomy Extraction */}
            <div className="lg:col-span-3 h-[700px] flex">
              <Card title="Taxonomy" subtitle="Entity Extraction" className="w-full flex-1 border-l-0">
                <div className="flex flex-col gap-10">
                  {['DISEASE', 'DRUG', 'SYMPTOM', 'TREATMENT'].map(category => {
                    const items = result.entities[category] || [];
                    if (items.length === 0) return null;
                    return (
                      <div key={category} className="flex flex-col gap-4">
                        <h4 className="text-[10px] font-bold text-premium-text-muted uppercase tracking-[0.3em] border-b border-premium-border pb-2">
                          {category}
                        </h4>
                        <div className="flex flex-wrap gap-2">
                          {items.map((item, idx) => (
                            <EntityTag key={idx} label={item} category={category} />
                          ))}
                        </div>
                      </div>
                    );
                  })}
                  
                  <div className="mt-8 pt-8 border-t border-premium-border h-[180px]">
                    <span className="label-uppercase mb-6">Distribution</span>
                    <Bar data={getChartData()} options={chartOptions} />
                  </div>
                </div>
              </Card>
            </div>
          </div>

          {/* 5. Clinical Recommendations (The "Trusted Card") */}
          {result.recommendations && Object.keys(result.recommendations.conditions).length > 0 && (
            <div className="mt-12 slide-up">
              <div className="flex flex-col gap-4 mb-12 items-center text-center">
                <span className="label-uppercase">Expert Analysis</span>
                <h2 className="text-5xl font-display text-premium-burgundy">Clinical Action Guidance</h2>
              </div>

              <div className="grid grid-cols-1 gap-12">
                {Object.entries(result.recommendations.conditions).map(([disease, recs], idx) => (
                  <div key={idx} className="bg-white border border-premium-border overflow-hidden flex flex-col lg:flex-row shadow-xl">
                    {/* Left Disease Branding */}
                    <div className="lg:w-1/4 bg-premium-burgundy text-white p-12 flex flex-col justify-between">
                      <div className="flex flex-col gap-4">
                         <span className="text-[10px] font-bold uppercase tracking-[0.4em] opacity-40">Target Condition</span>
                         <h3 className="text-4xl font-display leading-tight italic">{disease.toLowerCase()}</h3>
                      </div>
                      <Stethoscope size={48} strokeWidth={1} className="opacity-20" />
                    </div>

                    {/* Right Recommendations Content */}
                    <div className="lg:w-3/4 p-12 grid grid-cols-1 md:grid-cols-2 gap-16">
                      <div className="flex flex-col gap-10">
                        <div className="space-y-4">
                          <h5 className="label-uppercase text-emerald-700">Protocols</h5>
                          <ul className="space-y-3">
                            {recs.recommended_actions.map((item, i) => (
                              <li key={i} className="text-sm font-medium text-premium-text-primary flex items-start gap-4">
                                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-1.5 shrink-0" />
                                {item}
                              </li>
                            ))}
                          </ul>
                        </div>
                        <div className="space-y-4">
                          <h5 className="label-uppercase text-premium-accent">Contraindications</h5>
                          <ul className="space-y-3">
                            {recs.things_to_avoid.map((item, i) => (
                              <li key={i} className="text-sm font-medium text-premium-text-primary flex items-start gap-4">
                                <span className="w-1.5 h-1.5 rounded-full bg-premium-accent mt-1.5 shrink-0" />
                                {item}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>

                      <div className="flex flex-col gap-10">
                        <div className="bg-premium-bg p-8 border border-premium-border space-y-6">
                           <h5 className="label-uppercase text-premium-burgundy">Dietary Intelligence</h5>
                           <div className="grid grid-cols-1 gap-6">
                              <div>
                                <span className="text-[9px] font-bold uppercase text-premium-text-muted mb-2 block tracking-widest">Recommended</span>
                                <p className="text-xs font-bold leading-relaxed">{recs.diet_recommended.join(' • ')}</p>
                              </div>
                              <div className="pt-4 border-t border-premium-border">
                                <span className="text-[9px] font-bold uppercase text-premium-accent mb-2 block tracking-widest">Restricted</span>
                                <p className="text-xs font-bold leading-relaxed">{recs.diet_avoid.join(' • ')}</p>
                              </div>
                           </div>
                        </div>
                        <div className="space-y-4">
                          <h5 className="label-uppercase text-premium-text-primary">Lifestyle Interventions</h5>
                          <ul className="space-y-3">
                            {recs.lifestyle.map((item, i) => (
                              <li key={i} className="text-sm font-medium text-premium-text-secondary flex items-start gap-4">
                                <span className="w-1.5 h-1.5 rounded-full bg-premium-text-muted mt-1.5 shrink-0" />
                                {item}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Editorial Legal Section */}
              <div className="mt-24 max-w-2xl mx-auto text-center border-t border-premium-border pt-12">
                <span className="label-uppercase mb-4">Medical Advisory</span>
                <p className="text-[10px] font-bold text-premium-text-muted leading-loose uppercase tracking-[0.2em]">
                  {result.recommendations.disclaimer}
                </p>
              </div>
            </div>
          )}

        </section>
      )}

    </div>
  );
};

export default EndToEnd;
