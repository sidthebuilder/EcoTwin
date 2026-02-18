import React, { useState } from 'react';

const SimulationSandbox = () => {
    const [scenarios, setScenarios] = useState([
        { id: 1, label: 'Vehicle Type', baseline: 'Gas Sedan', modified: 'Electric Vehicle', impact: -2200 },
        { id: 2, label: 'Diet', baseline: 'Omnivore', modified: 'Vegetarian', impact: -1500 },
        { id: 3, label: 'Solar Install', baseline: 'Grid Only', modified: '5kW Solar System', impact: -3000 },
    ]);

    const totalImpact = scenarios.reduce((acc, s) => acc + s.impact, 0);

    return (
        <div className="bg-white rounded-3xl p-8 border border-gray-100 shadow-sm max-w-4xl mx-auto mt-12">
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h2 className="text-2xl font-bold text-gray-900">Simulation Sandbox</h2>
                    <p className="text-gray-500">Modify your Twin to see future footprint projections.</p>
                </div>
                <div className="text-right">
                    <div className="text-3xl font-black text-green-600">{totalImpact} kg</div>
                    <div className="text-xs text-gray-400 uppercase font-bold">Projected Annual Savings</div>
                </div>
            </div>

            <div className="space-y-4">
                {scenarios.map(scenario => (
                    <div key={scenario.id} className="flex items-center justify-between p-6 bg-gray-50 rounded-2xl border border-gray-100 hover:border-indigo-300 transition-colors">
                        <div className="flex gap-6 items-center">
                            <div className="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center text-indigo-600 font-bold">
                                {scenario.id}
                            </div>
                            <div>
                                <div className="font-semibold text-gray-900">{scenario.label}</div>
                                <div className="text-sm text-gray-500">
                                    <span className="line-through">{scenario.baseline}</span> → <span className="text-indigo-600 font-medium">{scenario.modified}</span>
                                </div>
                            </div>
                        </div>
                        <div className="text-lg font-bold text-green-600">{scenario.impact} kg</div>
                    </div>
                ))}
            </div>

            <button className="w-full mt-8 bg-indigo-600 text-white py-4 rounded-2xl font-bold text-lg hover:bg-indigo-700 shadow-lg shadow-indigo-200 transition-all">
                Add New Prediction Layer
            </button>
        </div>
    );
};

export default SimulationSandbox;
