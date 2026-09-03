import React, { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import FinancingCard from '../components/FinancingCard'
import BankOfferModal from '../components/BankOfferModal'
import { simulate, recommendFinancing } from '../api'

export default function Financing() {
  const [searchParams] = useSearchParams()
  const entityId = searchParams.get('entity_id')

  const [rec, setRec] = useState(null)
  const [offer, setOffer] = useState(null)
  const [open, setOpen] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function loadFinancing() {
      try {
        setError(null)

        // Step 1: Get simulation data from backend
        const simulation = await simulate({
          entity_id: Number(entityId),
        })

        // Step 2: Get financing recommendation
        const recommendation = await recommendFinancing(
          entityId,
          simulation.financing_input
        )

        setRec(recommendation)
      } catch (err) {
        console.error(err)
        setError('Unable to load financing recommendation.')
      }
    }

    if (entityId) {
      loadFinancing()
    } else {
      setError('No entity selected.')
    }
  }, [entityId])

  if (error) {
    return <div className="text-red-600">{error}</div>
  }

  if (!rec) {
    return <div>Loading financing...</div>
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-semibold mb-2">
        Financing Recommendation
      </h2>

      <p className="text-sm text-slate-500 mb-4">
        Review recommended financing and request a simulated bank offer.
      </p>

      <FinancingCard
        rec={rec}
        onGetOffer={() => {
          setOffer(rec.bank_offer)
          setOpen(true)
        }}
      />

      <BankOfferModal
        open={open}
        onClose={() => setOpen(false)}
        offer={offer}
        onDisburse={() => {
          setOffer((o) => ({
            ...o,
            status: 'DISBURSED',
          }))
        }}
      />
    </div>
  )
}