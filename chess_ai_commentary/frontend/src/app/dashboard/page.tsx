"use client";

import { UserButton, useAuth, useUser } from "@clerk/nextjs";
import { useState } from "react";
import { CommentaryConfigModal } from "@/components/CommentaryConfigModal";
import { RefreshCw, Calendar, Mic, Search } from "lucide-react";
import { Sidebar } from "@/components/Sidebar"; // <-- Import the shared Sidebar

export default function DashboardPage() {
  const { isLoaded, userId, getToken } = useAuth();
  const { user } = useUser();
  
  // --- STATE ---
  const [games, setGames] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(""); 
  
  // Dynamic Username State
  const [chessUsername, setChessUsername] = useState("Hikaru"); 
  
  // Modal State - Stores the FULL game object now
  const [selectedGame, setSelectedGame] = useState<any | null>(null);

  if (!isLoaded || !userId) {
    return (
        <div className="flex h-screen items-center justify-center bg-slate-950 text-white">
            Loading...
        </div>
    );
  }

  const fetchRecentGames = async () => {
    if (!chessUsername.trim()) {
        alert("Please enter a Chess.com username first.");
        return;
    }

    setLoading(true);
    setGames([]); 
    
    try {
        const token = await getToken();
        const headers = { Authorization: `Bearer ${token}` };

        // 1. Get Archives
        setStatus(`Fetching archives for ${chessUsername}...`);
        const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000";
        const archiveRes = await fetch(
            `${backendUrl}/api/v1/games/archives/${chessUsername}`, 
            { headers }
        );
        
        if (!archiveRes.ok) throw new Error("Could not find user or archives.");
        
        const archiveData = await archiveRes.json();

        if (!archiveData.archives || archiveData.archives.length === 0) {
            alert("No game archives found for this user.");
            setLoading(false);
            setStatus("");
            return;
        }

        // 2. Get Last 3 Months (or all if less than 3)
        const archivesToFetch = archiveData.archives.slice(-3);
        const allGames: any[] = [];

        for (const archiveUrl of archivesToFetch) {
            const parts = archiveUrl.split('/');
            const year = parts[parts.length - 2];
            const month = parts[parts.length - 1];

            setStatus(`Fetching games from ${year}-${month}...`);
            const gamesRes = await fetch(
                `${backendUrl}/api/v1/games/by-month/${chessUsername}/${year}/${month}`,
                { headers }
            );
            const gamesData = await gamesRes.json();

            if (gamesData.games) {
                allGames.push(...gamesData.games);
            }
        }

        // Sort by most recent first
        allGames.sort((a, b) => b.end_time - a.end_time);
        setGames(allGames);

    } catch (error) {
        console.error("Error fetching games:", error);
        alert("Failed to fetch games. Check spelling or try again.");
    } finally {
        setLoading(false);
        setStatus("");
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-200 font-sans">
      
      {/* --- SHARED SIDEBAR --- */}
      <Sidebar />

      {/* --- MAIN CONTENT --- */}
      <main className="flex-1 md:ml-64 p-8">
        
        {/* Header */}
        <div className="max-w-5xl mx-auto mb-10">
            <h1 className="text-3xl font-bold text-white mb-2">Welcome back, {user?.firstName} 👋</h1>
            <p className="text-slate-400">Ready to analyze your latest masterpieces?</p>
        </div>

        <div className="max-w-5xl mx-auto space-y-8">
            
            {/* SEARCH CARD */}
            <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 shadow-lg">
                <h2 className="text-lg font-semibold mb-4 text-white">Connect Chess.com</h2>
                <div className="flex flex-col md:flex-row gap-4">
                    <div className="relative flex-1">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                        <input 
                            type="text"
                            value={chessUsername}
                            onChange={(e) => setChessUsername(e.target.value)}
                            placeholder="Enter Chess.com username"
                            className="w-full bg-slate-950 border border-slate-700 rounded-lg py-2.5 pl-10 pr-4 text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
                        />
                    </div>
                    <button 
                        onClick={fetchRecentGames}
                        disabled={loading}
                        className="bg-blue-600 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2 min-w-[160px]"
                    >
                        {loading ? (
                            <><RefreshCw className="w-4 h-4 animate-spin" /> Fetching...</>
                        ) : (
                            "Fetch Games"
                        )}
                    </button>
                </div>
                {status && <p className="mt-3 text-sm text-blue-400 animate-pulse">{status}</p>}
            </div>

            {/* GAMES GRID */}
            {games.length > 0 && (
                <div>
                    <h3 className="text-xl font-bold text-white mb-4">Recent Games</h3>
                    <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
                        {games.map((game, index) => (
                            <div key={index} className="bg-slate-900 p-5 rounded-xl border border-slate-800 hover:border-blue-500/50 transition-all flex flex-col justify-between h-full">
                                
                                {/* Card Header */}
                                <div className="flex justify-between items-start mb-4">
                                    <div className="text-xs text-slate-500 flex items-center gap-1">
                                        <Calendar className="w-3 h-3" />
                                        {new Date(game.end_time * 1000).toLocaleDateString()}
                                    </div>
                                    <span className={`text-[10px] font-bold px-2 py-1 rounded uppercase tracking-wider ${
                                        game.white.username.toLowerCase() === chessUsername.toLowerCase() 
                                            ? (game.white.result === 'win' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400')
                                            : (game.black.result === 'win' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400')
                                    }`}>
                                        {game.white.username.toLowerCase() === chessUsername.toLowerCase() 
                                            ? (game.white.result === 'win' ? 'Won' : 'Lost/Draw')
                                            : (game.black.result === 'win' ? 'Won' : 'Lost/Draw')
                                        }
                                    </span>
                                </div>

                                {/* Players */}
                                <div className="space-y-2 mb-6">
                                    <div className="flex justify-between items-center">
                                        <div className="flex items-center gap-2">
                                            <div className="w-2 h-2 rounded-full bg-slate-200"></div>
                                            <span className="text-sm font-medium text-slate-200">{game.white.username}</span>
                                        </div>
                                        <span className="text-xs text-slate-500">{game.white.rating}</span>
                                    </div>
                                    <div className="flex justify-between items-center">
                                        <div className="flex items-center gap-2">
                                            <div className="w-2 h-2 rounded-full bg-slate-600"></div>
                                            <span className="text-sm font-medium text-slate-200">{game.black.username}</span>
                                        </div>
                                        <span className="text-xs text-slate-500">{game.black.rating}</span>
                                    </div>
                                </div>

                                {/* Action */}
                                <button 
                                    onClick={() => setSelectedGame(game)}
                                    className="w-full bg-slate-800 text-slate-300 px-4 py-2.5 rounded-lg text-sm font-medium hover:bg-blue-600 hover:text-white transition-all flex items-center justify-center gap-2"
                                >
                                    <Mic className="w-4 h-4" />
                                    Generate Audio
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
      </main>

      {/* MODAL */}
      {selectedGame && (
        <CommentaryConfigModal
            isOpen={!!selectedGame}
            onClose={() => setSelectedGame(null)}
            game={selectedGame} // Passing the full game object
        />
      )}
    </div>
  );
}