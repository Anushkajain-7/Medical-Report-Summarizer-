import { useState } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import EndToEnd from './modules/EndToEnd';
import Summarizer from './modules/Summarizer';
import NER from './modules/NER';
import Rouge from './modules/Rouge';

function App() {
  const [activeTab, setActiveTab] = useState('end2end');

  const renderModule = () => {
    switch (activeTab) {
      case 'end2end': return <EndToEnd />;
      case 'summarizer': return <Summarizer />;
      case 'ner': return <NER />;
      case 'rouge': return <Rouge />;
      default: return <EndToEnd />;
    }
  };

  return (
    <div className="flex min-h-screen w-full bg-premium-bg text-premium-text-primary selection:bg-premium-burgundy selection:text-white">
      {/* Editorial Sidebar */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Perspective Content */}
      <div className="flex flex-col flex-1 lg:ml-72 min-w-0">
        <Header />
        
        <main className="flex-1 p-8 lg:p-16 overflow-y-auto scrollbar">
          <div className="max-w-screen-2xl mx-auto w-full">
            {renderModule()}
          </div>
          
          {/* Global Page Footer */}
          <footer className="mt-32 pt-16 border-t border-premium-border flex flex-col md:flex-row justify-between items-start gap-8">
            <div className="max-w-xs">
              <h4 className="text-2xl font-display text-premium-burgundy mb-4">MedReport Intelligence</h4>
              <p className="text-xs font-medium text-premium-text-muted leading-relaxed uppercase tracking-widest">
                Professional-grade clinical documentation processing powered by neural architectures.
              </p>
            </div>
            <div className="flex gap-16">
              <div className="flex flex-col gap-3">
                <span className="label-uppercase">Project</span>
                <a href="#" className="text-xs font-bold hover:text-premium-burgundy transition-colors">Documentation</a>
                <a href="#" className="text-xs font-bold hover:text-premium-burgundy transition-colors">Model Notes</a>
              </div>
              <div className="flex flex-col gap-3">
                <span className="label-uppercase">Legal</span>
                <a href="#" className="text-xs font-bold hover:text-premium-burgundy transition-colors">HIPAA Compliance</a>
                <a href="#" className="text-xs font-bold hover:text-premium-burgundy transition-colors">Data Privacy</a>
              </div>
            </div>
          </footer>
        </main>
      </div>
    </div>
  );
}

export default App;
