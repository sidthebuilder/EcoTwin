import React from 'react';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        console.error("EcoTwin UI Error:", error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <div className="min-h-screen flex items-center justify-center p-6 bg-slate-50">
                    <div className="bg-white p-10 rounded-3xl shadow-xl max-w-md text-center border border-red-100">
                        <h2 className="text-2xl font-bold text-slate-900">Something went wrong</h2>
                        <p className="text-slate-500 mt-4 leading-relaxed">
                            The Digital Twin encountered a glitch in the simulation. Try refreshing the browser.
                        </p>
                        <button
                            onClick={() => window.location.reload()}
                            className="mt-8 bg-indigo-600 text-white px-8 py-3 rounded-2xl font-bold shadow-lg shadow-indigo-200"
                        >
                            Restart Simulation
                        </button>
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
