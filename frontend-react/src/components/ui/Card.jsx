import React from 'react';

const Card = ({ children, className = '', title, icon: Icon, rightElement }) => {
  return (
    <div className={`bg-white rounded-xl shadow-sm border border-clinical-200 flex flex-col overflow-hidden ${className}`}>
      {(title || Icon || rightElement) && (
        <div className="bg-clinical-50 border-b border-clinical-200 px-5 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            {Icon && <Icon size={18} className="text-clinical-500" />}
            <h3 className="font-semibold text-clinical-800 text-sm tracking-wide">{title}</h3>
          </div>
          {rightElement && <div>{rightElement}</div>}
        </div>
      )}
      <div className="p-5 flex-1 overflow-y-auto scrollbar">
        {children}
      </div>
    </div>
  );
};

export default Card;
