import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, LogOut } from 'lucide-react';
import useAuthStore from '../../store/authStore';

const Navbar = () => {
    const { isAuthenticated, logout } = useAuthStore();

    return (
        <nav className="glass-panel sticky top-0 z-50 py-4 px-6 md:px-12 flex justify-between items-center transition-all duration-300">
            <Link to="/" className="flex items-center gap-2 text-threat-clean font-bold text-xl tracking-wide hover:scale-105 transition-transform duration-300 drop-shadow-[0_0_8px_rgba(50,173,230,0.5)]">
                <Shield size={28} />
                Ransomware Shield
            </Link>

            <div className="flex items-center gap-6">
                {isAuthenticated ? (
                    <>
                        <Link to="/scanner" className="text-gray-300 hover:text-white transition">Scanner</Link>
                        <Link to="/dashboard" className="text-gray-300 hover:text-white transition">Dashboard</Link>
                        <Link to="/network-analysis" className="text-gray-300 hover:text-white transition">Network Analysis</Link>
                        <Link to="/ai-chat" className="text-gray-300 hover:text-white transition">AI Assistant</Link>
                        <button
                            onClick={logout}
                            className="flex items-center gap-2 text-threat-critical hover:text-red-400 transition"
                            title="Logout"
                        >
                            <LogOut size={20} />
                        </button>
                    </>
                ) : (
                    <>
                        <Link to="/login" className="text-gray-300 hover:text-white transition">Login</Link>
                        <Link to="/register" className="bg-threat-clean hover:bg-blue-600 text-white px-4 py-2 rounded-md font-medium transition">
                            Sign Up
                        </Link>
                    </>
                )}
            </div>
        </nav>
    );
};

export default Navbar;
