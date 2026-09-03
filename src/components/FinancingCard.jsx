import React from 'react'
import { formatINR } from '../api'

export default function FinancingCard({ rec, onGetOffer }) {
  const recommendation = rec?.recommendation

  if (!recommendation) {
    return (
      <div className="card">
        <p className="text-sm text-red-600">
          Financing recommendation is not available.
        </p>
      </div>
    )
  }

  return (
    <div className="card">
      <h3 className="text-sm text-slate-500">Financing Recommendation</h3>

      <div className="mt-2">
        <div className="text-2xl font-semibold">
          {formatINR(recommendation.recommended_amount)}
        </div>

        <div className="text-sm text-slate-500">
          Duration: {recommendation.duration_days} days
        </div>

        <div className="mt-2 text-sm">
          Priority:{' '}
          <span className="font-semibold">
            {recommendation.priority}
          </span>
        </div>

        <p className="text-sm text-slate-600 mt-2">
          {recommendation.reason}
        </p>

        {rec.remaining_gap > 0 && (
          <div className="mt-3 text-sm text-red-600">
            Remaining Funding Gap:{' '}
            <span className="font-semibold">
              {formatINR(rec.remaining_gap)}
            </span>
          </div>
        )}

        <div className="mt-4">
          <button
            onClick={onGetOffer}
            className="px-4 py-2 bg-sky-600 text-white rounded hover:bg-sky-700"
          >
            Get Bank Offer
          </button>
        </div>
      </div>
    </div>
  )
}