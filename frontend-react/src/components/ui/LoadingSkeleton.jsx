import React from 'react';
import Card from './Card';
import StatusStepper from './StatusStepper';

const LoadingSkeleton = () => {
  return (
    <div className="flex flex-col gap-6 animate-pulse">
      {/* Metrics Row Skeleton */}
      <div className="grid grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="bg-white rounded-lg border border-clinical-200 p-4 h-24 flex flex-col justify-center">
            <div className="h-2 w-16 bg-clinical-200 rounded mb-3"></div>
            <div className="h-6 w-24 bg-clinical-100 rounded"></div>
          </div>
        ))}
      </div>

      {/* Main 3-Column Skeleton */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {[1, 2, 3].map((i) => (
          <Card key={i} className="h-[500px]">
             <div className="space-y-4">
               <div className="h-4 w-3/4 bg-clinical-100 rounded"></div>
               <div className="h-4 w-full bg-clinical-50 rounded"></div>
               <div className="h-4 w-5/6 bg-clinical-50 rounded"></div>
               <div className="h-4 w-full bg-clinical-50 rounded"></div>
               <div className="h-4 w-2/3 bg-clinical-50 rounded"></div>
             </div>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default LoadingSkeleton;
