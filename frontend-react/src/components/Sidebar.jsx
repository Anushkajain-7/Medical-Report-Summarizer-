import React from 'react';
import { LayoutDashboard, FileScan, Braces, LineChart, ShieldCheck } from 'lucide-react';

const Sidebar = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: 'end2end', label: 'Intelligence', icon: LayoutDashboard },
    { id: 'summarizer', label: 'Summarizer', icon: FileScan },
    { id: 'ner', label: 'Extraction', icon: Braces },
    { id: 'rouge', label: 'Metrics', icon: LineChart },
  ];

  return (
    <div className="fixed inset-y-0 left-0 w-72 bg-premium-dark text-white hidden lg:flex flex-col z-50 overflow-hidden">
      {/* Brand Section */}
      <div className="p-12 pb-24">
        <div className="flex flex-col gap-2">
          <h1 className="text-4xl font-display font-medium tracking-tight">MedReport</h1>
          <span className="text-[10px] font-bold uppercase tracking-[0.5em] text-white/40">AI Platform</span>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-8 flex flex-col gap-12">
        <div className="flex flex-col gap-4">
          <span className="label-uppercase text-white/30 px-4">Navigation</span>
          <div className="flex flex-col gap-1">
            {tabs.map(tab => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-4 px-4 py-4 transition-all duration-500 group relative
                    ${isActive ? 'text-white' : 'text-white/40 hover:text-white'}
                  `}
                >
                  {isActive && (
                    <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-premium-maroon" />
                  )}
                  <Icon size={18} strokeWidth={isActive ? 2.5 : 1.5} className="transition-transform duration-500 group-hover:scale-110" />
                  <span className="text-xs font-bold uppercase tracking-widest">{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        <div className="flex flex-col gap-4">
          <span className="label-uppercase text-white/30 px-4">Deployment</span>
          <div className="px-4 py-6 bg-white/5 border border-white/10">
            <div className="flex items-center gap-3 mb-4">
              <ShieldCheck size={16} className="text-premium-accent" />
              <span className="text-[10px] font-bold uppercase tracking-widest">Secure Instance</span>
            </div>
            <p className="text-[10px] text-white/40 leading-relaxed uppercase tracking-wider">
              Local containerized node active. All processing is HIPAA compliant.
            </p>
          </div>
        </div>
      </nav>
      
      {/* Footer Branding */}
      <div className="p-12 border-t border-white/5">
        <div className="flex items-center gap-3">
          <div className="w-2 h-2 rounded-full bg-premium-accent animate-pulse" />
          <span className="text-[10px] font-bold uppercase tracking-widest text-white/40">Build v2.4.1</span>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
