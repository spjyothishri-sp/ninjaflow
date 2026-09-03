import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getEntity, getRisk, getForecast, formatINR } from '../api'
import CashFlowChart from '../components/CashFlowChart'
import RiskBadge from '../components/RiskBadge'

export default function EntityPage() {
  const { id } = useParams()
  const [entity, setEntity] = useState(null)
  const [risk, setRisk] = useState(null)
  const [forecast, setForecast] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    let mounted = true

    getEntity(id).then((e) => mounted && setEntity(e))
    getRisk(id).then((r) => mounted && setRisk(r))
    getForecast(id).then((f) => mounted && setForecast(f))

    return () => (mounted = false)
  }, [id])

  if (!entity || !risk) {
    return <div>Loading...</div>
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-2xl font-semibold">{entity.name}</h2>
          <div className="text-sm text-slate-500">
            {entity.type} • {entity.region}
          </div>
        </div>

        <div className="text-right">
          <div className="text-xl font-semibold">
            Risk Score: {entity.riskScore}
          </div>

          <div className="mt-1">
            <RiskBadge level={entity.riskLevel} />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="card">
          <h3 className="text-sm text-slate-500">
            Predicted payment delay
          </h3>

          <div className="text-2xl font-semibold">
            {entity.predictedDelay} days
          </div>

          <div className="text-sm text-slate-500 mt-2">
            Delay probability:{' '}
            {(entity.delayProbability * 100).toFixed(0)}%
          </div>

          <div className="mt-3 text-sm">
            <div>
              Outstanding receivables:{' '}
              <span className="font-medium">
                {formatINR(entity.receivables)}
              </span>
            </div>

            <div>
              Upcoming payables:{' '}
              <span className="font-medium">
                {formatINR(entity.payables)}
              </span>
            </div>
          </div>

          <div className="mt-4">
            <button
              onClick={() => navigate(`/financing?entity_id=${id}`)}
              className="px-3 py-2 bg-sky-600 text-white rounded"
            >
              Get Financing
            </button>
          </div>
        </div>

        <div className="card">
          <h3 className="text-sm text-slate-500">
            Why is this risky?
          </h3>

          <ul className="mt-2 list-disc pl-5 text-sm text-slate-700">
            {risk.reasons.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="mt-4">
        <CashFlowChart data={forecast} />
      </div>

      <div className="mt-4 card">
        <h3 className="text-sm text-slate-500">
          Projected Liquidity Gap
        </h3>

        <div className="text-3xl font-semibold text-red-600">
          ₹8,00,000
        </div>

        <div className="text-sm text-slate-500">
          Expected in 11 days
        </div>
      </div>
    </div>
  )
}