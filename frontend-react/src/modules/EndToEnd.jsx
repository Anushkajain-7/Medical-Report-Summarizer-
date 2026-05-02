import React, { useState } from 'react';
import { analyzeReport } from '../services/api';
import { ArrowRight, Info, ShieldAlert, Utensils, Footprints, Pill, AlertCircle, FileText, CheckCircle2, ShieldCheck, Activity } from 'lucide-react';

// UI Components
import Card from '../components/ui/Card';
import EntityTag from '../components/ui/EntityTag';
import StatusStepper from '../components/ui/StatusStepper';
import LoadingSkeleton from '../components/ui/LoadingSkeleton';
import FileUpload from '../components/ui/FileUpload';

const EndToEnd = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentStep, setCurrentStep] = useState(1);

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please upload your medical report to begin.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);
    setCurrentStep(1);

    try {
      const progression = setInterval(() => {
        setCurrentStep(prev => prev < 4 ? prev + 1 : prev);
      }, 1500);

      const data = await analyzeReport(file, null);
      
      clearInterval(progression);
      setCurrentStep(5);
      setResult(data);
    } catch (err) {
      setError(err.message || 'The reasoning engine encountered an error processing your report.');
      setCurrentStep(1);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityStyles = (severity) => {
    switch (severity) {
      case 'CRITICAL': return 'bg-red-600 text-white border-red-700 shadow-[0_0_20px_rgba(220,38,38,0.4)]';
      case 'SERIOUS': return 'bg-premiumPrimary text-white border-premiumPrimary';
      case 'MODERATE': return 'bg-premiumBg text-premiumPrimary border-premiumNeutral';
      default: return 'bg-premiumBg text-premiumText-secondary border-premiumNeutral';
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'CRITICAL': return <ShieldAlert size={24} className="text-white animate-pulse" />;
      case 'SERIOUS': return <AlertCircle size={24} className="text-white" />;
      default: return <Activity size={24} className="text-premiumPrimary" />;
    }
  };

  return (
    <div className="flex flex-col gap-24 py-12">
      
      {/* 1. Hero / Ingest Section */}
      <section className="flex flex-col items-center text-center max-w-5xl mx-auto gap-12 fade-in">
        <div className="flex flex-col gap-6">
          <span className="label-uppercase tracking-[0.6em]">Clinical Reasoning v5.0</span>
          <h1 className="text-7xl lg:text-8xl font-display text-premiumPrimary leading-[0.9] tracking-tighter">
            Narrative-Aware <br />
            <span className="italic text-premiumAccent">Clinical Insights.</span>
          </h1>
          <p className="text-xl font-sans text-premiumText-secondary max-w-2xl mx-auto leading-relaxed mt-4">
            Our reasoning engine understands the clinical story within your report, 
            detecting severity, domain context, and critical medical events.
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
              className="premiumBtn flex items-center gap-4 group"
            >
              Analyze Clinical Narrative
              <ArrowRight size={16} className="transition-transform duration-500 group-hover:translate-x-2" />
            </button>
          </div>
        </div>
      </section>

      {/* 2. Reasoning Process */}
      {(loading || result) && (
        <section className="max-w-4xl mx-auto w-full slide-up">
          <div className="text-center mb-8">
            <span className="label-uppercase">Multi-Stage Reasoning Engine Active</span>
          </div>
          <StatusStepper currentStep={currentStep} />
        </section>
      )}

      {/* 3. Loading State */}
      {loading && <LoadingSkeleton />}

      {/* 4. Intelligence Results */}
      {result && !loading && (
        <section className="flex flex-col gap-20 animate-in fade-in slide-in-from-bottom-12 duration-1000">
          
          {/* Intelligence Header */}
          <div className="flex flex-col md:flex-row items-center justify-between gap-12 bg-white border border-premiumNeutral p-12 lg:p-16 shadow-2xl relative overflow-hidden">
             {/* Decorative Background Element */}
             <div className="absolute top-0 right-0 w-64 h-64 bg-premiumBg rounded-full -mr-32 -mt-32 -z-10" />
             
             <div className="flex flex-col gap-6 max-w-2xl">
                <div className="flex items-center gap-4">
                   <div className="px-4 py-1.5 bg-premiumPrimary text-white text-[10px] font-bold uppercase tracking-widest">
                     {result.meta.domain}
                   </div>
                   <div className={`px-4 py-1.5 border text-[10px] font-bold uppercase tracking-widest flex items-center gap-2 ${getSeverityStyles(result.clinical_intelligence.severity_level)}`}>
                     {getSeverityIcon(result.clinical_intelligence.severity_level)}
                     Severity: {result.clinical_intelligence.severity_level}
                   </div>
                </div>
                <h2 className="text-5xl lg:text-6xl font-display text-premiumPrimary leading-tight italic">
                  Understanding the Story
                </h2>
                <p className="text-xl font-sans text-premiumText-primary leading-relaxed italic border-l-4 border-premiumAccent pl-8">
                  "{result.clinical_intelligence.what_this_means}"
                </p>
             </div>

             <div className="flex flex-col gap-8 shrink-0 min-w-[280px]">
                <div className="p-8 bg-premiumBg border border-premiumNeutral">
                   <span className="label-uppercase text-premiumText-muted mb-4 block">Key Clinical Markers</span>
                   <div className="flex flex-col gap-3">
                      {result.clinical_intelligence.key_highlights.map((h, i) => (
                        <div key={i} className="flex items-center gap-3 text-xs font-bold text-premiumPrimary uppercase tracking-widest">
                           <div className="w-1 h-1 rounded-full bg-premiumAccent" />
                           {h}
                        </div>
                      ))}
                      {result.clinical_intelligence.key_highlights.length === 0 && (
                        <span className="text-[10px] italic text-premiumText-muted uppercase">No acute markers detected</span>
                      )}
                   </div>
                </div>
             </div>
          </div>

          {/* Detailed Context Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
            
            {/* Left Column: Care Plan & Guidance */}
            <div className="lg:col-span-8 flex flex-col gap-8">
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                 {/* What to Do */}
                 <Card title="Immediate Next Steps" subtitle="Care Action Plan" icon={CheckCircle2}>
                    <ul className="space-y-4">
                      {result.clinical_intelligence.care_plan.do.map((item, i) => (
                        <li key={i} className="text-sm font-medium text-premiumText-primary flex items-start gap-4">
                          <span className="w-1.5 h-1.5 rounded-full bg-premiumPrimary mt-1.5 shrink-0" />
                          {item}
                        </li>
                      ))}
                    </ul>
                 </Card>

                 {/* Nutrition */}
                 <Card title="Nutritional Strategy" subtitle="Condition-Specific Diet" icon={Utensils}>
                    <div className="bg-premiumBg p-8 border border-premiumNeutral">
                       <p className="text-sm font-bold text-premiumPrimary leading-relaxed">
                         {result.clinical_intelligence.care_plan.diet}
                       </p>
                    </div>
                    <div className="mt-8">
                       <span className="label-uppercase mb-4">Patient Note</span>
                       <p className="text-xs text-premiumText-secondary leading-relaxed uppercase tracking-widest">
                         Consult your clinical team before making major changes to your existing diet plan.
                       </p>
                    </div>
                 </Card>

                 {/* Precautions */}
                 <Card title="Risk Avoidance" subtitle="Safety Guidelines" icon={ShieldAlert}>
                    <ul className="space-y-4">
                      {result.clinical_intelligence.care_plan.avoid.map((item, i) => (
                        <li key={i} className="text-sm font-medium text-premiumText-primary flex items-start gap-4">
                          <span className="w-1.5 h-1.5 rounded-full bg-premiumAccent mt-1.5 shrink-0" />
                          {item}
                        </li>
                      ))}
                    </ul>
                 </Card>

                 {/* Warning Signs */}
                 <Card title="Red Flag Symptoms" subtitle="Emergency Monitor" icon={AlertCircle} className="border-premiumAccent/30 bg-premiumAccent/[0.02]">
                    <div className="flex flex-col gap-4">
                       {result.clinical_intelligence.care_plan.red_flags.map((flag, i) => (
                         <div key={i} className="flex items-center gap-4 p-4 bg-white border border-premiumNeutral text-xs font-bold text-premiumAccent uppercase tracking-widest">
                            <ShieldAlert size={14} className="shrink-0 animate-pulse" />
                            {flag}
                         </div>
                       ))}
                    </div>
                 </Card>
              </div>

              {/* Professional Abstract */}
              <Card title="Clinical Summary" subtitle="Technical Narrative Abstract" icon={FileText}>
                 <p className="text-sm font-medium text-premiumText-secondary leading-relaxed font-sans italic selection:bg-premiumPrimary selection:text-white">
                    {result.technical_summary}
                 </p>
              </Card>
            </div>

            {/* Right Column: Identified Findings & Meta */}
            <div className="lg:col-span-4 flex flex-col gap-8">
              
              <Card title="Identified Context" subtitle="Narrative Entities" icon={Pill} className="flex-1">
                <div className="flex flex-col gap-10">
                  {Object.entries(result.findings).map(([category, items]) => {
                    if (!items || items.length === 0) return null;
                    return (
                      <div key={category} className="flex flex-col gap-4">
                        <h4 className="label-uppercase border-b border-premiumNeutral pb-2">
                          {category}
                        </h4>
                        <div className="flex flex-wrap gap-2">
                          {items.map((item, idx) => (
                            <EntityTag key={idx} label={item} category={category.toUpperCase()} />
                          ))}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </Card>

              {/* Meta Stats */}
              <div className="bg-premiumDark p-10 text-white flex flex-col gap-6">
                 <div className="flex items-center gap-3">
                    <ShieldCheck size={18} className="text-emerald-500" />
                    <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-white/50">Intelligence Stats</span>
                 </div>
                 <div className="grid grid-cols-2 gap-8">
                    <div className="flex flex-col gap-1">
                       <span className="text-[8px] font-bold uppercase tracking-widest text-white/30">Latency</span>
                       <span className="text-xl font-display">{result.meta.processing_time}s</span>
                    </div>
                    <div className="flex flex-col gap-1">
                       <span className="text-[8px] font-bold uppercase tracking-widest text-white/30">Engine</span>
                       <span className="text-xl font-display leading-tight">{result.meta.engine.split(' ')[2]}</span>
                    </div>
                 </div>
              </div>

            </div>
          </div>

          {/* Safety Footer */}
          <div className="mt-12 max-w-4xl mx-auto text-center p-12 border-2 border-premiumNeutral border-dashed bg-white">
            <ShieldAlert size={32} className="mx-auto text-premiumAccent mb-6" />
            <p className="text-[10px] font-bold text-premiumText-muted leading-loose uppercase tracking-[0.3em]">
              {result.clinical_intelligence.disclaimer}
            </p>
          </div>

        </section>
      )}

    </div>
  );
};

export default EndToEnd;
