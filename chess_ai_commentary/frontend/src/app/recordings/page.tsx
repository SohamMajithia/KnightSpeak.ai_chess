"use client"
import Link from "next/link"
import { useState, useEffect } from "react"
import { Mic, Download, Loader2 } from "lucide-react"
import { useUser } from "@clerk/nextjs"
import { Sidebar } from "@/components/Sidebar" // <-- Importing the Shared Sidebar

// --- Component Types ---
interface Recording {
  id: string
  player_white: string
  player_black: string
  created_at: string
  audio_url: string
}

// --- Component: Recording Card ---
function RecordingCard({ recording }: { recording: Recording }) {
  const handleDownload = () => {
    const link = document.createElement("a")
    link.href = recording.audio_url
    link.download = `${recording.player_white}_vs_${recording.player_black}_commentary.wav`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  const formattedDate = new Date(recording.created_at).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 hover:border-blue-500/50 transition-all shadow-sm">
      
      {/* Title and Date */}
      <div className="mb-5">
        <h3 className="text-lg font-bold text-white mb-2 flex items-center gap-2">
           <span className="bg-slate-800 p-1 rounded text-blue-400"><Mic className="w-4 h-4" /></span>
           {recording.player_white} <span className="text-slate-500 text-sm font-normal">vs</span> {recording.player_black}
        </h3>
        <p className="text-xs text-slate-500 uppercase tracking-wider font-medium">
            Generated: {formattedDate}
        </p>
      </div>

      {/* Audio Player */}
      <div className="mb-5 border border-slate-700 rounded-lg overflow-hidden bg-black/20">
        <audio controls className="w-full h-10" controlsList="nodownload">
          <source src={recording.audio_url} type="audio/wav" /> 
          Your browser does not support the audio element.
        </audio>
      </div>

      {/* Download Button */}
      <button
        onClick={handleDownload}
        className="w-full bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium py-2.5 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors border border-slate-700 hover:border-slate-600"
      >
        <Download className="w-4 h-4" />
        Download File
      </button>
    </div>
  )
}

// --- Main Page Component ---
export default function RecordingsPage() {
  const [recordings, setRecordings] = useState<Recording[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const { user, isLoaded } = useUser()

  useEffect(() => {
    if (!isLoaded || !user) return;

    const fetchRecordings = async () => {
      try {
        // Fetch data from your FastAPI Backend
        const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000";
        const response = await fetch(`${backendUrl}/api/v1/recordings/${user.id}`)

        if (!response.ok) {
          throw new Error("Failed to fetch recordings")
        }

        const data = await response.json()
        let list = [];
        if (data) {
            if (Array.isArray(data)) {
                list = data;
            } else if (data.recordings && Array.isArray(data.recordings)) {
                list = data.recordings;
            }
        }
        // Handle both formats: list directly or { recordings: [...] }
        setRecordings(list)
        
      } catch (error) {
        console.error("Error fetching recordings:", error)
        setRecordings([])
      } finally {
        setIsLoading(false)
      }
    }

    fetchRecordings()
  }, [isLoaded, user])

  if (!isLoaded) {
     return <div className="flex h-screen bg-slate-950 items-center justify-center text-white">Loading...</div>
  }

  return (
    <div className="flex min-h-screen bg-slate-950 font-sans text-slate-200">
      
      {/* Shared Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 md:ml-64">
        
        {/* Top Bar */}
        <div className="border-b border-slate-800 bg-slate-950/80 backdrop-blur-sm sticky top-0 z-40 px-8 py-6">
          <h1 className="text-3xl font-bold text-white tracking-tight">Audio Library 🎧</h1>
          <p className="text-slate-400 mt-1">Listen to your past game analyses.</p>
        </div>

        {/* Content Area */}
        <div className="p-8">
          {isLoading ? (
            // Loading Skeleton
            <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl p-6 animate-pulse h-64">
                   <div className="h-6 bg-slate-800 rounded w-3/4 mb-4"></div>
                   <div className="h-4 bg-slate-800 rounded w-1/2 mb-8"></div>
                   <div className="h-12 bg-slate-800 rounded mb-4"></div>
                   <div className="h-10 bg-slate-800 rounded"></div>
                </div>
              ))}
            </div>
          ) : recordings.length === 0 ? (
            // Empty State
            <div className="flex flex-col items-center justify-center py-20 text-center border-2 border-dashed border-slate-800 rounded-xl bg-slate-900/50">
              <div className="w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center mb-4">
                  <Mic className="w-8 h-8 text-slate-500" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">No recordings yet</h3>
              <p className="text-slate-400 max-w-md mb-6">
                Go to the Dashboard to generate your first AI commentary!
              </p>
              <Link href="/dashboard" className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-500 transition">
                Go to Dashboard
              </Link>
            </div>
          ) : (
            // Recordings Grid
            <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-6">
              {recordings.map((recording) => (
                <RecordingCard key={recording.id} recording={recording} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}