import React from 'react'
import { formatINR } from '../api'

export default function FinancingCard({ rec, onGetOffer }) {
  return (
    <div className="card">
      <h3 className="text-sm text-slate-500">Financing Recommendation</h3>
      <div className="mt-2">
        <div className="text-2xl font-semibold">{formatINR(rec.recommendedAmount)}</div>
        <div className="text-sm text-slate-500">Duration: {rec.durationDays} days</div>
        <div className="mt-2 text-sm">Priority: <span className="font-semibold">{rec.priority}</span></div>
        <p className="text-sm text-slate-600 mt-2">{rec.reason}</p>
        <div className="mt-4">
          <button onClick={onGetOffer} className="px-4 py-2 bg-sky-600 text-white rounded hover:bg-sky-700">Get Bank Offer</button>
        </div>
      </div>
    </div>
  )
}
