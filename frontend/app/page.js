"use client";

import { useEffect, useState } from 'react';
import { fetchPrediction } from '../lib/api';

import ForecastTimeline from '../components/ForecastTimeline';
import PredictionsTable from '../components/PredictionsTable';

export default function Home() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function loadData() {
            const result = await fetchPrediction();
            setData(result);
            setLoading(false);
        }
        loadData();
    }, []);

    // Loading state handled by components

    // Dead code analysis shows these vars are unused in render, but wrapping in check to prevent crash if data is null
    if (data) {
        const currentForecast = data.forecast[0];
        const lastHistory = data.history[data.history.length - 1];
        const lastWeekActual = lastHistory ? lastHistory.registrations : 0;

        let weekRange = '';
        if (currentForecast) {
            const d = new Date(currentForecast.week_ending);
            d.setDate(d.getDate() - 6);
            weekRange = `Week of ${d.toLocaleDateString('en-GB')}`;
        }
    }

    return (
        <main className="min-h-screen p-8 bg-slate-50">
            <div className="container mx-auto pt-8">

                {/* Header moved to Navbar */}

                <div className="w-full mb-16 h-[500px]" style={{ marginBottom: '2em' }}>
                    <ForecastTimeline history={data?.history} forecast={data?.forecast} />
                </div>

                {/* Bottom Section - Table */}
                <div className="w-full">
                    <PredictionsTable forecast={data?.forecast} />
                </div>

            </div>
        </main>
    );
}