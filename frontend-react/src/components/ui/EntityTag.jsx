import React from 'react';

const EntityTag = ({ label, category }) => {
  // Define strict clinical colors for taxonomies
  const styles = {
    DISEASE: 'text-red-700 bg-red-50 border-red-200',
    DRUG: 'text-blue-700 bg-blue-50 border-blue-200',
    SYMPTOM: 'text-amber-700 bg-amber-50 border-amber-200',
    TREATMENT: 'text-emerald-700 bg-emerald-50 border-emerald-200',
    DEFAULT: 'text-clinical-600 bg-clinical-50 border-clinical-200'
  };

  const styleClass = styles[category] || styles.DEFAULT;

  return (
    <span className={`px-2.5 py-1 rounded-md text-[11px] font-semibold uppercase tracking-wider border ${styleClass}`}>
      {label}
    </span>
  );
};

export default EntityTag;
