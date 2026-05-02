import React, { useEffect, useState } from 'react';
import { checkHealth } from '../services/api';

const Header = () => {
  const [isOnline, setIsOnline] = useState(null);

  useEffect(() => {
    const check = async () => {
      const status = await checkHealth();
      setIsOnline(status);
    };
    check();
    const interval = setInterval(check, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="h-24 bg-premium-bg flex items-center justify-between px-8 lg:px-16 border-b border-premium-border/50 sticky top-0 z-40 backdrop-blur-md bg-opacity-80">
      <div className="flex items-center gap-12">
        <div className="hidden lg:flex flex-col">
          <span className="label-uppercase mb-0">Perspective</span>
          <h2 className="text-xl font-display italic text-premium-burgundy">Intelligence Dashboard</h2>
        </div>
      </div>

      <div className="flex items-center gap-12">
        <div className="flex flex-col items-end">
          <span className="label-uppercase mb-0">System Status</span>
          <div className="flex items-center gap-3">
             <div className={`w-1.5 h-1.5 rounded-full ${isOnline ? 'bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.6)]' : 'bg-premium-accent'}`} />
             <span className="text-[10px] font-bold uppercase tracking-widest text-premium-text-primary">
               {isOnline === null ? 'Initializing...' : isOnline ? 'Secure API Active' : 'Offline Mode'}
             </span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
