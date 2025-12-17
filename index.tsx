import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';

const triggerBreachAlarm = () => {
    try {
        const audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)();
        const oscillator = audioCtx.createOscillator();
        oscillator.type = 'sawtooth';
        oscillator.frequency.setValueAtTime(440, audioCtx.currentTime);
        oscillator.connect(audioCtx.destination);
        oscillator.start();
        oscillator.stop(audioCtx.currentTime + 0.1);
    } catch (e) { console.error("Audio blocked by browser policy. Interaction required.", e); }
};

const PurpleGuardDashboard = () => {
    const [metadata, setMetadata] = useState({ total_kills: 0, findings: [] });
    const [lastKillCount, setLastKillCount] = useState(0);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                // Pointing to the metadata.json in your root
                const response = await fetch('/metadata.json');
                if (!response.ok) throw new Error("Metadata not found");
                const data = await response.json();
                setMetadata(data);

                if (data.total_kills > lastKillCount) {
                    if (lastKillCount !== 0) triggerBreachAlarm();
                    setLastKillCount(data.total_kills);
                }
            } catch (err) {
                console.log("Waiting for Omnibus Engine data...");
            }
        };

        const interval = setInterval(fetchStats, 2000);
        fetchStats(); 
        return () => clearInterval(interval);
    }, [lastKillCount]);

    return (
        <div className="p-4 md:p-8 min-h-screen">
            <header className="mb-8 border-b border-red-900 pb-4">
                <h1 className="text-2xl md:text-4xl font-bold text-red-600 tracking-tighter">
                    PURPLEGUARD v3.2 <span className="text-white text-sm font-mono ml-2">[ACTIVE_SWARM_MODE]</span>
                </h1>
            </header>

            {metadata.ai_analysis && (
                <div className="mb-6 bg-red-950/20 border border-red-500 p-4 rounded-sm animate-pulse">
                    <h3 className="text-red-500 text-xs font-bold uppercase mb-2">Hephaestus Intelligence Report</h3>
                    <p className="text-white text-xs leading-relaxed font-mono whitespace-pre-wrap">{metadata.ai_analysis}</p>
                </div>
            )}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-slate-900 border border-red-500/30 p-6 rounded-sm">
                    <h3 className="text-red-400 text-xs uppercase mb-2">Total Confirmed Kills</h3>
                    <div className="text-6xl font-black text-red-500">{metadata.total_kills}</div>
                    <div className="mt-4 h-1 bg-red-900/50 w-full"><div className="h-1 bg-red-500 w-full animate-pulse"></div></div>
                </div>

                <div className="md:col-span-2 bg-slate-900 border border-green-500/30 p-4 rounded-sm">
                    <h3 className="text-green-400 text-xs uppercase mb-4 border-b border-green-900 pb-2">Nexus Feed (Latest Breaches)</h3>
                    <div className="space-y-2 max-h-96 overflow-y-auto font-mono text-[10px] md:text-xs">
                        {metadata.findings?.length > 0 ? (
                            [...metadata.findings].reverse().map((f, i) => (
                                <div key={i} className="flex justify-between border-b border-slate-800 pb-1">
                                    <span className="text-red-400 font-bold">[{f.type}]</span>
                                    <span className="text-slate-400 truncate ml-4">{f.target}</span>
                                </div>
                            ))
                        ) : (
                            <div className="text-slate-600 animate-pulse italic">Awaiting telemetry from omnibus.py...</div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

const container = document.getElementById('root');
if (container) {
    const root = createRoot(container);
    root.render(<PurpleGuardDashboard />);
}
