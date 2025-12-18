
"use client";

export default function PredictionsTable({ forecast }) {
    if (!forecast || forecast.length === 0) return null;

    const getStatus = (count) => {
        if (count > 150) return { label: 'Peak Demand', className: 'badge-peak' };
        if (count > 50) return { label: 'Normal', className: 'badge-normal' };
        return { label: 'Low Activity', className: 'badge-low' };
    };

    return (
        <div className="card bg-white overflow-hidden">
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-bold text-slate-900">Upcoming Schedule</h2>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full">
                    <thead>
                        <tr className="bg-slate-50/50">
                            <th>Week Beginning</th>
                            <th>Predicted Count</th>
                            <th>Confidence Range</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {forecast.map((item, idx) => {
                            const status = getStatus(item.prediction);
                            const weekEnding = new Date(item.week_ending);
                            const weekBeginning = new Date(weekEnding);
                            weekBeginning.setDate(weekEnding.getDate() - 6);

                            return (
                                <tr key={idx} className="hover:bg-slate-50 transition-colors group">
                                    <td className="font-medium text-slate-700">
                                        {weekBeginning.toLocaleDateString('en-GB', { year: 'numeric', month: 'long', day: 'numeric' })}
                                    </td>
                                    <td>
                                        <span className="font-bold text-slate-900 text-base">{item.prediction}</span>
                                    </td>
                                    <td className="text-slate-500 text-sm">
                                        {item.confidence_lower} - {item.confidence_upper}
                                    </td>
                                    <td>
                                        <span className={`badge ${status.className}`}>
                                            {status.label}
                                        </span>
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
