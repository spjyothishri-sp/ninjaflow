import React, { useState, useEffect } from 'react'
import { formatINR } from '../api'

function Slider({ label, min, max, step = 1, value, onChange, suffix = '' }) {
  return (
    <div>
      <div className="flex justify-between text-sm mb-1">
        <div>{label}</div>
        <div className="font-medium">
          {value.toLocaleString('en-IN')}
          {suffix}
        </div>
      </div>

      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full"
      />
    </div>
  )
}

function calculateWhatIf(paymentDelay, orderAmount, supplierPayment, currentCash) {
  // Estimate how much of the order amount is available immediately.
  // Longer payment delays reduce immediately available cash.
  const collectionFactor = Math.max(0, 1 - paymentDelay / 30)

  const availableCollection = orderAmount * collectionFactor

  // Projected cash after expected collection and supplier payment.
  const projectedCash =
    currentCash + availableCollection - supplierPayment

  // Amount by which projected cash falls below zero.
  const liquidityGap = Math.max(0, -projectedCash)

  // Financing required is equal to the liquidity gap.
  const financingRequired = liquidityGap

  // Simple demo risk calculation.
  let riskLevel = 'LOW'

  if (paymentDelay >= 20 || liquidityGap > 500000) {
    riskLevel = 'CRITICAL'
  } else if (paymentDelay >= 10 || liquidityGap > 250000) {
    riskLevel = 'HIGH'
  } else if (paymentDelay >= 5 || liquidityGap > 0) {
    riskLevel = 'MEDIUM'
  }

  return {
    projectedCash: Math.round(projectedCash),
    riskLevel,
    liquidityGap: Math.round(liquidityGap),
    financingRequired: Math.round(financingRequired),
  }
}

export default function Simulator() {
  const [paymentDelay, setPaymentDelay] = useState(6)
  const [orderAmount, setOrderAmount] = useState(200000)
  const [supplierPayment, setSupplierPayment] = useState(500000)
  const [currentCash, setCurrentCash] = useState(1500000)

  const [result, setResult] = useState(null)

  useEffect(() => {
    const calculatedResult = calculateWhatIf(
      paymentDelay,
      orderAmount,
      supplierPayment,
      currentCash
    )

    setResult(calculatedResult)
  }, [paymentDelay, orderAmount, supplierPayment, currentCash])

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-2xl font-semibold mb-2">
        What-If Simulator
      </h2>

      <p className="text-sm text-slate-500 mb-4">
        Stress test liquidity by tweaking key variables.
      </p>

      <div className="grid gap-4">

        <div className="card">
          <Slider
            label="Payment Delay (days)"
            min={0}
            max={30}
            value={paymentDelay}
            onChange={setPaymentDelay}
          />
        </div>

        <div className="card">
          <Slider
            label="Order Amount"
            min={50000}
            max={1000000}
            step={5000}
            value={orderAmount}
            onChange={setOrderAmount}
          />
        </div>

        <div className="card">
          <Slider
            label="Supplier Payment"
            min={50000}
            max={1500000}
            step={5000}
            value={supplierPayment}
            onChange={setSupplierPayment}
          />
        </div>

        <div className="card">
          <Slider
            label="Current Cash"
            min={100000}
            max={3000000}
            step={10000}
            value={currentCash}
            onChange={setCurrentCash}
          />
        </div>

        <div className="card">
          <h3 className="text-sm text-slate-500">
            Impact Panel
          </h3>

          {result ? (
            <div className="mt-3 grid grid-cols-1 md:grid-cols-4 gap-3">

              <div className="p-3 bg-gray-50 rounded">
                <div className="text-sm text-slate-500">
                  Projected Cash
                </div>

                <div className="font-semibold">
                  {formatINR(result.projectedCash)}
                </div>
              </div>

              <div className="p-3 bg-gray-50 rounded">
                <div className="text-sm text-slate-500">
                  Risk Level
                </div>

                <div className="font-semibold">
                  {result.riskLevel}
                </div>
              </div>

              <div className="p-3 bg-gray-50 rounded">
                <div className="text-sm text-slate-500">
                  Liquidity Gap
                </div>

                <div className="font-semibold text-red-600">
                  {formatINR(result.liquidityGap)}
                </div>
              </div>

              <div className="p-3 bg-gray-50 rounded">
                <div className="text-sm text-slate-500">
                  Financing Required
                </div>

                <div className="font-semibold">
                  {formatINR(result.financingRequired)}
                </div>
              </div>

            </div>
          ) : (
            <div>Calculating...</div>
          )}
        </div>

      </div>
    </div>
  )
}