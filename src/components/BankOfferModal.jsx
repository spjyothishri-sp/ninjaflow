import React, { useState } from 'react'

export default function BankOfferModal({ open, onClose, offer, onDisburse }) {
  const [status, setStatus] = useState(offer?.status || 'OFFERED')

  React.useEffect(() => {
    setStatus(offer?.status || 'OFFERED')
  }, [offer])

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div
        className="absolute inset-0 bg-black/40"
        onClick={onClose}
      ></div>

      <div className="relative bg-white rounded-lg shadow-lg w-full max-w-md p-6">
        <h2 className="text-lg font-semibold">
          Simulated Bank/NBFC Offer
        </h2>

        <div className="text-xs text-red-600 font-semibold mt-1">
          SIMULATED — DEMO ONLY
        </div>

        <div className="mt-4 space-y-2">
          <div>
            Eligibility:{' '}
            <span className="font-medium">
              {offer?.eligible ? 'Eligible' : 'Not Eligible'}
            </span>
          </div>

          <div>
            Approved Amount:{' '}
            <span className="font-medium">
              {offer?.approved_amount != null
                ? offer.approved_amount.toLocaleString('en-IN', {
                    style: 'currency',
                    currency: 'INR',
                    maximumFractionDigits: 0,
                  })
                : '-'}
            </span>
          </div>

          <div>
            Interest Rate:{' '}
            <span className="font-medium">
              {offer?.interest_rate != null
                ? `${offer.interest_rate}%`
                : '-'}
            </span>
          </div>

          <div>
            Duration:{' '}
            <span className="font-medium">
              {offer?.duration_days != null
                ? `${offer.duration_days} days`
                : '-'}
            </span>
          </div>

          <div>
            Status:{' '}
            <span
              className={`font-semibold ${
                status === 'DISBURSED'
                  ? 'text-green-600'
                  : 'text-sky-600'
              }`}
            >
              {status}
            </span>
          </div>

          {offer?.message && (
            <div className="text-sm text-slate-500 mt-2">
              {offer.message}
            </div>
          )}
        </div>

        <div className="mt-6 flex gap-3 justify-end">
          <button
            onClick={onClose}
            className="px-3 py-1 rounded border"
          >
            Close
          </button>

          <button
            onClick={() => setStatus('OFFERED')}
            className="px-3 py-1 rounded border"
          >
            Approve
          </button>

          <button
            onClick={() => {
              setStatus('DISBURSED')
              onDisburse && onDisburse()
            }}
            className="px-3 py-1 rounded bg-green-600 text-white"
          >
            Disburse
          </button>
        </div>
      </div>
    </div>
  )
}