import React from 'react';
import { Plane, ShoppingCart, Home, Zap } from 'lucide-react';

import { Activity } from '../services/api';

const getIcon = (type: string) => {
    switch (type.toLowerCase()) {
        case 'travel': return <Plane size={18} />;
        case 'groceries': return <ShoppingCart size={18} />;
        case 'housing': return <Home size={18} />;
        default: return <Zap size={18} />;
    }
};

const ActivityDisplay: React.FC<{ activity: Activity }> = ({ activity }) => {
    return (
        <div className="flex items-start gap-4 p-4 rounded-xl bg-white border border-gray-200 hover:border-gray-300 transition-colors">
            <div className="w-10 h-10 rounded-full bg-gray-50 border border-gray-100 flex items-center justify-center text-gray-500">
                {getIcon(activity.activity_type)}
            </div>

            <div className="flex-1 min-w-0">
                <div className="flex justify-between items-start">
                    <div>
                        <p className="text-sm font-medium text-gray-900">{activity.description}</p>
                        <p className="text-xs text-gray-500 mt-0.5">{activity.timestamp}</p>
                    </div>
                    <div className="text-right">
                        <div className="text-sm font-semibold text-gray-900">{activity.carbon_estimate} kg</div>
                        <div className="text-[10px] font-medium text-gray-400">CO2e</div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ActivityDisplay;
