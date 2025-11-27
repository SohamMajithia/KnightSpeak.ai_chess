import type { Metadata } from 'next'
import { Inter } from "next/font/google"; 
import './globals.css'
import { ClerkProvider } from '@clerk/nextjs' // <-- CRITICAL IMPORT

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: 'Knightspeaks - Chess AI Commentary',
  description: 'The world\'s first AI commentator that analyzes your chess moves with the energy of a Grandmaster.',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    // 1. This Wrapper is REQUIRED for Clerk to work
    <ClerkProvider>
      <html lang="en" className="dark">
        <body className={inter.className}>
          {children}
        </body>
      </html>
    </ClerkProvider>
  )
}