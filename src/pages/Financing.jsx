import React, { useEffect, useState } from 'react'
import FinancingCard from '../components/FinancingCard'
import BankOfferModal from '../components/BankOfferModal'
import { recommendFinancing, checkBankEligibility } from '../api'

export default function Financing() {
  const [rec, setRec] = useState(null)
  const [offer, setOffer] = useState(null)
  const [open, setOpen] = useState(false)

  useEffect(() => {
    recommendFinancing().then((r) => setRec(r))
  }, [])

  if (!rec) return <div>Loading financing...</div>

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-semibold mb-2">Financing Recommendation</h2>
      <p className="text-sm text-slate-500 mb-4">Review recommended financing and request a simulated bank offer.</p>

      <FinancingCard rec={rec} onGetOffer={async () => {
        const res = await checkBankEligibility({ requestedAmount: rec.recommendedAmount, duration: rec.durationDays })
        setOffer(res)
        setOpen(true)
      }} />

      <BankOfferModal open={open} onClose={() => setOpen(false)} offer={offer} onDisburse={() => {
        // mock side-effect: update offer status
        setOffer((o) => ({ ...o, status: 'DISBURSED' }))
      }} />
    </div>
  )
}
