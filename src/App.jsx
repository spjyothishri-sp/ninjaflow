import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import EntityPage from './pages/EntityPage'
import Financing from './pages/Financing'
import Simulator from './pages/Simulator'
import Sidebar from './components/Sidebar'
import Navbar from './components/Navbar'

export default function App() {
  return (
    <div className="min-h-screen flex">
      <Sidebar />
      <div className="flex-1">
        <Navbar />
        <main className="p-4 md:p-6 lg:p-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/entity/:id" element={<EntityPage />} />
            <Route path="/financing" element={<Financing />} />
            <Route path="/simulate" element={<Simulator />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </div>
  )
}
