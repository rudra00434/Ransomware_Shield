import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/common/Navbar';
import ProtectedRoute from './components/common/ProtectedRoute';
import { AlertsProvider } from './components/common/AlertsContext';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Scanner from './pages/Scanner';
import AIAssistant from './pages/AIAssistant';
import NetworkAnalysis from './pages/NetworkAnalysis';

function App() {
    return (
        <AlertsProvider>
            <BrowserRouter>
                <Navbar />
                <Routes>
                    <Route path="/" element={<Landing />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />

                    {/* Protected Routes */}
                    <Route element={<ProtectedRoute />}>
                        <Route path="/dashboard" element={<Dashboard />} />
                        <Route path="/scanner" element={<Scanner />} />
                        <Route path="/ai-chat" element={<AIAssistant />} />
                        <Route path="/network-analysis" element={<NetworkAnalysis />} />
                    </Route>
                </Routes>
            </BrowserRouter>
        </AlertsProvider>
    );
}

export default App;
