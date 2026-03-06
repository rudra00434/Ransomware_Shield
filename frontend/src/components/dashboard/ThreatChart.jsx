import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const ThreatChart = ({ data = [] }) => {
    return (
        <div className="w-full h-full min-h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
                <AreaChart
                    data={data}
                    margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                >
                    <defs>
                        <linearGradient id="colorCritical" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#FF2D55" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#FF2D55" stopOpacity={0} />
                        </linearGradient>
                        <linearGradient id="colorHigh" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#FF6B35" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#FF6B35" stopOpacity={0} />
                        </linearGradient>
                    </defs>
                    <XAxis dataKey="name" stroke="#4B5563" tick={{ fill: '#9CA3AF' }} />
                    <YAxis stroke="#4B5563" tick={{ fill: '#9CA3AF' }} />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#0A0E1A', borderColor: '#374151', borderRadius: '0.5rem' }}
                        itemStyle={{ color: '#E5E7EB' }}
                    />
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
                    <Area type="monotone" dataKey="Critical" stroke="#FF2D55" fillOpacity={1} fill="url(#colorCritical)" />
                    <Area type="monotone" dataKey="High" stroke="#FF6B35" fillOpacity={1} fill="url(#colorHigh)" />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
};

export default ThreatChart;
