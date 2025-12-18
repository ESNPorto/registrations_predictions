"use client";

export default function Navbar() {
    return (
        <nav className="nav-container">
            <div className="nav-content">
                {/* Left Side */}
                <div className="nav-brand">
                    <div className="flex items-center" style={{ height: '40px' }}>
                        <img
                            src="/logo.png"
                            alt="ESN Porto"
                            className="h-full w-auto object-contain"
                        />
                    </div>
                    <div className="h-6 w-[1px] bg-slate-200" style={{ margin: '0 10px' }}></div>
                    <h1 className="nav-title">Registrations Forecast</h1>
                </div>
            </div>
        </nav>
    );
}