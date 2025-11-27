"use client"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { LayoutDashboard, FileAudio, Settings, Swords, User } from "lucide-react"
import { UserButton, useUser } from "@clerk/nextjs"

export function Sidebar() {
  const pathname = usePathname()
  const { user } = useUser()

  const navItems = [
    { href: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
    { href: "/recordings", icon: FileAudio, label: "My Recordings" },
    { href: "/settings", icon: Settings, label: "Settings" },
  ]

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-950 flex-col hidden md:flex fixed h-full">
      <div className="p-6 border-b border-slate-800">
        <div className="flex items-center gap-2 font-bold text-white text-xl">
          <Swords className="w-6 h-6 text-blue-500" />
          <span>Knightspeaks</span>
        </div>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link
              key={item.label}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition ${
                isActive 
                  ? "bg-blue-500/10 text-blue-400 border border-blue-500/20" 
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-900"
              }`}
            >
              <item.icon className="w-5 h-5" />
              {item.label}
            </Link>
          )
        })}
      </nav>

      <div className="p-4 border-t border-slate-800">
         <div className="flex items-center gap-3 px-2">
            <UserButton afterSignOutUrl="/" />
            <div className="flex flex-col">
               <span className="text-sm font-medium text-white truncate w-32">
                 {user?.fullName || user?.username}
               </span>
               <span className="text-xs text-slate-500">Free Plan</span>
            </div>
         </div>
      </div>
    </aside>
  )
}