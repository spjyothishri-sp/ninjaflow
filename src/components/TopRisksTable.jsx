import React from 'react'
import { Link } from 'react-router-dom'
import RiskBadge from './RiskBadge'
import { formatINR } from '../api'

export default function TopRisksTable({ entities = [] }) {
  return (
    <div className="card overflow-x-auto">
      <h3 className="text-sm text-slate-500 mb-2">Top Risky Entities</h3>
      <table className="w-full text-left table-auto">
        <thead>
          <tr className="text-xs text-slate-500">
            <th className="p-2">Entity</th>
            <th className="p-2">Type</th>
            <th className="p-2">Risk Score</th>
            <th className="p-2">Risk Level</th>
            <th className="p-2">Action</th>
          </tr>
        </thead>
        <tbody>
          {entities.map((e) => (
            <tr key={e.id} className="border-t">
              <td className="p-2">
                <Link to={`/entity/${e.id}`} className="font-medium text-sky-600 hover:underline">
                  {e.name}
                </Link>
                <div className="text-xs text-slate-500">{e.region}</div>
              </td>
              <td className="p-2">{e.type}</td>
              <td className="p-2">{e.riskScore}</td>
              <td className="p-2">
                <RiskBadge level={e.riskLevel} />
              </td>
              <td className="p-2"> 
                <Link to={`/entity/${e.id}`} className="text-sm text-white bg-sky-600 px-3 py-1 rounded hover:bg-sky-700">View</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
