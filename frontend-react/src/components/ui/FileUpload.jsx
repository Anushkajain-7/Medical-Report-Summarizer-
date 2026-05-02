import React, { useRef } from 'react';
import { UploadCloud, FileText, AlertCircle } from 'lucide-react';

const FileUpload = ({ file, onFileChange, error }) => {
  const fileInputRef = useRef(null);

  return (
    <div className="flex flex-col gap-3">
      <div 
        onClick={() => fileInputRef.current.click()}
        className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-all duration-200 
          ${file 
            ? 'border-clinical-accent bg-blue-50/30 hover:bg-blue-50/50' 
            : 'border-clinical-300 hover:border-clinical-accent bg-clinical-50 hover:bg-white'
          }`}
      >
        <div className="flex justify-center mb-4">
          <div className={`p-4 rounded-full ${file ? 'bg-blue-100' : 'bg-white shadow-sm border border-clinical-200'}`}>
            <UploadCloud size={32} className={file ? 'text-clinical-accent' : 'text-clinical-400'} />
          </div>
        </div>
        
        {file ? (
          <div>
            <p className="text-lg font-bold text-clinical-800 flex items-center justify-center gap-2">
              <FileText size={18} className="text-clinical-500" />
              {file.name}
            </p>
            <p className="text-sm font-medium text-clinical-500 mt-2">
              {(file.size / 1024).toFixed(1)} KB • Ready for Analysis
            </p>
          </div>
        ) : (
          <div>
            <p className="text-lg font-bold text-clinical-800">
              Select or drag document here
            </p>
            <p className="text-sm font-medium text-clinical-500 mt-2">
              Supported formats: PDF, DOCX, TXT (Max 5MB)
            </p>
          </div>
        )}
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={(e) => onFileChange(e.target.files?.[0] || null)} 
          accept=".pdf,.docx,.txt" 
          className="hidden" 
        />
      </div>

      {error && (
        <div className="px-4 py-3 bg-red-50 border border-red-100 rounded-lg flex items-start gap-3">
          <AlertCircle size={18} className="text-red-600 mt-0.5 shrink-0" />
          <p className="text-sm font-medium text-red-800">{error}</p>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
