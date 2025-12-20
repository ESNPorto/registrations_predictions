"use client";

import { useEffect } from 'react';

export default function NotebookPage() {
    useEffect(() => {
        const originalPadding = document.body.style.paddingTop;
        const originalMargin = document.body.style.margin;
        const originalOverflow = document.body.style.overflow;
        
        document.body.style.paddingTop = '0';
        document.body.style.margin = '0';
        document.body.style.overflow = 'hidden';
        
        return () => {
            document.body.style.paddingTop = originalPadding;
            document.body.style.margin = originalMargin;
            document.body.style.overflow = originalOverflow;
        };
    }, []);
    
    return (
        <div style={{ 
            position: 'fixed',
            top: 'var(--nav-height)',
            left: 0,
            right: 0,
            bottom: 0,
            padding: 0,
            margin: 0,
            overflow: 'hidden'
        }}>
            <iframe
                src="/notebook.html"
                style={{
                    width: '100%',
                    height: '100%',
                    border: 'none',
                    display: 'block',
                    margin: 0,
                    padding: 0,
                }}
                title="Jupyter Notebook"
            />
        </div>
    );
}