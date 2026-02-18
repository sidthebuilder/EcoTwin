import React from 'react';

const ActivitySkeleton = () => (
    <div className="animate-pulse bg-white p-8 rounded-3xl border border-slate-100 shadow-sm">
        <div className="flex justify-between items-start">
            <div className="space-y-3 flex-1">
                <div className="h-4 bg-slate-100 rounded w-1/4"></div>
                <div className="h-6 bg-slate-100 rounded w-3/4"></div>
            </div>
            <div className="h-10 bg-slate-100 rounded w-16"></div>
        </div>
        <div className="mt-8 space-y-2">
            <div className="h-2 bg-slate-100 rounded"></div>
            <div className="h-2 bg-slate-100 rounded w-5/6"></div>
        </div>
    </div>
);

export default ActivitySkeleton;
