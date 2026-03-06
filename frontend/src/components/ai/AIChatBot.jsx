import React, { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, Loader2 } from 'lucide-react';
import { aiService } from '../../services/aiService';

const AIChatBot = () => {
    const [messages, setMessages] = useState([
        { role: 'assistant', text: 'Hello! I am your AI security analyst. How can I help you understand your recent scan results, or answer general malware questions?' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [suggestions, setSuggestions] = useState([
        "What is ransomware?",
        "How do I recover from WannaCry?",
        "Explain the last scan result."
    ]);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (text) => {
        if (!text.trim()) return;

        const userMsg = { role: 'user', text };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setIsLoading(true);

        try {
            const data = await aiService.sendMessage(text);
            setMessages(prev => [...prev, { role: 'assistant', text: data.reply }]);
            if (data.suggestions) {
                setSuggestions(data.suggestions);
            }
        } catch (error) {
            setMessages(prev => [...prev, { role: 'assistant', text: 'Sorry, I am having trouble connecting to the intelligence database right now.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex-1 flex flex-col h-full">
            {/* Chat History */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        {msg.role === 'assistant' && (
                            <div className="w-10 h-10 rounded-full bg-threat-clean/20 border border-threat-clean flex items-center justify-center shrink-0">
                                <Bot className="text-threat-clean" size={20} />
                            </div>
                        )}

                        <div className={`max-w-[80%] rounded-xl p-4 ${msg.role === 'user'
                            ? 'bg-blue-600 text-white rounded-br-none'
                            : 'bg-dark-900 border border-gray-700 text-gray-200 rounded-bl-none'
                            }`}>
                            {msg.text}
                        </div>

                        {msg.role === 'user' && (
                            <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center shrink-0">
                                <User className="text-gray-300" size={20} />
                            </div>
                        )}
                    </div>
                ))}
                {isLoading && (
                    <div className="flex gap-4">
                        <div className="w-10 h-10 rounded-full bg-threat-clean/20 border border-threat-clean flex items-center justify-center shrink-0">
                            <Bot className="text-threat-clean" size={20} />
                        </div>
                        <div className="bg-dark-900 border border-gray-700 rounded-xl p-4 rounded-bl-none flex items-center gap-2 text-gray-400">
                            <Loader2 className="animate-spin" size={16} /> Analyzing threat data...
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Suggestion Chips */}
            {suggestions.length > 0 && !isLoading && (
                <div className="px-6 pb-2 flex flex-wrap gap-2">
                    {suggestions.map((suggestion, idx) => (
                        <button
                            key={idx}
                            onClick={() => handleSend(suggestion)}
                            className="px-4 py-2 bg-dark-800 hover:bg-dark-700 border border-gray-600 rounded-full text-sm text-gray-300 transition"
                        >
                            {suggestion}
                        </button>
                    ))}
                </div>
            )}

            {/* Input Field */}
            <div className="p-4 border-t border-gray-700 bg-dark-800 rounded-b-xl">
                <form
                    className="flex gap-4"
                    onSubmit={(e) => { e.preventDefault(); handleSend(input); }}
                >
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        disabled={isLoading}
                        placeholder="Ask about threats, file analyses, or remediation steps..."
                        className="flex-1 bg-dark-900 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-threat-clean disabled:opacity-50"
                    />
                    <button
                        type="submit"
                        disabled={isLoading || !input.trim()}
                        className="bg-threat-clean hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-medium transition disabled:bg-gray-600 disabled:cursor-not-allowed flex items-center gap-2"
                    >
                        <Send size={18} />
                        <span className="hidden sm:inline">Send</span>
                    </button>
                </form>
            </div>
        </div>
    );
};

export default AIChatBot;
