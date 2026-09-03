import React from 'react'
import { NavLink } from 'react-router-dom'

const links = [
  { to: '/', label: 'Dashboard' },
  { to: '/entity/1', label: 'Risk Entities' },
  { to: '/financing', label: 'Financing' },
  { to: '/simulate', label: 'What-If Simulator' },
]

export default function Sidebar() {
  return (
    <aside className="hidden md:block w-64 border-r bg-white">
      <div className="h-full sticky top-0 p-4">
        <nav className="flex flex-col gap-2">
          {links.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              className={({ isActive }) =>
                `px-3 py-2 rounded-md text-sm hover:bg-slate-100 ${isActive ? 'bg-slate-100 font-medium' : ''}`
              }
            >
              {l.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </aside>
  )
}
