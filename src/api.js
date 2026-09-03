import { entities, forecast30, dashboardSummary, financingRecommendation } from './mockData'

const wait = (ms) => new Promise((res) => setTimeout(res, ms))

export function formatINR(amount) {
  if (amount == null) return '-'
  return amount.toLocaleString('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 })
}

export async function getDashboard() {
  await wait(300)
  return { summary: dashboardSummary, forecast: forecast30 }
}

export async function getEntities() {
  await wait(200)
  return entities
}

export async function getEntity(id) {
  await wait(200)
  return entities.find((e) => String(e.id) === String(id)) || null
}

export async function getRisk(id) {
  await wait(200)
  const entity = entities.find((e) => String(e.id) === String(id))
  if (!entity) return null
  return {
    score: entity.riskScore,
    level: entity.riskLevel,
    reasons: [
      `Historical average payment delay: ${Math.round(entity.predictedDelay + 1)} days`,
      `Predicted payment delay: ${entity.predictedDelay} days`,
      `Outstanding receivables: ${formatINR(entity.receivables)}`,
      `Upcoming payables: ${formatINR(entity.payables)}`,
    ],
  }
}

export async function getForecast(id) {
  await wait(200)
  // return a mock per-entity forecast by adjusting the global forecast
  const factor = 1 + ((id % 3) - 1) * 0.12
  return forecast30.map((f) => ({ ...f, cash: Math.round(f.cash * factor) }))
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export async function recommendFinancing(id, financingInput) {
  const response = await fetch(`${API_BASE_URL}/financing/recommend`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      entity_id: Number(id),
      financing_input: financingInput,
    }),
  })

  if (!response.ok) {
    throw new Error(`Financing API error: ${response.status}`)
  }

  return await response.json()
}

export async function checkBankEligibility(data) {
  await wait(300)
  // very simple eligibility mock
  return {
    eligible: true,
    approvedAmount: data.requestedAmount || financingRecommendation.recommendedAmount,
    interestRate: 12.5,
    durationDays: data.duration || financingRecommendation.durationDays,
    status: 'OFFERED',
  }
}

export async function simulate(data) {
  const response = await fetch(`${API_BASE_URL}/simulate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      entity_id: Number(data.entity_id),
    }),
  })

  if (!response.ok) {
    throw new Error(`Simulation API error: ${response.status}`)
  }

  return await response.json()
}
