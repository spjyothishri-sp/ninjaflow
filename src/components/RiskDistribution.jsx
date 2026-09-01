import React from 'react'
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts'

const COLORS = ['#10b981', '#f59e0b', '#ef4444']

export default function RiskDistribution({ data }) {
  const pie = [
    { name: 'HEALTHY', value: data.healthy || 4 },
    { name: 'AT RISK', value: data.atRisk || 3 },
    { name: 'CRITICAL', value: data.critical || 2 },
  ]
  return (
    <div className="card h-64">
      <h3 className="text-sm text-slate-500 mb-2">Risk Distribution</h3>
      <ResponsiveContainer width="100%" height="85%">
        <PieChart>
          <Pie data={pie} dataKey="value" outerRadius={70} innerRadius={30}>
            {pie.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}
