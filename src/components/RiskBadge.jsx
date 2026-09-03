import React from 'react'

export default function RiskBadge({ level }) {
  const map = {
    HEALTHY: 'bg-green-100 text-green-800',
    'AT RISK': 'bg-yellow-100 text-yellow-800',
    CRITICAL: 'bg-red-100 text-red-800',
  }
  return <span className={`px-2 py-1 rounded-full text-xs font-semibold ${map[level] || 'bg-gray-100 text-gray-800'}`}>{level}</span>
}
