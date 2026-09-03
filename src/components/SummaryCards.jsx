import React from 'react'
import { formatINR } from '../api'

export default function SummaryCards({ summary }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div className="card">
        <h3 className="text-sm text-slate-500">Total Cash</h3>
        <div className="text-2xl font-semibold">{formatINR(summary.totalCash)}</div>
      </div>
      <div className="card">
        <h3 className="text-sm text-slate-500">Expected Collections</h3>
        <div className="text-2xl font-semibold">{formatINR(summary.expectedCollections)}</div>
      </div>
      <div className="card">
        <h3 className="text-sm text-slate-500">Upcoming Payments</h3>
        <div className="text-2xl font-semibold">{formatINR(summary.upcomingPayments)}</div>
      </div>
      <div className="card">
        <h3 className="text-sm text-slate-500">Projected Gap</h3>
        <div className="text-2xl font-semibold text-red-600">{formatINR(summary.projectedGap)}</div>
      </div>
    </div>
  )
}
