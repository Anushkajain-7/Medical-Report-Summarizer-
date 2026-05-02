import React, { useState } from 'react';
import { analyzeReport } from '../services/api';
import { Activity, FileText, FileCheck, List, Stethoscope, AlertCircle } from 'lucide-react';
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
  const [currentStep, setCurrentStep] = useState(1); // 1: Upload, 2: Summarizing, 3: NER, 4: Recommendations, 5: Done

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please upload a valid clinical document before analyzing.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);
    
    // Simulate staggered steps for UI feedback
    setCurrentStep(2);

    try {
      // In a real WebSocket implementation, we'd stream status. 
      // Here we just wait for the single HTTP call and mock the step progression.
      setTimeout(() => setCurrentStep(3), 1500);
      setTimeout(() => setCurrentStep(4), 3000);
      
      const data = await analyzeReport(file, null);
      
      setCurrentStep(5);
      setResult(data);
    } catch (err) {
      setError(err.message || 'An unexpected error occurred during processing.');
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
          label: 'Entities Detected',
          data: counts,
          backgroundColor: ['#ef4444', '#0ea5e9', '#f59e0b', '#10b981'],
          borderRadius: 4,
          barPercentage: 0.6
        },
      ],
    };
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      y: { beginAtZero: true, grid: { color: '#f1f5f9' }, ticks: { stepSize: 1, font: { family: 'Inter' } } },
      x: { grid: { display: false }, ticks: { font: { family: 'Inter', weight: '600' } } }
    }
  };

  return (
    <div className="flex flex-col gap-8 max-w-[1600px] mx-auto pb-12">
      
      {/* Header */}
      <div>
        <h1 className="text-3xl font-extrabold text-clinical-900 tracking-tight">Clinical Report Analysis</h1>
        <p className="text-clinical-500 mt-2 text-sm font-medium max-w-3xl leading-relaxed">
          Upload medical documentation to trigger the automated NLP pipeline. The system will generate an abstractive summary, 
          extract structured medical taxonomies, and provide condition-specific clinical guidance.
        </p>
      </div>

      {/* Upload & Controls Section */}
      <Card className="bg-white p-2">
        <div className="p-4 grid grid-cols-1 md:grid-cols-12 gap-8 items-center">
          
          {/* Left: Upload Zone */}
          <div className="md:col-span-8 lg:col-span-9">
            <FileUpload 
              file={file} 
              onFileChange={(f) => { setFile(f); setError(null); }} 
              error={error} 
            />
          </div>

          {/* Right: Actions */}
          <div className="md:col-span-4 lg:col-span-3 flex flex-col justify-center gap-4 border-t md:border-t-0 md:border-l border-clinical-100 pt-6 md:pt-0 md:pl-8 h-full">
            <div className="text-center md:text-left">
              <h3 className="font-bold text-clinical-800 mb-1">Ready to Process</h3>
              <p className="text-xs font-medium text-clinical-400 mb-6">Action requires pipeline execution.</p>
              
              <button
                onClick={handleAnalyze}
                disabled={loading || !file}
                className="w-full btn-primary py-3 flex justify-center items-center gap-2 text-sm"
              >
                <Activity size={18} className={loading ? "animate-pulse" : ""} />
                {loading ? 'Executing Pipeline...' : 'Run Analysis'}
              </button>
            </div>
          </div>

        </div>

        {/* Stepper (Only visible during loading or after completion) */}
        {(loading || result) && (
          <div className="px-8 py-6 border-t border-clinical-100 bg-clinical-50/50">
            <StatusStepper currentStep={currentStep} />
          </div>
        )}
      </Card>

      {/* Loading State */}
      {loading && <LoadingSkeleton />}

      {/* Results Dashboard */}
      {result && !loading && (
        <div className="flex flex-col gap-8 animate-in fade-in slide-in-from-bottom-4 duration-700 fill-mode-both">
          
          {/* Main 3-Column Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[600px]">
            
            {/* 1. Original Document */}
            <Card title="Source Document" icon={FileText} className="h-full">
              <div className="font-mono text-xs text-clinical-600 leading-relaxed whitespace-pre-wrap">
                {result.raw_text}
              </div>
            </Card>

            {/* 2. Abstractive Summary */}
            <Card 
              title="Generated Summary" 
              icon={FileCheck} 
              className="h-full ring-2 ring-clinical-accent/20"
              rightElement={
                <span className="bg-blue-50 text-clinical-accent text-[10px] font-bold px-2.5 py-1 rounded-full uppercase tracking-wider border border-blue-100">
                  {result.summary_model}
                </span>
              }
            >
              <div className="text-sm font-medium text-clinical-800 leading-loose">
                {result.summary}
              </div>
            </Card>

            {/* 3. Extracted Taxonomies */}
            <Card title="Structured Entities" icon={List} className="h-full">
              <div className="flex flex-col gap-6">
                {['DISEASE', 'DRUG', 'SYMPTOM', 'TREATMENT'].map(category => {
                  const items = result.entities[category] || [];
                  return (
                    <div key={category}>
                      <h4 className="text-xs font-bold text-clinical-400 uppercase tracking-widest mb-3 border-b border-clinical-100 pb-2">
                        {category} ({items.length})
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {items.length > 0 ? (
                          items.map((item, idx) => <EntityTag key={idx} label={item} category={category} />)
                        ) : (
                          <span className="text-xs font-medium text-clinical-300 italic">No entities detected</span>
                        )}
                      </div>
                    </div>
                  );
                })}
                
                {/* Chart */}
                <div className="mt-4 pt-6 border-t border-clinical-100 h-[180px]">
                  <Bar data={getChartData()} options={chartOptions} />
                </div>
              </div>
            </Card>
          </div>

          {/* Clinical Action Guidance Section */}
          {result.recommendations && Object.keys(result.recommendations.conditions).length > 0 && (
            <Card 
              title="Clinical Action Guidance" 
              icon={Stethoscope}
              className="border-t-4 border-t-clinical-accent"
            >
              <div className="flex flex-col gap-8 p-2">
                {Object.entries(result.recommendations.conditions).map(([disease, recs], idx) => (
                  <div key={idx} className="flex flex-col gap-5">
                    <h4 className="text-lg font-extrabold text-clinical-900 capitalize flex items-center gap-2">
                      <span className="w-2 h-6 bg-clinical-accent rounded-full inline-block"></span>
                      {disease.toLowerCase()}
                    </h4>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      
                      {/* Left: Actions & Precautions */}
                      <div className="flex flex-col gap-6">
                        {/* Recommended Actions */}
                        <div>
                          <h5 className="text-xs font-bold text-emerald-700 uppercase tracking-widest mb-3 flex items-center gap-2">
                            <div className="w-1.5 h-1.5 rounded-full bg-emerald-500"></div> Recommended Actions
                          </h5>
                          <ul className="space-y-2">
                            {recs.recommended_actions.map((item, i) => (
                              <li key={i} className="text-sm font-medium text-clinical-700 flex items-start gap-2">
                                <span className="text-emerald-500 mt-0.5">•</span> {item}
                              </li>
                            ))}
                          </ul>
                        </div>
                        
                        {/* Things to Avoid */}
                        <div>
                          <h5 className="text-xs font-bold text-red-700 uppercase tracking-widest mb-3 flex items-center gap-2">
                            <div className="w-1.5 h-1.5 rounded-full bg-red-500"></div> Things to Avoid
                          </h5>
                          <ul className="space-y-2">
                            {recs.things_to_avoid.map((item, i) => (
                              <li key={i} className="text-sm font-medium text-clinical-700 flex items-start gap-2">
                                <span className="text-red-500 mt-0.5">•</span> {item}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>

                      {/* Right: Diet & Lifestyle */}
                      <div className="flex flex-col gap-6">
                        {/* Diet */}
                        <div className="bg-blue-50/50 rounded-xl p-5 border border-blue-100">
                          <h5 className="text-xs font-bold text-blue-800 uppercase tracking-widest mb-4">Dietary Guidelines</h5>
                          <div className="grid grid-cols-2 gap-4">
                            <div>
                              <span className="text-[10px] font-bold text-blue-600 uppercase tracking-wider block mb-2">Encouraged</span>
                              <ul className="space-y-1">
                                {recs.diet_recommended.map((item, i) => (
                                  <li key={i} className="text-xs font-medium text-clinical-700 flex items-start gap-1.5">
                                    <span className="text-blue-400">+</span> {item}
                                  </li>
                                ))}
                              </ul>
                            </div>
                            <div>
                              <span className="text-[10px] font-bold text-red-600 uppercase tracking-wider block mb-2">Restricted</span>
                              <ul className="space-y-1">
                                {recs.diet_avoid.map((item, i) => (
                                  <li key={i} className="text-xs font-medium text-clinical-700 flex items-start gap-1.5">
                                    <span className="text-red-400">-</span> {item}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          </div>
                        </div>

                        {/* Lifestyle */}
                        <div>
                          <h5 className="text-xs font-bold text-clinical-600 uppercase tracking-widest mb-3 flex items-center gap-2">
                            <div className="w-1.5 h-1.5 rounded-full bg-clinical-400"></div> Lifestyle Interventions
                          </h5>
                          <ul className="space-y-2">
                            {recs.lifestyle.map((item, i) => (
                              <li key={i} className="text-sm font-medium text-clinical-700 flex items-start gap-2">
                                <span className="text-clinical-400 mt-0.5">•</span> {item}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                      
                    </div>
                  </div>
                ))}

                {/* Disclaimer */}
                <div className="mt-8 pt-6 border-t border-clinical-100 flex gap-3 items-start bg-amber-50/50 p-4 rounded-lg border-l-4 border-l-amber-400">
                  <AlertCircle size={18} className="text-amber-600 shrink-0 mt-0.5" />
                  <p className="text-xs font-medium text-amber-800 leading-relaxed">
                    {result.recommendations.disclaimer}
                  </p>
                </div>
              </div>
            </Card>
          )}

        </div>
      )}
    </div>
  );
};

export default EndToEnd;
