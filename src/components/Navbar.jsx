import React from 'react'

export default function Navbar() {
  return (
    <header className="border-b bg-white/50 backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold">NinjaFlow</h1>
          <p className="text-sm text-slate-500">Liquidity Control Tower</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="text-sm px-3 py-1 rounded-md bg-slate-100 hover:bg-slate-200">Demo Mode</button>
        </div>
      </div>
    </header>
  )
}
