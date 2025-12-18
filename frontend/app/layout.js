import './globals.css';
import Navbar from '../components/Navbar';

export const metadata = {
    title: 'ESN Porto Predictions',
    description: 'Forecast membership registrations for ESN Porto.',
    icons: {
        icon: '/favicon.png',
    },
};

export default function RootLayout({ children }) {
    return (
        <html lang="en" suppressHydrationWarning>
            <body className="antialiased bg-slate-50 text-slate-900 pt-16">
                <Navbar />
                {children}
            </body>
        </html>
    );
}
