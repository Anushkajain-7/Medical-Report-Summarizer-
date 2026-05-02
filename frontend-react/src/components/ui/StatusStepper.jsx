import React from 'react';
import { Check, CircleDot, Circle } from 'lucide-react';

const StatusStepper = ({ currentStep }) => {
  const steps = [
    { id: 1, label: 'Document Upload' },
    { id: 2, label: 'Abstractive Summarization' },
    { id: 3, label: 'Entity Extraction' },
    { id: 4, label: 'Clinical Recommendations' }
  ];

  return (
    <div className="w-full py-4">
      <div className="flex items-center justify-between">
        {steps.map((step, index) => {
          const isCompleted = currentStep > step.id;
          const isCurrent = currentStep === step.id;
          
          return (
            <div key={step.id} className="flex flex-col items-center relative z-10 flex-1">
              <div 
                className={`w-8 h-8 rounded-full flex items-center justify-center border-2 transition-all duration-300 bg-white
                  ${isCompleted ? 'border-clinical-success text-clinical-success' : 
                    isCurrent ? 'border-clinical-accent text-clinical-accent ring-4 ring-clinical-100' : 
                    'border-clinical-200 text-clinical-300'}`}
              >
                {isCompleted ? <Check size={16} strokeWidth={3} /> : 
                 isCurrent ? <CircleDot size={16} strokeWidth={2.5} /> : 
                 <span className="text-xs font-bold">{step.id}</span>}
              </div>
              <span className={`text-[10px] font-bold uppercase tracking-wider mt-3 text-center transition-colors
                ${isCompleted || isCurrent ? 'text-clinical-800' : 'text-clinical-400'}`}>
                {step.label}
              </span>

              {/* Connecting Line */}
              {index < steps.length - 1 && (
                <div className={`absolute top-4 left-[50%] w-full h-[2px] -z-10 transition-all duration-500
                  ${isCompleted ? 'bg-clinical-success' : 'bg-clinical-200'}`} 
                />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default StatusStepper;
