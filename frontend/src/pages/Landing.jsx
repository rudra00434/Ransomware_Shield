import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, Zap, Search, MessageSquare } from 'lucide-react';

const Landing = () => {
    return (
        <div className="min-h-[calc(100vh-80px)] flex flex-col items-center justify-center text-center px-4 relative overflow-hidden">
            {/* Decorative background blur bubbles */}
            <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-threat-clean/20 rounded-full mix-blend-screen filter blur-[128px] animate-pulse"></div>
            <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-threat-low/20 rounded-full mix-blend-screen filter blur-[128px] animate-pulse delay-1000"></div>

            <div className="max-w-4xl space-y-8 relative z-10">
                <div className="flex justify-center mb-6">
                    <div className="relative">
                        <Shield className="h-24 w-24 text-threat-clean drop-shadow-[0_0_15px_rgba(50,173,230,0.8)]" />
                        <div className="absolute inset-0 bg-threat-clean bg-opacity-20 blur-xl rounded-full"></div>
                    </div>
                </div>

                <h1 className="text-6xl md:text-8xl font-black tracking-tight drop-shadow-2xl">
                    Next-Gen <span className="text-transparent bg-clip-text bg-gradient-to-r from-threat-clean to-purple-500 drop-shadow-[0_0_10px_rgba(50,173,230,0.5)]">AI Analyst</span>
                </h1>

                <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto font-light leading-relaxed">
                    Real-time ransomware and malware analysis. Protect your endpoints with YARA, deep learning heuristics, and an interactive LLM security expert.
                </p>

                <div className="flex flex-col sm:flex-row justify-center gap-6 pt-10">
                    <Link to="/register" className="px-8 py-4 bg-gradient-to-r from-threat-clean to-blue-600 hover:from-blue-400 hover:to-blue-700 text-white font-bold rounded-full transition-all duration-300 transform hover:scale-105 hover:shadow-[0_0_20px_rgba(50,173,230,0.6)] text-lg flex items-center justify-center gap-2">
                        <Zap size={24} className="animate-pulse" /> Get Started Free
                    </Link>
                    <Link to="/login" className="px-8 py-4 glass-panel hover:bg-white/10 text-white font-bold rounded-full transition-all duration-300 transform hover:scale-105 text-lg">
                        Sign In
                    </Link>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 pt-24 text-left">
                    <div className="p-8 glass-panel rounded-2xl hover:-translate-y-2 transition-transform duration-300 group">
                        <Search className="h-12 w-12 text-threat-clean mb-6 group-hover:scale-110 transition-transform drop-shadow-[0_0_8px_rgba(50,173,230,0.5)]" />
                        <h3 className="text-2xl font-bold mb-3 text-white">Deep Scanning</h3>
                        <p className="text-gray-400 leading-relaxed">Multi-engine analysis using static extraction and precise YARA rules for zero-day threat detection.</p>
                    </div>
                    <div className="p-8 glass-panel rounded-2xl hover:-translate-y-2 transition-transform duration-300 group delay-100">
                        <Zap className="h-12 w-12 text-purple-400 mb-6 group-hover:scale-110 transition-transform drop-shadow-[0_0_8px_rgba(168,85,247,0.5)]" />
                        <h3 className="text-2xl font-bold mb-3 text-white">ML Classification</h3>
                        <p className="text-gray-400 leading-relaxed">Advanced Random Forest models trained on EMBER to classify suspicious file entropy.</p>
                    </div>
                    <div className="p-8 glass-panel rounded-2xl hover:-translate-y-2 transition-transform duration-300 group delay-200">
                        <MessageSquare className="h-12 w-12 text-threat-low mb-6 group-hover:scale-110 transition-transform drop-shadow-[0_0_8px_rgba(48,209,88,0.5)]" />
                        <h3 className="text-2xl font-bold mb-3 text-white">AI Assistant</h3>
                        <p className="text-gray-400 leading-relaxed">Understand complex threats instantly with plain-English LLM explanations and chat context.</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Landing;
