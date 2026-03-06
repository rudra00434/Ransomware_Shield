import React, { useState, useEffect, useRef } from 'react';
import { Activity, ShieldAlert, Wifi, Play, Square, Server, WifiOff, AlertTriangle } from 'lucide-react';

const NetworkAnalysis = () => {
    const [connections, setConnections] = useState([]);
    const [analysisLog, setAnalysisLog] = useState([]);
    const [isMonitoring, setIsMonitoring] = useState(false);
    const [error, setError] = useState(null);
    const [mitmAlert, setMitmAlert] = useState(null);
    const ws = useRef(null);
    const analysisEndRef = useRef(null);

    // Auto-scroll the AI analysis log
    useEffect(() => {
        analysisEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [analysisLog]);

    useEffect(() => {
        // Initialize WebSocket connection
        ws.current = new WebSocket('ws://localhost:8000/ws/network-analysis/');

        ws.current.onopen = () => {
            console.log("WebSocket Connected");
            setError(null);
        };

        ws.current.onmessage = (event) => {
            const data = JSON.parse(event.data);

            if (data.type === 'network_data') {
                setConnections(data.connections);
            } else if (data.type === 'ai_analysis') {
                setAnalysisLog(prev => [...prev, {
                    time: new Date().toLocaleTimeString(),
                    text: data.analysis
                }]);
            } else if (data.type === 'mitm_alert') {
                setMitmAlert(data.alert);
            } else if (data.error) {
                setError(data.error);
                setIsMonitoring(false);
            } else if (data.status === 'monitoring_started') {
                setIsMonitoring(true);
            } else if (data.status === 'monitoring_stopped') {
                setIsMonitoring(false);
                setConnections([]);
                setMitmAlert(null); // Clear alerts on stop
            }
        };

        ws.current.onerror = (err) => {
            console.error('WebSocket Error:', err);
            setError('Lost connection to the analysis server.');
            setIsMonitoring(false);
        };

        ws.current.onclose = () => {
            setIsMonitoring(false);
            console.log("WebSocket Disconnected");
        };

        return () => {
            if (ws.current) {
                ws.current.close();
            }
        };
    }, []);

    const toggleMonitoring = () => {
        if (!ws.current || ws.current.readyState !== WebSocket.OPEN) {
            setError("Cannot connect to server. Ensure the backend is running.");
            return;
        }

        if (isMonitoring) {
            ws.current.send(JSON.stringify({ command: 'stop' }));
        } else {
            setError(null);
            setMitmAlert(null);
            ws.current.send(JSON.stringify({ command: 'start' }));
            // Add initial log entry
            setAnalysisLog([{
                time: new Date().toLocaleTimeString(),
                text: "Initiating live network traffic capture and AI analysis loop..."
            }]);
        }
    };

    return (
        <div className="max-w-7xl mx-auto p-6 pt-12 pb-24 relative overflow-hidden">
            <div className="absolute top-0 left-0 w-[500px] h-[500px] bg-indigo-500/5 rounded-full mix-blend-screen filter blur-[100px] pointer-events-none"></div>

            <div className="mb-8 relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="flex items-center gap-4">
                    <div className="bg-indigo-500/20 p-4 rounded-2xl border border-indigo-500/30 relative">
                        {isMonitoring && (
                            <span className="absolute -top-1 -right-1 flex h-3 w-3">
                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                                <span className="relative inline-flex rounded-full h-3 w-3 bg-indigo-500"></span>
                            </span>
                        )}
                        <Activity className={`h-10 w-10 ${isMonitoring ? 'text-indigo-400 animate-pulse' : 'text-gray-500'}`} />
                    </div>
                    <div>
                        <h1 className="text-3xl font-black tracking-tight drop-shadow-md">Live Network <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">Monitor</span></h1>
                        <p className="text-gray-400 mt-1 text-lg">Continuous AI analysis of your active system connections.</p>
                    </div>
                </div>

                {error && (
                    <div className="mb-6 glass-panel border-threat-critical/50 text-threat-critical p-4 rounded-xl flex items-center gap-3 relative z-10 shadow-[0_0_15px_rgba(255,45,85,0.2)]">
                        <ShieldAlert className="animate-pulse flex-shrink-0" />
                        <span className="font-semibold">{error}</span>
                    </div>
                )}

                <div className="flex items-center gap-4">
                    <button
                        onClick={() => {
                            if (!isMonitoring) {
                                setError("Please start the live monitor first to test alerts.");
                                return;
                            }
                            setMitmAlert({
                                title: 'Man-in-the-Middle Attack Detected (ARP Spoofing)',
                                description: 'A single physical device is claiming to be multiple IP addresses on your network. This strongly indicates an active interception attack.',
                                severity: 'CRITICAL',
                                mac: '00-11-22-33-44-55',
                                ips: ['192.168.1.1', '192.168.1.100', '192.168.1.105']
                            });
                        }}
                        className="text-gray-400 hover:text-threat-critical transition-colors text-sm font-medium px-3 py-2 border border-transparent hover:border-threat-critical/30 rounded-lg"
                    >
                        Simulate Attack
                    </button>

                    <button
                        onClick={toggleMonitoring}
                        className={`flex items-center gap-2 px-6 py-3 rounded-xl font-bold transition-all shadow-lg ${isMonitoring
                            ? 'bg-threat-critical/20 text-threat-critical border border-threat-critical/50 hover:bg-threat-critical/30'
                            : 'bg-gradient-to-r from-indigo-600 to-cyan-600 text-white hover:from-indigo-500 hover:to-cyan-500 border border-transparent hover:shadow-[0_0_15px_rgba(99,102,241,0.4)]'
                            }`}
                    >
                        {isMonitoring ? (
                            <><Square size={18} fill="currentColor" /> Stop Capturing</>
                        ) : (
                            <><Play size={18} fill="currentColor" /> Start Live Monitor</>
                        )}
                    </button>
                </div>
            </div>

            {/* MitM Alert Banner */}
            {mitmAlert && (
                <div className="mb-8 -mt-2 animate-in slide-in-from-top-4 fade-in duration-500">
                    <div className="bg-gradient-to-r from-threat-critical/20 to-red-900/40 border-2 border-threat-critical/60 rounded-2xl p-6 relative overflow-hidden shadow-[0_0_30px_rgba(255,45,85,0.3)]">
                        <div className="absolute inset-0 bg-threat-critical mix-blend-overlay opacity-10 animate-pulse"></div>
                        <div className="absolute -right-10 -top-10 opacity-10">
                            <AlertTriangle size={150} className="text-threat-critical" />
                        </div>

                        <div className="relative z-10 flex items-start gap-4">
                            <div className="bg-threat-critical/20 p-3 rounded-xl shrink-0 border border-threat-critical/30">
                                <AlertTriangle className="h-8 w-8 text-threat-critical animate-pulse" />
                            </div>
                            <div className="flex-1">
                                <h3 className="text-2xl font-black text-white tracking-wide mb-1 flex items-center gap-3">
                                    {mitmAlert.title}
                                    <span className="px-3 py-1 bg-threat-critical text-white text-xs font-bold rounded-full uppercase tracking-wider">
                                        ACTION REQUIRED
                                    </span>
                                </h3>
                                <p className="text-gray-300 text-lg mb-4">{mitmAlert.description}</p>

                                <div className="bg-dark-900/60 p-4 rounded-xl border border-threat-critical/20 font-mono text-sm inline-block">
                                    <div className="text-gray-400 mb-1">Conflicting Hardware Address:</div>
                                    <div className="text-threat-critical font-bold text-lg">{mitmAlert.mac.toUpperCase()}</div>
                                    <div className="text-gray-400 mt-3 mb-1">Spoofing IP Addresses:</div>
                                    <div className="flex flex-wrap gap-2">
                                        {mitmAlert.ips.map(ip => (
                                            <span key={ip} className="bg-threat-critical/20 text-red-300 px-2 py-1 rounded border border-threat-critical/30">
                                                {ip}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 relative z-10">
                {/* Connections Feed */}
                <div className="glass-panel p-6 rounded-2xl border border-white/10 shadow-2xl flex flex-col h-[700px]">
                    <div className="flex justify-between items-center mb-4 border-b border-gray-700 pb-3">
                        <div className="flex items-center gap-2">
                            <Wifi className="text-cyan-400" size={20} />
                            <h2 className="text-xl font-bold text-white">Active Connections Feed</h2>
                        </div>
                        <span className="bg-dark-900 border border-gray-700 px-3 py-1 rounded-full text-xs font-mono text-gray-300">
                            {connections.length} ACTIVE
                        </span>
                    </div>

                    <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar space-y-2">
                        {!isMonitoring && connections.length === 0 ? (
                            <div className="h-full flex flex-col items-center justify-center text-gray-500 opacity-50">
                                <WifiOff className="h-16 w-16 mb-4" />
                                <p>Monitoring is offline. Press Start to capture.</p>
                            </div>
                        ) : (
                            connections.map((conn, idx) => (
                                <div key={idx} className="bg-dark-900/50 border border-gray-800 p-3 rounded-lg flex flex-col text-sm font-mono hover:border-gray-600 transition-colors">
                                    <div className="flex justify-between items-center mb-2">
                                        <span className={`px-2 py-0.5 rounded text-xs font-bold ${conn.status === 'LISTEN' ? 'bg-indigo-500/20 text-indigo-400' : 'bg-green-500/20 text-green-400'
                                            }`}>
                                            {conn.status}
                                        </span>
                                        <span className="text-gray-500 text-xs">PID: {conn.pid} • {conn.type}</span>
                                    </div>
                                    <div className="grid grid-cols-2 gap-2 text-gray-300">
                                        <div>
                                            <span className="text-gray-500 text-xs block mb-0.5">LOCAL</span>
                                            {conn.local_address || 'N/A'}
                                        </div>
                                        <div>
                                            <span className="text-gray-500 text-xs block mb-0.5">REMOTE</span>
                                            {conn.remote_address || 'N/A'}
                                        </div>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </div>

                {/* AI Analyst Log */}
                <div className="glass-panel p-6 rounded-2xl border border-white/10 shadow-2xl flex flex-col h-[700px] bg-gradient-to-b from-dark-800 to-indigo-900/10">
                    <div className="flex items-center gap-2 mb-4 border-b border-gray-700 pb-3 shrink-0">
                        <Server className="text-indigo-400" size={20} />
                        <h2 className="text-xl font-bold text-white">Live AI Analyst Log</h2>
                    </div>

                    <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar">
                        {analysisLog.length === 0 && !isMonitoring ? (
                            <div className="h-full flex flex-col items-center justify-center text-gray-500 opacity-50">
                                <Server className="h-16 w-16 mb-4" />
                                <p>Awaiting live connection stream...</p>
                            </div>
                        ) : (
                            <div className="space-y-4">
                                {analysisLog.map((log, idx) => (
                                    <div key={idx} className="animate-in fade-in slide-in-from-bottom-2 duration-300">
                                        <div className="flex items-center gap-2 mb-1">
                                            <div className="w-2 h-2 rounded-full bg-indigo-500"></div>
                                            <span className="text-xs font-mono text-indigo-400">{log.time}</span>
                                            <span className="text-xs font-bold text-gray-500 uppercase">SYSTEM UPDATE</span>
                                        </div>
                                        <div className="bg-black/40 border border-indigo-500/20 p-4 rounded-xl rounded-tl-none prose prose-sm prose-invert prose-indigo max-w-none shadow-inner">
                                            {log.text.split('\n').map((line, i) => (
                                                <p key={i} className="mb-1 text-gray-300 leading-relaxed">{line}</p>
                                            ))}
                                        </div>
                                    </div>
                                ))}

                                {isMonitoring && (
                                    <div className="flex items-center gap-3 text-indigo-400/70 p-4">
                                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-indigo-400"></div>
                                        <span className="text-sm font-medium animate-pulse">Analyzing network stream...</span>
                                    </div>
                                )}
                                <div ref={analysisEndRef} />
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default NetworkAnalysis;
