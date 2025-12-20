"use client";

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navbar() {
    const pathname = usePathname();
    
    return (
        <nav className="nav-container">
            <div className="nav-content">
                {/* Left Side */}
                <div className="nav-brand">
                    <img 
                        src="/logo.png" 
                        alt="ESN Porto" 
                        style={{ height: '40px', width: 'auto' }}
                    />
                    <div className="nav-title">Registrations Forecast</div>
                </div>

                {/* Right Side - Navigation Links */}
                <div className="nav-links">
                    <Link 
                        href="/" 
                        className={`nav-link ${pathname === '/' ? 'nav-link-active' : ''}`}
                    >
                        Dashboard
                    </Link>
                    <Link 
                        href="/notebook" 
                        className={`nav-link ${pathname === '/notebook' ? 'nav-link-active' : ''}`}
                    >
                        View Notebook
                    </Link>
                </div>
            </div>
        </nav>
    );
}