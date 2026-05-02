import React from 'react';

const LoadingSkeleton = () => {
  return (
    <div className="flex flex-col gap-12 animate-pulse py-12">
      {/* Editorial Grid Skeleton */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-4 h-[600px] bg-white border border-premiumNeutral" />
        <div className="lg:col-span-5 h-[600px] bg-white border border-premiumNeutral shadow-xl" />
        <div className="lg:col-span-3 h-[600px] bg-white border border-premiumNeutral" />
      </div>
      
      {/* Metrics Row Skeleton */}
      <div className="grid grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="bg-white border border-premiumNeutral p-6 h-24" />
        ))}
      </div>
    </div>
  );
};

export default LoadingSkeleton;
