import React, { useRef } from 'react';
import { Upload, FileText, X } from 'lucide-react';

const FileUpload = ({ file, onFileChange, error, loading }) => {
  const fileInputRef = useRef(null);

  return (
    <div className="flex flex-col gap-6 slide-up">
      <div 
        onClick={() => !loading && fileInputRef.current.click()}
        className={`group relative overflow-hidden transition-all duration-700 border-2 border-dashed p-16 text-center cursor-pointer
          ${file 
            ? 'border-premium-burgundy bg-premium-burgundy/5' 
            : 'border-premium-border bg-white hover:border-premium-maroon hover:bg-premium-bg'
          } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        <div className="flex flex-col items-center justify-center gap-6 relative z-10">
          <div className={`p-6 border transition-all duration-700 
            ${file ? 'border-premium-burgundy bg-premium-burgundy text-white' : 'border-premium-border bg-white group-hover:border-premium-maroon'}`}>
            <Upload size={32} strokeWidth={1.5} className={!file ? 'text-premium-burgundy' : ''} />
          </div>
          
          {file ? (
            <div className="fade-in">
              <h4 className="text-3xl font-display text-premium-burgundy italic">
                {file.name}
              </h4>
              <p className="label-uppercase mt-4 tracking-[0.4em]">
                Ready for Analysis • {(file.size / 1024).toFixed(1)} KB
              </p>
            </div>
          ) : (
            <div>
              <h4 className="text-4xl font-display text-premium-burgundy mb-2">
                Deposit Clinical Report
              </h4>
              <p className="label-uppercase tracking-[0.4em]">
                PDF • DOCX • TXT • LIMIT 5MB
              </p>
            </div>
          )}
        </div>
        
        {/* Decorative corner accents */}
        <div className="absolute top-4 left-4 w-8 h-8 border-t border-l border-premium-border group-hover:border-premium-maroon transition-colors duration-700" />
        <div className="absolute top-4 right-4 w-8 h-8 border-t border-r border-premium-border group-hover:border-premium-maroon transition-colors duration-700" />
        <div className="absolute bottom-4 left-4 w-8 h-8 border-b border-l border-premium-border group-hover:border-premium-maroon transition-colors duration-700" />
        <div className="absolute bottom-4 right-4 w-8 h-8 border-b border-r border-premium-border group-hover:border-premium-maroon transition-colors duration-700" />
        
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={(e) => onFileChange(e.target.files?.[0] || null)} 
          accept=".pdf,.docx,.txt" 
          className="hidden" 
        />
      </div>

      {error && (
        <div className="p-6 border border-premium-accent bg-premium-accent/5 text-premium-accent text-sm font-sans font-bold uppercase tracking-widest flex items-center gap-4 fade-in">
          <X size={16} />
          {error}
        </div>
      )}
    </div>
  );
};

export default FileUpload;
