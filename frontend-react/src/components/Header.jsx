import React, { useEffect, useState } from 'react';
import { checkHealth } from '../services/api';
import { ShieldCheck, ShieldAlert } from 'lucide-react';

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
    <header className="h-16 bg-white border-b border-clinical-200 flex items-center justify-between px-8 shadow-sm">
      <div className="flex items-center">
        <h2 className="text-clinical-800 font-semibold tracking-tight">Clinical Processing Dashboard</h2>
      </div>
      <div className="flex items-center gap-2">
        {isOnline === null ? (
          <span className="text-clinical-400 text-sm font-medium flex items-center gap-2">
             <span className="w-2 h-2 rounded-full bg-clinical-400 animate-pulse"></span>
             Checking Connectivity...
          </span>
        ) : isOnline ? (
          <div className="flex items-center gap-2 px-3 py-1.5 bg-clinical-50 border border-clinical-200 rounded-md">
            <ShieldCheck size={16} className="text-clinical-success" />
            <span className="text-clinical-success text-xs font-bold uppercase tracking-wider">Secure API Online</span>
          </div>
        ) : (
          <div className="flex items-center gap-2 px-3 py-1.5 bg-clinical-50 border border-clinical-200 rounded-md">
            <ShieldAlert size={16} className="text-clinical-danger" />
            <span className="text-clinical-danger text-xs font-bold uppercase tracking-wider">API Offline</span>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
