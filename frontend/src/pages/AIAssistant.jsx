import React from 'react';
import AIChatBot from '../components/ai/AIChatBot';

const AIAssistant = () => {
    return (
        <div className="max-w-5xl mx-auto p-6 pt-12 h-[calc(100vh-100px)] flex flex-col">
            <div className="mb-6">
                <h1 className="text-3xl font-bold">Security AI Assistant</h1>
                <p className="text-gray-400 mt-1">Get immediate, LLM-powered context on indicators of compromise.</p>
            </div>

            <div className="flex-1 bg-dark-800 rounded-xl border border-gray-700 flex flex-col overflow-hidden shadow-2xl">
                <AIChatBot />
            </div>
        </div>
    );
};

export default AIAssistant;
