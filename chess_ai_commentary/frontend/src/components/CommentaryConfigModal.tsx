"use client"

import React, { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Mic, User, Download, X, Play, Loader2 } from "lucide-react"
import { useUser } from "@clerk/nextjs" // <-- Import Clerk hook

type ModalState = "config" | "processing" | "success"

interface CommentaryConfigModalProps {
  isOpen: boolean
  onClose: () => void
  game: any // <-- Accepts the full game object now
}

const statusMessages = [
  "Connecting to Stockfish Engine...",
  "Analyzing Board Positions...",
  "Sending Analysis to Gemini AI...",
  "Drafting Commentary Script...",
  "Synthesizing Voice Audio...",
  "Finalizing Audio File (Uploading to Cloud)..."
]

export function CommentaryConfigModal({ isOpen, onClose, game }: CommentaryConfigModalProps) {
  const { user } = useUser(); // <-- Get the current user
  const [modalState, setModalState] = useState<ModalState>("config")
  const [language, setLanguage] = useState("English")
  const [voiceType, setVoiceType] = useState<"standard" | "custom">("standard")
  const [voiceFile, setVoiceFile] = useState<File | null>(null)
  
  const [progress, setProgress] = useState(0)
  const [currentStatusIndex, setCurrentStatusIndex] = useState(0)
  const [audioUrl, setAudioUrl] = useState<string | null>(null)
  
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleStartGeneration = async () => {
    if (!user) {
        alert("You must be logged in.");
        return;
    }

    setModalState("processing")
    setProgress(5)
    setCurrentStatusIndex(0)

    const statusInterval = setInterval(() => {
      setCurrentStatusIndex((prev) => (prev + 1) % statusMessages.length)
    }, 4000)

    try {
        console.log("🚀 Sending Request to Backend...");

        // --- NEW: Construct the payload with all required data ---
        const payload = {
            pgn: game.pgn,
            language: language,
            user_id: user.id, // <-- Clerk User ID
            player_white: game.white.username,
            player_black: game.black.username
        };

        const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000";
        const response = await fetch(`${backendUrl}/api/v1/generate-commentary`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `Backend error: ${response.statusText}`);
        }

        const data = await response.json();
        console.log("✅ Backend Response:", data);

        if (data.audio_url) {
            setProgress(100);
            setAudioUrl(data.audio_url); // This will now be a Supabase URL!
            
            setTimeout(() => {
                setModalState("success");
                clearInterval(statusInterval);
            }, 500);
        } else {
             throw new Error("No audio URL returned");
        }

    } catch (error) {
        console.error("❌ Generation Failed:", error);
        alert(`Failed: ${error}`);
        setModalState("config");
        clearInterval(statusInterval);
    }
  }

  // ... (Keep handleFileUpload, handleDownload, handleClose exactly as they were) ...
  // ... (Copy the rest of the UI render code exactly as it was in the previous version) ...
  
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file && file.size <= 5 * 1024 * 1024) {
      setVoiceFile(file)
    } else {
        alert("File too large. Max 5MB.");
    }
  }

  const handleDownload = () => {
    if (!audioUrl) return;
    const link = document.createElement("a")
    link.href = audioUrl
    link.download = `commentary_${game.white.username}_vs_${game.black.username}.wav`
    document.body.appendChild(link);
    link.click()
    document.body.removeChild(link);
  }

  const handleClose = () => {
    if (modalState !== "processing") {
        setTimeout(() => {
            setModalState("config")
            setAudioUrl(null)
            setProgress(0)
        }, 200);
        onClose();
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="bg-slate-900 border-slate-800 text-white max-w-md">
        {modalState === "config" && (
          <>
            <DialogHeader>
              <DialogTitle className="text-white">Configure Commentary</DialogTitle>
            </DialogHeader>
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Language</label>
                <select value={language} onChange={(e) => setLanguage(e.target.value)} className="w-full px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-blue-500 transition">
                  <option>English</option>
                  <option>Spanish</option>
                  <option>French</option>
                  <option>German</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-3">Voice Option</label>
                <div className="space-y-3">
                  <button onClick={() => { setVoiceType("standard"); setVoiceFile(null); }} className={`w-full p-4 rounded-lg border-2 transition flex items-center gap-3 ${voiceType === "standard" ? "border-blue-500 bg-blue-500/10" : "border-slate-700 bg-slate-800/50 hover:border-slate-600"}`}>
                    <div className="flex-1 text-left">
                      <Mic className="w-5 h-5 mb-1 text-blue-400" />
                      <p className="font-medium text-white">Professional Commentator</p>
                      <p className="text-xs text-slate-400">High-quality AI voice (Claribel)</p>
                    </div>
                    <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${voiceType === "standard" ? "border-blue-500 bg-blue-500" : "border-slate-600"}`}>
                      {voiceType === "standard" && <div className="w-2 h-2 bg-white rounded-full" />}
                    </div>
                  </button>
                  <button onClick={() => setVoiceType("custom")} className={`w-full p-4 rounded-lg border-2 transition flex items-center gap-3 ${voiceType === "custom" ? "border-blue-500 bg-blue-500/10" : "border-slate-700 bg-slate-800/50 hover:border-slate-600"}`}>
                    <div className="flex-1 text-left">
                      <User className="w-5 h-5 mb-1 text-blue-400" />
                      <p className="font-medium text-white">Clone My Voice</p>
                      <p className="text-xs text-slate-400">Upload a sample (.wav)</p>
                    </div>
                    <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${voiceType === "custom" ? "border-blue-500 bg-blue-500" : "border-slate-600"}`}>
                      {voiceType === "custom" && <div className="w-2 h-2 bg-white rounded-full" />}
                    </div>
                  </button>
                </div>
              </div>
              {voiceType === "custom" && (
                <div onClick={() => fileInputRef.current?.click()} className="border-2 border-dashed border-slate-700 rounded-lg p-6 text-center cursor-pointer hover:border-blue-500 transition bg-slate-800/30">
                  <input ref={fileInputRef} type="file" accept=".wav" onChange={handleFileUpload} className="hidden" />
                  <p className="text-sm font-medium text-white mb-1">{voiceFile ? voiceFile.name : "Click to upload or drag & drop"}</p>
                  <p className="text-xs text-slate-400">Max 5MB • WAV format</p>
                </div>
              )}
              <div className="flex gap-3 pt-4">
                <Button variant="outline" onClick={handleClose} className="flex-1 border-slate-700 text-slate-300 hover:bg-slate-800 bg-transparent">Cancel</Button>
                <Button onClick={handleStartGeneration} className="flex-1 bg-blue-600 hover:bg-blue-700 text-white">Start Generation</Button>
              </div>
            </div>
          </>
        )}
        {modalState === "processing" && (
          <>
            <DialogHeader><DialogTitle className="text-white">Generating Commentary...</DialogTitle></DialogHeader>
            <div className="space-y-6 py-4">
              <div>
                <div className="flex items-center justify-between mb-2"><p className="text-sm font-medium text-slate-300">Progress</p><p className="text-sm font-semibold text-blue-400">{Math.round(progress)}%</p></div>
                <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden"><div className="h-full bg-gradient-to-r from-blue-600 to-blue-500 transition-all duration-500" style={{ width: `${progress}%` }} /></div>
              </div>
              <div className="text-center py-8">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-blue-500/20 mb-4"><Loader2 className="w-6 h-6 text-blue-400 animate-spin" /></div>
                <p className="text-sm font-medium text-slate-300 animate-pulse">{statusMessages[currentStatusIndex]}</p>
                <p className="text-xs text-slate-500 mt-2">This can take 1-2 minutes on a CPU</p>
              </div>
            </div>
          </>
        )}
        {modalState === "success" && audioUrl && (
          <>
            <DialogHeader><DialogTitle className="text-white flex items-center gap-2">Commentary Ready!</DialogTitle></DialogHeader>
            <div className="space-y-6 py-4">
              <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
                <p className="text-xs text-slate-400 mb-2 uppercase tracking-wider font-semibold">Preview Audio</p>
                <audio controls className="w-full h-10" src={audioUrl}>Your browser does not support the audio element.</audio>
              </div>
              <div className="flex gap-3">
                <Button onClick={handleDownload} className="flex-1 bg-blue-600 hover:bg-blue-700 text-white flex items-center justify-center gap-2"><Download className="w-4 h-4" />Download MP3</Button>
                <Button onClick={handleClose} className="flex-1 bg-slate-800 hover:bg-slate-700 text-white flex items-center justify-center gap-2"><X className="w-4 h-4" />Close</Button>
              </div>
            </div>
          </>
        )}
      </DialogContent>
    </Dialog>
  )
}