import { useState } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import EndToEnd from './modules/EndToEnd';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="flex min-h-screen w-full bg-premiumBg text-premiumText-primary selection:bg-premiumPrimary selection:text-white">
      {/* Editorial Sidebar */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Perspective Content */}
      <div className="flex flex-col flex-1 lg:ml-72 min-w-0">
        <Header />
        
        <main className="flex-1 p-8 lg:p-16 overflow-y-auto scrollbar">
          <div className="max-w-screen-2xl mx-auto w-full">
            {activeTab === 'dashboard' ? <EndToEnd /> : <EndToEnd />}
          </div>
          
          {/* Global Page Footer */}
          <footer className="mt-32 pt-16 border-t border-premiumNeutral flex flex-col md:flex-row justify-between items-start gap-8">
            <div className="max-w-xs">
              <h4 className="text-2xl font-display text-premiumPrimary mb-4">MedReport Assistant</h4>
              <p className="text-xs font-medium text-premiumText-muted leading-relaxed uppercase tracking-widest">
                AI-powered clinical report interpretation for patients and caregivers.
              </p>
            </div>
            <div className="flex gap-16 text-[10px] font-bold uppercase tracking-widest text-premiumText-muted">
               <span>Secure</span>
               <span>Private</span>
               <span>HIPAA Compliant</span>
            </div>
          </footer>
        </main>
      </div>
    </div>
  );
}

export default App;
