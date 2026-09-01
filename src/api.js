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

export async function recommendFinancing(id) {
  await wait(200)
  return financingRecommendation
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
  await wait(200)
  // Simple simulation: paymentDelay increases gap and risk
  const { paymentDelay = 6, orderAmount = 200000, supplierPayment = 500000, currentCash = 1500000 } = data
  const delayFactor = 1 + paymentDelay / 30
  const projectedCash = Math.max(0, Math.round(currentCash - supplierPayment - orderAmount / 2 - paymentDelay * 15000))
  const liquidityGap = Math.max(0, Math.round((supplierPayment + orderAmount) * delayFactor - currentCash))
  const riskScore = Math.min(100, Math.round(30 + paymentDelay * 2 + (liquidityGap / 100000) * 5))
  const riskLevel = riskScore > 70 ? 'CRITICAL' : riskScore > 45 ? 'AT RISK' : 'HEALTHY'
  const financingRequired = liquidityGap > 0 ? liquidityGap : 0
  return { projectedCash, liquidityGap, riskScore, riskLevel, financingRequired }
}
