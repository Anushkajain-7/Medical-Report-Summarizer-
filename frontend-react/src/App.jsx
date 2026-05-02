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
    <div className="flex min-h-screen w-full bg-clinical-50 text-clinical-800">
      {/* Sidebar - Fixed on the left */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Area */}
      <div className="flex flex-col flex-1 ml-64 min-w-0 transition-all duration-300">
        <Header />
        
        {/* Module Content */}
        <main className="flex-1 p-8 overflow-y-auto scrollbar">
          <div className="max-w-7xl mx-auto">
            {renderModule()}
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
