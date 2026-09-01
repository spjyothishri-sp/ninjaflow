import React, { useEffect, useState } from 'react'
import { getDashboard, getEntities } from '../api'
import SummaryCards from '../components/SummaryCards'
import RiskDistribution from '../components/RiskDistribution'
import CashFlowChart from '../components/CashFlowChart'
import TopRisksTable from '../components/TopRisksTable'
import FinancingCard from '../components/FinancingCard'
import { Link, useNavigate } from 'react-router-dom'

export default function Dashboard() {
  const [summary, setSummary] = useState(null)
  const [forecast, setForecast] = useState([])
  const [entities, setEntities] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    let mounted = true
    getDashboard().then((d) => {
      if (!mounted) return
      setSummary(d.summary)
      setForecast(d.forecast)
    })
    getEntities().then((e) => mounted && setEntities(e))
    return () => (mounted = false)
  }, [])

  if (!summary) return <div className="p-4">Loading dashboard...</div>

  const topRisks = [...entities].sort((a, b) => b.riskScore - a.riskScore).slice(0, 6)

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-semibold">NinjaFlow</h2>
            <p className="text-sm text-slate-500">Liquidity Control Tower</p>
          </div>
          <div>
            <Link to="/simulate" className="px-3 py-2 bg-slate-100 rounded">Open Simulator</Link>
          </div>
        </div>
      </div>

      <SummaryCards summary={summary} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mt-4">
        <div className="lg:col-span-1">
          <RiskDistribution data={{ healthy: 4, atRisk: 3, critical: 3 }} />
        </div>
        <div className="lg:col-span-2">
          <CashFlowChart data={forecast} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mt-4">
        <TopRisksTable entities={topRisks} />
        <FinancingCard rec={{ recommendedAmount: 750000, durationDays: 15, priority: 'HIGH', reason: 'Projected ₹8,00,000 shortfall in 11 days due to predicted payment delays and upcoming supplier obligations.' }} onGetOffer={() => navigate('/financing')} />
      </div>
    </div>
  )
}
