import React from 'react';

const EntityTag = ({ label, category }) => {
  const styles = {
    DISEASE: 'text-premiumPrimary border-premiumAccent/20 bg-premiumAccent/5',
    DRUG: 'text-blue-900 border-blue-200 bg-blue-50/30',
    SYMPTOM: 'text-amber-900 border-amber-200 bg-amber-50/30',
    TREATMENT: 'text-emerald-900 border-emerald-200 bg-emerald-50/30',
    DEFAULT: 'text-premiumText-secondary border-premiumNeutral bg-premiumBg'
  };

  const styleClass = styles[category] || styles.DEFAULT;

  return (
    <span className={`px-3 py-1.5 border font-sans text-[10px] font-bold uppercase tracking-widest transition-all duration-300 hover:scale-105 ${styleClass}`}>
      {label}
    </span>
  );
};

export default EntityTag;
