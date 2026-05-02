import React from 'react';
import { Activity, Type, List, FileText, HeartPulse } from 'lucide-react';

const Sidebar = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: 'end2end', label: 'Clinical Dashboard', icon: Activity },
    { id: 'summarizer', label: 'Summarizer Module', icon: FileText },
    { id: 'ner', label: 'Entity Extraction', icon: List },
    { id: 'rouge', label: 'Metric Evaluator', icon: Type },
  ];

  return (
    <div className="fixed inset-y-0 left-0 w-64 bg-white border-r border-clinical-200 flex flex-col z-50 shadow-sm">
      <div className="p-6 border-b border-clinical-100 flex items-center gap-3">
        <div className="w-10 h-10 rounded-lg bg-clinical-accent flex items-center justify-center text-white shadow-sm">
          <HeartPulse size={24} strokeWidth={2.5} />
        </div>
        <div className="flex flex-col">
          <span className="text-lg font-bold text-clinical-800 tracking-tight leading-none">MedReport</span>
          <span className="text-xs font-semibold text-clinical-400 uppercase tracking-wider mt-1">AI System</span>
        </div>
      </div>

      <nav className="flex-1 p-4 flex flex-col gap-2">
        <div className="px-3 mb-2 text-xs font-semibold text-clinical-400 uppercase tracking-wider">
          Analysis Modules
        </div>
        {tabs.map(tab => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-3 px-4 py-3 rounded-md text-sm font-medium transition-all duration-200 w-full text-left
                ${isActive 
                  ? 'bg-clinical-50 text-clinical-accent border border-clinical-200 shadow-sm' 
                  : 'text-clinical-600 hover:bg-clinical-50 hover:text-clinical-800 border border-transparent'
                }
              `}
            >
              <Icon size={18} className={isActive ? 'text-clinical-accent' : 'text-clinical-400'} />
              {tab.label}
            </button>
          );
        })}
      </nav>
      
      <div className="p-6 border-t border-clinical-100">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-clinical-success"></div>
          <span className="text-xs font-medium text-clinical-500">System Online v2.1.0</span>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
