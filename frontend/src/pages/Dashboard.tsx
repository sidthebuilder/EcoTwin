import React, { useState } from 'react';
import {
    BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer
} from 'recharts';
import { Leaf, ArrowRight, Activity, Calendar } from 'lucide-react';
import ActivityDisplay from '../components/ActivityDisplay';

import { activityService, Activity } from '../services/api';

const Dashboard = () => {
    const [viewMode, setViewMode] = useState('overview');
    const [activities, setActivities] = useState<Activity[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await activityService.getAll();
                setActivities(data);
                setError(null); // Clear any previous errors on successful fetch
            } catch (err) {
                console.error("Failed to fetch dashboard data:", err);
                setError('Failed to load dashboard data. Please check your connection and try again.');
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    // Calculate metrics from real data
    const totalFootprint = activities.reduce((sum, act) => sum + act.carbon_estimate, 0);
    // Simple mock aggregation for the chart (in a real app, backend should provide this)
    const chartData = [
        { name: 'Mon', mobility: 12, home: 18 },
        { name: 'Tue', mobility: 15, home: 16 },
        { name: 'Wed', mobility: 8, home: 19 },
        { name: 'Thu', mobility: 22, home: 17 },
        { name: 'Fri', mobility: 18, home: 20 },
        { name: 'Sat', mobility: 5, home: 22 },
        { name: 'Sun', mobility: 3, home: 21 },
    ];

    return (
        <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
            {/* Navigation */}
            <nav className="border-b border-gray-200 bg-white">
                <div className="max-w-5xl mx-auto px-6 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-2 font-semibold text-lg tracking-tight">
                        <div className="w-8 h-8 bg-emerald-100 text-emerald-700 flex items-center justify-center rounded-lg">
                            <Leaf size={18} />
                        </div>
                        EcoTwin
                    </div>
                    <div className="flex gap-6 text-sm font-medium text-gray-500">
                        <button className="text-gray-900 hover:text-emerald-700 transition-colors">Dashboard</button>
                        <button className="hover:text-emerald-700 transition-colors">Reports</button>
                        <button className="hover:text-emerald-700 transition-colors">Settings</button>
                    </div>
                    <div className="w-8 h-8 bg-gray-200 rounded-full border border-gray-300"></div>
                </div>
            </nav>

            <main className="max-w-5xl mx-auto px-6 py-12 space-y-12">
                {/* Header Section */}
                <section className="flex justify-between items-end">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
                        <p className="text-gray-500 mt-2">Overview of your personal carbon footprint.</p>
                    </div>
                    <div className="flex gap-2 bg-white border border-gray-200 p-1 rounded-lg">
                        {['Overview', 'Analysis'].map(m => (
                            <button
                                key={m}
                                onClick={() => setViewMode(m.toLowerCase())}
                                className={`px-4 py-1.5 text-sm font-medium rounded-md transition-all ${viewMode === m.toLowerCase()
                                    ? 'bg-gray-100 text-gray-900 shadow-sm'
                                    : 'text-gray-500 hover:text-gray-700'
                                    }`}
                            >
                                {m}
                            </button>
                        ))}
                    </div>
                </section>

                {/* Key Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                        <div className="flex items-center gap-2 text-gray-500 text-sm font-medium mb-4">
                            <Activity size={16} />
                            Annual Projection
                        </div>
                        <div className="text-4xl font-bold text-gray-900 tracking-tight">
                            {totalFootprint.toFixed(1)} <span className="text-xl text-gray-400 font-normal">tons</span>
                        </div>
                        <div className="mt-4 text-sm text-emerald-700 bg-emerald-50 inline-block px-2 py-0.5 rounded font-medium">
                            ↓ 12% vs last year
                        </div>
                    </div>

                    <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm md:col-span-2">
                        <div className="flex items-center justify-between mb-6">
                            <div className="flex items-center gap-2 text-gray-500 text-sm font-medium">
                                <Calendar size={16} />
                                Recent Activity
                            </div>
                            <div className="text-xs font-semibold text-emerald-600 cursor-pointer">View full report →</div>
                        </div>
                        <div className="h-32">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={chartData} barSize={32}>
                                    <XAxis
                                        dataKey="name"
                                        axisLine={false}
                                        tickLine={false}
                                        tick={{ fill: '#9ca3af', fontSize: 12 }}
                                        dy={10}
                                    />
                                    <Tooltip
                                        cursor={{ fill: '#f3f4f6' }}
                                        contentStyle={{ borderRadius: '8px', border: '1px solid #e5e7eb', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                                    />
                                    <Bar dataKey="home" stackId="a" fill="#d1d5db" radius={[0, 0, 4, 4]} />
                                    <Bar dataKey="mobility" stackId="a" fill="#10b981" radius={[4, 4, 0, 0]} />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>

                {/* Activity Feed */}
                <section className="grid grid-cols-1 lg:grid-cols-3 gap-12">
                    <div className="lg:col-span-2 space-y-6">
                        <h2 className="text-lg font-semibold text-gray-900 border-b border-gray-100 pb-2">Latest Updates</h2>
                        <div className="space-y-4">
                            {loading ? (
                                <p className="text-gray-500">Loading your eco-twin...</p>
                            ) : error ? (
                                <div className="p-4 bg-red-50 text-red-700 rounded-md border border-red-200 flex items-center gap-2">
                                    <AlertCircle className="w-5 h-5" />
                                    <span>{error}</span>
                                    <button
                                        onClick={() => window.location.reload()}
                                        className="ml-auto text-sm font-semibold underline hover:text-red-900"
                                    >
                                        Retry
                                    </button>
                                </div>
                            ) : (
                                activities.map(activity => (
                                    <ActivityDisplay key={activity.id} activity={activity} />
                                ))
                            )}
                        </div>
                    </div>

                    {/* Simple Sidebar */}
                    <div className="space-y-6">
                        <h2 className="text-lg font-semibold text-gray-900 border-b border-gray-100 pb-2">Suggestions</h2>

                        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm group hover:border-emerald-200 transition-colors cursor-pointer">
                            <h3 className="font-semibold text-gray-900 group-hover:text-emerald-700 transition-colors">Switch to Renewable</h3>
                            <p className="text-sm text-gray-500 mt-2 leading-relaxed">
                                Your heating usage is high. Switching to a simplified heat pump system could save 1.2 tons annually.
                            </p>
                            <div className="mt-4 flex items-center text-sm font-medium text-emerald-600 gap-1">
                                Simulate Impact <ArrowRight size={14} />
                            </div>
                        </div>

                        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm group hover:border-emerald-200 transition-colors cursor-pointer">
                            <h3 className="font-semibold text-gray-900 group-hover:text-emerald-700 transition-colors">Optimize Commute</h3>
                            <p className="text-sm text-gray-500 mt-2 leading-relaxed">
                                2 days of remote work can reduce your mobility footprint by 15%.
                            </p>
                            <div className="mt-4 flex items-center text-sm font-medium text-emerald-600 gap-1">
                                Simulate Impact <ArrowRight size={14} />
                            </div>
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
};

export default Dashboard;
