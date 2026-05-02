import React from 'react';

const Card = ({ children, className = '', title, subtitle, icon: Icon, rightElement, dark = false }) => {
  return (
    <div className={`premium-card relative flex flex-col ${dark ? 'bg-premium-dark text-white' : 'bg-white'} ${className}`}>
      {(title || Icon || rightElement) && (
        <div className={`px-8 py-6 flex items-center justify-between border-b ${dark ? 'border-white/10' : 'border-premium-border'}`}>
          <div className="flex flex-col">
            {subtitle && <span className="label-uppercase">{subtitle}</span>}
            <div className="flex items-center gap-3">
              {Icon && <Icon size={20} className={dark ? 'text-white/60' : 'text-premium-maroon'} />}
              <h3 className={`text-2xl font-display ${dark ? 'text-white' : 'text-premium-burgundy'}`}>{title}</h3>
            </div>
          </div>
          {rightElement && <div>{rightElement}</div>}
        </div>
      )}
      <div className="p-8 flex-1 overflow-y-auto scrollbar">
        {children}
      </div>
    </div>
  );
};

export default Card;
