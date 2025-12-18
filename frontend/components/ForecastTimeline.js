"use client";

import {
    AreaChart,
    Area,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer
} from 'recharts';
import ChartSkeleton from './ChartSkeleton';

import { useState, useEffect } from 'react';

export default function ForecastTimeline({ history, forecast }) {
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
    }, []);

    if (!history || !forecast) return <ChartSkeleton />;
    if (!mounted) return <ChartSkeleton />;

    console.log('History:', history.length);
    console.log('Forecast:', forecast.length);

    // Process data for Recharts
    // Combined array of history + forecast
    // We need to format it so it's a single timeline.

    // History data points
    const historyPoints = history.map(h => {
        const d = new Date(h.week_ending);
        d.setDate(d.getDate() - 6); // "Week Beginning"
        return {
            date: d.toLocaleDateString('en-GB', { month: 'short', day: 'numeric' }),
            fullDate: d,
            registrations: h.registrations,
            prediction: null,
            lower: null,
            upper: null,
            isForecast: false
        };
    });

    // Forecast data points
    const forecastPoints = forecast.map(f => {
        const d = new Date(f.week_ending);
        d.setDate(d.getDate() - 6); // "Week Beginning"
        return {
            date: d.toLocaleDateString('en-GB', { month: 'short', day: 'numeric' }),
            fullDate: d,
            registrations: null,
            prediction: f.prediction,
            lower: f.confidence_lower,
            upper: f.confidence_upper,
            range: [f.confidence_lower, f.confidence_upper],
            isForecast: true
        };
    });

    // Combine history and forecast data
    const data = [...historyPoints, ...forecastPoints];

    const CustomTooltip = ({ active, payload, label }) => {
        if (active && payload && payload.length) {
            const isPred = payload[0].payload.isForecast;
            return (
                <div className="bg-white p-4 border border-slate-100 shadow-xl rounded-lg">
                    <p className="text-slate-500 text-xs mb-1">{label}</p>
                    {payload.map((entry, index) => {
                        if (entry.value === null) return null;
                        return (
                            <div key={index} className="flex items-center gap-2 mb-1">
                                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.color }}></div>
                                <span className="text-slate-600 font-medium text-sm">
                                    {entry.name}: {entry.value}
                                </span>
                            </div>
                        );
                    })}
                    {isPred && (
                        <div className="mt-1 pt-1 border-t border-slate-100">
                            <p className="text-xs text-slate-400">Confidence: High</p>
                        </div>
                    )}
                </div>
            );
        }
        return null;
    };

    return (
        <div className="card h-full w-full bg-white p-6 rounded-xl shadow-sm border border-slate-100">
            <div className="w-full" style={{ height: '400px' }}>
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart
                        data={data}
                        margin={{
                            top: 10,
                            right: 30,
                            left: 0,
                            bottom: 0,
                        }}
                    >
                        <defs>
                            <linearGradient id="colorPrediction" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#2E3192" stopOpacity={0.2} />
                                <stop offset="95%" stopColor="#2E3192" stopOpacity={0} />
                            </linearGradient>
                            <linearGradient id="colorHistory" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#94a3b8" stopOpacity={0.2} />
                                <stop offset="95%" stopColor="#94a3b8" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                        <XAxis
                            dataKey="date"
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: '#64748b', fontSize: 12 }}
                            dy={10}
                            minTickGap={30}
                        />
                        <YAxis
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: '#64748b', fontSize: 12 }}
                            dx={-10}
                        />
                        <Tooltip content={<CustomTooltip />} />

                        {/* Historical Line */}
                        <Area
                            type="monotone"
                            dataKey="registrations"
                            name="Historical"
                            stroke="#94a3b8"
                            strokeWidth={3}
                            fill="url(#colorHistory)"
                            activeDot={{ r: 6, strokeWidth: 0 }}
                        />

                        {/* Prediction Line */}
                        <Area
                            type="monotone"
                            dataKey="prediction"
                            name="Forecast"
                            stroke="#2E3192"
                            strokeWidth={3}
                            fill="url(#colorPrediction)"
                            activeDot={{ r: 6, strokeWidth: 0 }}
                            animationDuration={1500}
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}