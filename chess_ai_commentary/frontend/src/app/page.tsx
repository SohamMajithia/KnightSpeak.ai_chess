'use client'

import Link from 'next/link' 
import { useUser, UserButton } from '@clerk/nextjs'
import { Button } from '@/components/ui/button'
import { Cpu, Mic, Swords, ArrowRight, Play, Volume2, Globe, Sparkles, ChevronRight } from 'lucide-react'
import { useState, useEffect, useRef } from 'react'

// 🔊 Make sure you have a file at: frontend/public/audio/sample_commentary.wav
const SAMPLE_AUDIO_PATH = "/audio/sample_commentary.wav"; 

export default function Home() {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMounted, setIsMounted] = useState(false);
  const { isSignedIn, isLoaded, user } = useUser();

  // 1. Handle Hydration (Fixes the error)
  useEffect(() => {
    setIsMounted(true);
    // Reset play state when audio finishes
    if (audioRef.current) {
        audioRef.current.onended = () => setIsPlaying(false);
    }
  }, [isLoaded]);

  // 2. Handle Audio Playback
  const handleTogglePlayback = () => {
    if (!audioRef.current) return;

    if (isPlaying) {
        audioRef.current.pause();
    } else {
        audioRef.current.play();
    }
    setIsPlaying(!isPlaying);
  };

  // 3. Handle "View Demo" Button (Scrolls & Plays)
  const handleViewDemo = () => {
    const demoSection = document.getElementById('audio-demo-section');
    if (demoSection) {
        demoSection.scrollIntoView({ behavior: 'smooth' });
        // Optional: Auto-play when scrolling down
        if (!isPlaying && audioRef.current) {
            audioRef.current.play();
            setIsPlaying(true);
        }
    }
  };

  // Loading State
  if (!isLoaded) {
      return (
          <main className="min-h-screen flex items-center justify-center bg-slate-950">
              <Swords className="w-12 h-12 text-blue-500 animate-spin" />
          </main>
      )
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
      
      {/* Hidden Audio Element */}
      <audio ref={audioRef} src={SAMPLE_AUDIO_PATH} preload="auto" /> 

      {/* Navigation */}
      <nav className="border-b border-slate-800 sticky top-0 z-50 backdrop-blur-sm bg-slate-950/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Swords className="w-6 h-6 text-blue-500" />
            <span className="text-xl font-bold text-white">Knightspeaks</span>
          </div>
          <div className="flex items-center gap-4">
            {isSignedIn ? (
                <div className="flex items-center gap-4">
                    <Link href="/dashboard" className="text-slate-300 hover:text-white transition text-sm font-medium">Dashboard</Link>
                    <UserButton afterSignOutUrl="/"/>
                </div>
            ) : (
                <Link href="/sign-in">
                    <Button variant="outline" className="border-blue-500 text-blue-400 hover:bg-blue-500/10">
                        Login
                    </Button>
                </Link>
            )}
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-32">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div className="space-y-6">
            <h1 className="text-4xl md:text-6xl font-bold text-white leading-tight text-balance">
              Turn Your Chess Games into <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-blue-600">Epic Stories</span>
            </h1>
            <p className="text-lg md:text-xl text-slate-300 leading-relaxed text-pretty">
              The world's first AI commentator that analyzes your moves with the energy of a Grandmaster. Powered by Stockfish & advanced AI.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              
              {/* MAIN CTA BUTTONS */}
              <Link href={isSignedIn ? "/dashboard" : "/sign-up"} className="w-full sm:w-auto">
                <Button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 text-lg rounded-lg font-semibold flex items-center gap-2 w-full justify-center">
                  {isSignedIn ? "Go to Dashboard" : "Get Started Free"}
                  <ArrowRight className="w-5 h-5" />
                </Button>
              </Link>

              <Button 
                onClick={handleViewDemo} 
                variant="outline" 
                className="border-slate-600 text-slate-200 hover:bg-slate-800 px-8 py-3 text-lg rounded-lg font-semibold flex items-center gap-2 w-full sm:w-auto justify-center"
              >
                <Play className="w-5 h-5" />
                View Demo
              </Button>
            </div>
          </div>

          {/* Visual: Waveform Animation */}
          <div className="hidden md:flex items-center justify-center">
            <div className="relative w-full h-96 bg-gradient-to-b from-blue-500/10 to-blue-500/5 rounded-xl border border-blue-500/20 backdrop-blur-sm flex items-center justify-center overflow-hidden">
              <div className="absolute inset-0 flex items-center justify-center gap-1 opacity-60">
                {isMounted && [...Array(50)].map((_, i) => (
                  <div
                    key={i}
                    className="bg-blue-500 rounded-full"
                    style={{
                      width: '2px',
                      height: `${Math.sin(i / 10) * 60 + 80}px`,
                      animation: `pulse ${2 + (i % 3)}s ease-in-out infinite`,
                      animationDelay: `${i * 0.05}s`,
                    }}
                  />
                ))}
              </div>
              <Mic className="w-20 h-20 text-blue-500 z-10" />
              <style jsx>{`
                @keyframes pulse {
                  0%, 100% { opacity: 0.3; transform: scaleY(0.8); }
                  50% { opacity: 1; transform: scaleY(1); }
                }
              `}</style>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4 text-balance">How It Works</h2>
          <p className="text-lg text-slate-400">From your game to professional commentary in three simple steps</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {[
            { num: 1, title: 'Connect', desc: 'Link your Chess.com profile or upload your PGN file in seconds', icon: ArrowRight },
            { num: 2, title: 'Analyze', desc: 'Our AI engine finds brilliant moves, blunders, and key moments', icon: Cpu },
            { num: 3, title: 'Listen', desc: 'Get a downloadable MP3 with full voice commentary', icon: Volume2 },
          ].map((step, i) => (
            <div key={i} className="relative">
              <div className="bg-slate-800/50 border border-slate-700 rounded-xl p-8 backdrop-blur-sm hover:border-blue-500/50 transition">
                <div className="absolute -top-4 -left-4 w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                  {step.num}
                </div>
                <step.icon className="w-8 h-8 text-blue-400 mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">{step.title}</h3>
                <p className="text-slate-400">{step.desc}</p>
              </div>
              {i < 2 && (
                <div className="hidden md:block absolute top-1/2 -right-4 translate-y-1/2">
                  <ChevronRight className="w-6 h-6 text-blue-500/50" />
                </div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* Key Features Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <h2 className="text-4xl md:text-5xl font-bold text-white mb-16 text-center text-balance">Powerful Features Built for Champions</h2>

        <div className="grid md:grid-cols-2 gap-6">
          {[
            {
              title: 'Grandmaster Analysis',
              desc: 'Powered by Stockfish 16 with position evaluation and variation analysis',
              icon: Swords,
              color: 'from-blue-500/20 to-blue-600/20',
            },
            {
              title: 'Charismatic AI',
              desc: 'No robotic voices. Advanced AI adds personality, humor, and genuine excitement to your commentary',
              icon: Sparkles,
              color: 'from-purple-500/20 to-purple-600/20',
            },
            {
              title: 'Voice Cloning',
              desc: 'Upload your own voice or choose from professional commentators for your personal style',
              icon: Mic,
              color: 'from-orange-500/20 to-orange-600/20',
            },
            {
              title: 'Multi-Language Support',
              desc: 'English, Spanish, German, and French - analyze your games in your native language',
              icon: Globe,
              color: 'from-green-500/20 to-green-600/20',
            },
          ].map((feature, i) => (
            <div key={i} className={`bg-gradient-to-br ${feature.color} border border-slate-700 rounded-xl p-8 backdrop-blur-sm hover:border-blue-500/50 transition`}>
              <feature.icon className="w-10 h-10 text-blue-400 mb-4" />
              <h3 className="text-2xl font-bold text-white mb-2">{feature.title}</h3>
              <p className="text-slate-300">{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Audio Demo Section (With ID) */}
      <section id="audio-demo-section" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="bg-gradient-to-r from-blue-600/20 to-blue-500/10 border border-blue-500/30 rounded-2xl p-12 backdrop-blur-sm">
          <div className="flex flex-col md:flex-row items-center justify-between gap-8">
            <div className="flex-1">
              <h3 className="text-3xl font-bold text-white mb-3">Hear It Yourself</h3>
              <p className="text-slate-300 mb-6">
                Listen to our AI commentating a real chess game with energy, insight, and personality that brings every move to life.
              </p>
              <div className="flex items-center gap-4">
                <button
                  onClick={handleTogglePlayback}
                  className="bg-blue-600 hover:bg-blue-700 text-white rounded-full p-4 transition"
                >
                  {isPlaying ? <Volume2 className="w-6 h-6" /> : <Play className="w-6 h-6" />}
                </button>
                <div className="flex-1">
                  <p className="text-sm text-slate-400">Sample Commentary</p>
                  <div className="h-1 bg-slate-700 rounded-full mt-2 overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-blue-500 to-blue-600 transition-all duration-100"
                      style={{ width: isPlaying ? '100%' : '0%' }}
                    />
                  </div>
                </div>
              </div>
            </div>
            <div className="hidden lg:block">
              <Mic className="w-32 h-32 text-blue-500 opacity-20" />
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="bg-gradient-to-r from-blue-600 to-blue-500 rounded-2xl p-12 md:p-16 text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6 text-balance">Ready to Elevate Your Chess Game?</h2>
          <p className="text-lg text-blue-100 mb-8 max-w-2xl mx-auto">
            Get started free today and turn your chess games into epic, AI-powered commentary that you'll actually want to listen to.
          </p>
          <Link href={isSignedIn ? "/dashboard" : "/sign-up"} className="w-full sm:w-auto">
            <Button className="bg-white text-blue-600 hover:bg-slate-100 px-8 py-3 text-lg font-semibold rounded-lg">
              Start Free Trial
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="flex flex-col md:flex-row justify-between items-center gap-8">
            <div className="flex items-center gap-2">
              <Swords className="w-5 h-5 text-blue-500" />
              <span className="font-bold text-white">Knightspeaks</span>
            </div>
            <div className="flex gap-8 text-sm">
              <Link href="/" className="text-slate-400 hover:text-white transition">Home</Link>
              <Link href={isSignedIn ? "/dashboard" : "/sign-in"} className="text-slate-400 hover:text-white transition">
                Login
              </Link>
            </div>
            <p className="text-slate-500 text-sm">© 2025 Knightspeaks. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </main>
  )
}