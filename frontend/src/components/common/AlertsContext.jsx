import React, { createContext, useContext, useEffect, useState } from 'react';

const AlertsContext = createContext();

export const useAlerts = () => useContext(AlertsContext);

export const AlertsProvider = ({ children }) => {
    const [alerts, setAlerts] = useState([]);
    const [ws, setWs] = useState(null);

    useEffect(() => {
        // Connect to the Django Channels WebSocket for alerts
        const socket = new WebSocket('ws://127.0.0.1:8000/ws/alerts/');

        socket.onopen = () => {
            console.log('Connected to Alerts WebSocket');
        };

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.message) {
                // Add the new alert to the state
                setAlerts((prevAlerts) => [...prevAlerts, data.message]);
            }
        };

        socket.onclose = () => {
            console.log('Disconnected from Alerts WebSocket');
        };

        setWs(socket);

        return () => {
            socket.close();
        };
    }, []);

    const dismissAlert = (indexToRemove) => {
        setAlerts((prevAlerts) => prevAlerts.filter((_, index) => index !== indexToRemove));
    };

    return (
        <AlertsContext.Provider value={{ alerts, dismissAlert }}>
            {children}

            {/* Global Alert Display Overlay */}
            {alerts.length > 0 && (
                <div className="fixed top-0 left-0 w-full z-50 pointer-events-none flex flex-col items-center pt-8 px-4 gap-4">
                    {alerts.map((alert, index) => (
                        <div key={index} className={`w-full max-w-2xl p-6 rounded-lg shadow-2xl pointer-events-auto flex items-start gap-4 transform transition-all 
                            ${alert.severity === 'CRITICAL' ? 'bg-red-900 border-l-4 border-red-500 text-white animate-pulse' : 'bg-yellow-800 border-l-4 border-yellow-500 text-white'}`}>

                            <div className="flex-1">
                                <h3 className="text-xl font-bold mb-2 flex items-center gap-2">
                                    <span className="text-2xl">⚠️</span> {alert.title || alert.type}
                                </h3>
                                <p className="text-gray-100">{alert.description || alert.message || JSON.stringify(alert)}</p>

                                {alert.filepath && (
                                    <div className="mt-3 p-2 bg-black bg-opacity-30 rounded font-mono text-sm break-all">
                                        Affected File: {alert.filepath}
                                    </div>
                                )}
                            </div>

                            <button
                                onClick={() => dismissAlert(index)}
                                className="text-white hover:text-gray-300 font-bold p-1 bg-black bg-opacity-20 rounded-full w-8 h-8 flex items-center justify-center shrink-0"
                            >
                                ×
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </AlertsContext.Provider>
    );
};
