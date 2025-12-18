export default function ChartSkeleton() {
    return (
        <div className="card h-full w-full bg-white p-6 rounded-xl shadow-sm border border-slate-100 animate-pulse">
            {/* Title Skeleton */}
            <div className="h-6 w-48 bg-slate-200 rounded mb-6"></div>

            {/* Chart Area Skeleton */}
            <div className="w-full h-[350px] flex items-end gap-2">
                {/* Y-Axis lines */}
                <div className="w-full h-full relative">
                    <div className="absolute left-0 right-0 top-0 h-px bg-slate-100"></div>
                    <div className="absolute left-0 right-0 top-1/4 h-px bg-slate-100"></div>
                    <div className="absolute left-0 right-0 top-2/4 h-px bg-slate-100"></div>
                    <div className="absolute left-0 right-0 top-3/4 h-px bg-slate-100"></div>
                    <div className="absolute left-0 right-0 bottom-0 h-px bg-slate-100"></div>

                    {/* Fake Chart Shape */}
                    <div className="absolute bottom-0 left-0 right-0 h-1/3 bg-slate-100 rounded-t-lg opacity-50"></div>
                    <div className="absolute bottom-0 left-1/4 right-0 h-1/2 bg-slate-100 rounded-t-lg opacity-50"></div>
                    <div className="absolute bottom-0 left-1/2 right-0 h-2/3 bg-slate-100 rounded-t-lg opacity-50"></div>
                </div>
            </div>
        </div>
    );
}
