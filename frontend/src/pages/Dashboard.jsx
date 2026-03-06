import React, { useState, useEffect } from 'react';
import ThreatChart from '../components/dashboard/ThreatChart';
import { Activity, ShieldAlert, ShieldCheck } from 'lucide-react';
import axios from 'axios';

const Dashboard = () => {
    const [data, setData] = useState({
        kpi: {
            total_scans_7d: 0,
            scan_change_pct: 0,
            critical_threats: 0,
            suspicious_files: 0,
            clean_files: 0,
            clear_rate: 0
        },
        recent_detections: [],
        timeline: []
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/dashboard/stats/');
                setData(response.data);
            } catch (error) {
                console.error("Failed to fetch dashboard data:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchDashboardData();

        // Optional: refresh data every 30 seconds
        const interval = setInterval(fetchDashboardData, 30000);
        return () => clearInterval(interval);
    }, []);

    if (loading) {
        return <div className="max-w-7xl mx-auto p-6 pt-12 text-center text-gray-400">Loading real-time telemetry...</div>;
    }

    const { kpi, recent_detections, timeline } = data;

    return (
        <div className="max-w-7xl mx-auto p-6 pt-12">
            <div className="flex justify-between items-end mb-8">
                <div>
                    <h1 className="text-3xl font-bold">Security Overview</h1>
                    <p className="text-gray-400 mt-1">Real-time telemetry and threat intelligence</p>
                </div>
                <button className="bg-dark-800 hover:bg-dark-700 border border-gray-600 px-4 py-2 rounded-lg text-sm font-medium transition">
                    Export Report
                </button>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div className="bg-dark-800 p-6 rounded-xl border border-gray-700 shadow-lg relative overflow-hidden group hover:border-gray-500 transition">
                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition">
                        <Activity size={64} />
                    </div>
                    <h3 className="text-gray-400 font-medium mb-1">Total Scans (7d)</h3>
                    <p className="text-4xl font-bold text-white">{kpi.total_scans_7d}</p>
                    <p className={`text-sm mt-2 font-medium ${kpi.scan_change_pct >= 0 ? 'text-threat-clean' : 'text-threat-high'}`}>
                        {kpi.scan_change_pct >= 0 ? '+' : ''}{kpi.scan_change_pct}% vs last week
                    </p>
                </div>

                <div className="bg-dark-800 p-6 rounded-xl border border-threat-critical/30 shadow-lg relative overflow-hidden group hover:border-threat-critical/50 transition">
                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition text-threat-critical">
                        <ShieldAlert size={64} />
                    </div>
                    <h3 className="text-gray-400 font-medium mb-1">Critical Threats</h3>
                    <p className="text-4xl font-bold text-threat-critical">{kpi.critical_threats}</p>
                    <p className="text-gray-400 text-sm mt-2">All time detections</p>
                </div>

                <div className="bg-dark-800 p-6 rounded-xl border border-threat-high/30 shadow-lg relative overflow-hidden">
                    <h3 className="text-gray-400 font-medium mb-1">Suspicious Files</h3>
                    <p className="text-4xl font-bold text-threat-high">{kpi.suspicious_files}</p>
                    <p className="text-gray-400 text-sm mt-2">Requires manual review</p>
                </div>

                <div className="bg-dark-800 p-6 rounded-xl border border-threat-clean/30 shadow-lg relative overflow-hidden group hover:border-threat-clean/50 transition">
                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition text-threat-clean">
                        <ShieldCheck size={64} />
                    </div>
                    <h3 className="text-gray-400 font-medium mb-1">Clean Files</h3>
                    <p className="text-4xl font-bold text-threat-clean">{kpi.clean_files}</p>
                    <p className="text-threat-clean text-sm mt-2 font-medium">{kpi.clear_rate}% clear rate</p>
                </div>
            </div>

            {/* Charts Area */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 bg-dark-800 p-6 rounded-xl border border-gray-700 shadow-lg">
                    <h3 className="text-xl font-bold mb-6">Threat Timeline</h3>
                    <div className="h-80 w-full">
                        <ThreatChart data={timeline} />
                    </div>
                </div>
                <div className="bg-dark-800 p-6 rounded-xl border border-gray-700 shadow-lg flex flex-col">
                    <h3 className="text-xl font-bold mb-4">Recent Detections</h3>
                    <div className="flex-1 space-y-4 overflow-y-auto">
                        {recent_detections.length > 0 ? (
                            recent_detections.map((item) => (
                                <div key={item.id} className="flex items-center justify-between p-3 rounded-lg bg-dark-900 border border-gray-800 hover:border-gray-600 transition cursor-pointer">
                                    <div className="truncate pr-4 flex-1">
                                        <p className="font-medium text-sm truncate" title={item.file_name}>{item.file_name}</p>
                                        <p className="text-xs text-gray-400 mt-1">
                                            {new Date(item.created_at).toLocaleString()}
                                        </p>
                                    </div>
                                    <div className={`px-3 py-1 rounded text-xs font-bold border ${item.threat_level === 'CRITICAL' ? 'bg-threat-critical/20 text-threat-critical border-threat-critical/30' :
                                            item.threat_level === 'HIGH' ? 'bg-threat-high/20 text-threat-high border-threat-high/30' :
                                                'bg-threat-medium/20 text-threat-medium border-threat-medium/30'
                                        }`}>
                                        {item.threat_level}
                                    </div>
                                </div>
                            ))
                        ) : (
                            <div className="text-center text-gray-500 text-sm mt-4">
                                No malicious or suspicious files detected yet.
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
