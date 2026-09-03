import React from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { formatINR } from '../api'

export default function CashFlowChart({ data }) {
  return (
    <div className="card h-64">
      <h3 className="text-sm text-slate-500 mb-2">30-Day Cash Flow Forecast</h3>
      <ResponsiveContainer width="100%" height="85%">
        <LineChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="day" />
          <YAxis tickFormatter={(v) => `${v / 100000}L`} />
          <Tooltip formatter={(value) => formatINR(value)} />
          <Line type="monotone" dataKey="cash" stroke="#2563eb" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
