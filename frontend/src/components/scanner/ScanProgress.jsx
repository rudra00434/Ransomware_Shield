import React from 'react';
import { Loader2, CheckCircle, Clock } from 'lucide-react';

const ScanProgress = ({ status }) => {
    const steps = [
        { key: 'PENDING', label: 'Queued for Analysis' },
        { key: 'SCANNING', label: 'Multi-Engine Deep Scan' },
        { key: 'COMPLETED', label: 'Analysis Complete' }
    ];

    const getStepStatus = (stepIndex, currentStatus) => {
        const currentIndex = steps.findIndex(s => s.key === currentStatus);
        if (currentStatus === 'FAILED') return 'failed';
        if (stepIndex < currentIndex) return 'completed';
        if (stepIndex === currentIndex) return 'active';
        return 'pending';
    };

    return (
        <div className="w-full max-w-2xl mx-auto mt-8 bg-dark-800 p-6 rounded-xl border border-gray-700 shadow-lg">
            <h3 className="text-lg font-semibold mb-6 flex items-center justify-center gap-2">
                <Loader2 className="animate-spin text-threat-clean" />
                Processing File...
            </h3>

            <div className="space-y-6 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-gray-700 before:to-transparent">
                {steps.map((step, idx) => {
                    const s = getStepStatus(idx, status);
                    return (
                        <div key={step.key} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                            <div className={`flex items-center justify-center w-10 h-10 rounded-full border-4 shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow
                ${s === 'completed' ? 'bg-threat-clean border-dark-900 text-dark-900' :
                                    s === 'active' ? 'bg-dark-900 border-threat-clean text-threat-clean' :
                                        'bg-dark-900 border-gray-700 text-gray-600'}
              `}>
                                {s === 'completed' ? <CheckCircle size={20} /> : <Clock size={20} />}
                            </div>
                            <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-lg bg-dark-900 border border-gray-700">
                                <div className="flex items-center justify-between space-x-2 mb-1">
                                    <div className={`font-bold ${s === 'active' ? 'text-white' : 'text-gray-400'}`}>{step.label}</div>
                                    <div className={`text-xs font-medium ${s === 'completed' ? 'text-threat-clean' : ''}`}>
                                        {s === 'active' && <span className="flex h-3 w-3"><span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-threat-clean opacity-75"></span><span className="relative inline-flex rounded-full h-3 w-3 bg-threat-clean"></span></span>}
                                    </div>
                                </div>
                            </div>
                        </div>
                    )
                })}
            </div>
        </div>
    );
};

export default ScanProgress;
