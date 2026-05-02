import React from 'react';

const StatusStepper = ({ currentStep }) => {
  const steps = [
    { id: 1, label: 'Ingest' },
    { id: 2, label: 'Summarize' },
    { id: 3, label: 'Extract' },
    { id: 4, label: 'Guidance' }
  ];

  return (
    <div className="w-full py-8">
      <div className="flex items-center justify-between">
        {steps.map((step, index) => {
          const isCompleted = currentStep > step.id;
          const isCurrent = currentStep === step.id;
          
          return (
            <div key={step.id} className="flex flex-col items-center relative z-10 flex-1">
              <div 
                className={`w-6 h-6 flex items-center justify-center border transition-all duration-700 bg-white
                  ${isCompleted ? 'border-premium-burgundy bg-premium-burgundy text-white' : 
                    isCurrent ? 'border-premium-burgundy text-premium-burgundy scale-125' : 
                    'border-premium-border text-premium-border'}`}
              >
                {isCompleted ? (
                   <span className="text-[8px]">✓</span>
                ) : (
                   <span className="text-[10px] font-bold font-sans">{step.id}</span>
                )}
              </div>
              <span className={`label-uppercase mt-4 transition-colors duration-500
                ${isCompleted || isCurrent ? 'text-premium-burgundy' : 'text-premium-border'}`}>
                {step.label}
              </span>

              {index < steps.length - 1 && (
                <div className="absolute top-3 left-[50%] w-full h-[1px] -z-10">
                  <div className={`h-full transition-all duration-1000 ease-in-out
                    ${isCompleted ? 'bg-premium-burgundy w-full' : 'bg-premium-border w-0'}`} 
                  />
                  <div className="absolute inset-0 bg-premium-border -z-20" />
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default StatusStepper;
