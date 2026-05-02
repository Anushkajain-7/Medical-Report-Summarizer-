import React, { useState } from 'react';
import { analyzeReport } from '../services/api';
import { ArrowRight, Info, ShieldAlert, Utensils, Footprints, Pill, AlertCircle, FileText, CheckCircle2 } from 'lucide-react';

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
      // Simulate pipeline progression
      const progression = setInterval(() => {
        setCurrentStep(prev => prev < 4 ? prev + 1 : prev);
      }, 1200);

      const data = await analyzeReport(file, null);
      
      clearInterval(progression);
      setCurrentStep(5);
      setResult(data);
    } catch (err) {
      setError(err.message || 'The assistant encountered an error processing your report.');
      setCurrentStep(1);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-24 py-12">
      
      {/* 1. Hero / Ingest Section */}
      <section className="flex flex-col items-center text-center max-w-5xl mx-auto gap-12 fade-in">
        <div className="flex flex-col gap-6">
          <span className="label-uppercase tracking-[0.6em]">Proactive Health Assistant</span>
          <h1 className="text-7xl lg:text-8xl font-display text-premiumPrimary leading-[0.9] tracking-tighter">
            Decode Your <br />
            <span className="italic text-premiumAccent">Medical Story.</span>
          </h1>
          <p className="text-xl font-sans text-premiumText-secondary max-w-2xl mx-auto leading-relaxed mt-4">
            Transform complex clinical reports into a clear, understandable plan. 
            Analyze labs, symptoms, and findings to understand what comes next.
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
              Understand My Report
              <ArrowRight size={16} className="transition-transform duration-500 group-hover:translate-x-2" />
            </button>
          </div>
        </div>
      </section>

      {/* 2. Assistant Status */}
      {(loading || result) && (
        <section className="max-w-4xl mx-auto w-full slide-up">
          <div className="text-center mb-8">
            <span className="label-uppercase">Inference Pipeline Active</span>
          </div>
          <StatusStepper currentStep={currentStep} />
        </section>
      )}

      {/* 3. Loading State */}
      {loading && <LoadingSkeleton />}

      {/* 4. Interpretation Results */}
      {result && !loading && (
        <section className="flex flex-col gap-20 animate-in fade-in slide-in-from-bottom-12 duration-1000">
          
          {/* Main Interpretation Header */}
          <div className="flex flex-col items-center text-center gap-4">
             <span className="label-uppercase">Primary Clinical Pattern Identified</span>
             <h2 className="text-5xl lg:text-7xl font-display text-premiumPrimary italic">
               {result.interpretation.status_label}
             </h2>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
            
            {/* Left: Interpretation & Care Plan */}
            <div className="lg:col-span-8 flex flex-col gap-8">
              
              {/* Understanding Section */}
              <Card 
                title="What This Suggests" 
                subtitle="Patient-Centric Interpretation" 
                className="shadow-2xl border-premiumAccent/10"
                icon={Info}
              >
                <div className="text-2xl font-display text-premiumPrimary leading-relaxed mb-8 border-l-4 border-premiumAccent pl-8 italic">
                  "{result.interpretation.simple_explanation}"
                </div>
                
                <div className="mt-12 space-y-6">
                   <h5 className="label-uppercase">Critical Indicators to Monitor (Red Flags)</h5>
                   <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {result.interpretation.red_flags.map((flag, i) => (
                        <div key={i} className="flex items-center gap-3 p-4 bg-premiumAccent/5 border border-premiumAccent/10 text-xs font-bold text-premiumPrimary uppercase tracking-wide">
                           <AlertCircle size={14} className="text-premiumAccent" />
                           {flag}
                        </div>
                      ))}
                   </div>
                </div>
              </Card>

              {/* Comprehensive Care Plan */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                 {/* What to Do */}
                 <Card title="Immediate Actions" subtitle="Next Steps" icon={CheckCircle2}>
                    <ul className="space-y-4">
                      {result.interpretation.care_plan.do.map((item, i) => (
                        <li key={i} className="text-sm font-medium text-premiumText-primary flex items-start gap-4">
                          <span className="w-1.5 h-1.5 rounded-full bg-premiumPrimary mt-1.5 shrink-0" />
                          {item}
                        </li>
                      ))}
                    </ul>
                 </Card>

                 {/* Nutrition */}
                 <Card title="Nutritional Guidance" subtitle="Food Intelligence" icon={Utensils}>
                    <div className="space-y-6">
                       <div>
                          <span className="text-[9px] font-bold uppercase text-emerald-700 mb-2 block tracking-widest">Helpful Choices</span>
                          <p className="text-xs font-bold leading-relaxed">{result.interpretation.care_plan.diet_recommended.join(' • ')}</p>
                       </div>
                       <div className="pt-4 border-t border-premiumNeutral">
                          <span className="text-[9px] font-bold uppercase text-premiumAccent mb-2 block tracking-widest">Suggested Limits</span>
                          <p className="text-xs font-bold leading-relaxed">{result.interpretation.care_plan.diet_restricted.join(' • ')}</p>
                       </div>
                    </div>
                 </Card>

                 {/* Avoid */}
                 <Card title="Precautions" subtitle="What to Avoid" icon={ShieldAlert}>
                    <ul className="space-y-4">
                      {result.interpretation.care_plan.avoid.map((item, i) => (
                        <li key={i} className="text-sm font-medium text-premiumText-primary flex items-start gap-4">
                          <span className="w-1.5 h-1.5 rounded-full bg-premiumAccent mt-1.5 shrink-0" />
                          {item}
                        </li>
                      ))}
                    </ul>
                 </Card>

                 {/* Lifestyle */}
                 <Card title="Daily Habits" subtitle="Lifestyle Support" icon={Footprints}>
                    <ul className="space-y-4">
                      {result.interpretation.care_plan.lifestyle.map((item, i) => (
                        <li key={i} className="text-sm font-medium text-premiumText-secondary flex items-start gap-4">
                          <span className="w-1.5 h-1.5 rounded-full bg-premiumNeutral mt-1.5 shrink-0" />
                          {item}
                        </li>
                      ))}
                    </ul>
                 </Card>
              </div>
            </div>

            {/* Right: Detected Context & Professional Summary */}
            <div className="lg:col-span-4 flex flex-col gap-8">
              
              {/* Professional Abstract */}
              <Card title="Clinical Summary" subtitle="For Medical Review" icon={FileText}>
                 <p className="text-xs font-medium text-premiumText-secondary leading-relaxed font-sans italic">
                    "{result.technical_summary}"
                 </p>
              </Card>

              {/* Identified Findings */}
              <Card title="Identified Context" subtitle="Detected Information" icon={Pill} className="flex-1">
                <div className="flex flex-col gap-8">
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

            </div>
          </div>

          {/* Safety Footer */}
          <div className="mt-12 max-w-4xl mx-auto text-center p-12 border-2 border-premiumNeutral border-dashed">
            <ShieldAlert size={32} className="mx-auto text-premiumAccent mb-6" />
            <p className="text-[10px] font-bold text-premiumText-muted leading-loose uppercase tracking-[0.25em]">
              {result.interpretation.disclaimer}
            </p>
          </div>

        </section>
      )}

    </div>
  );
};

export default EndToEnd;
