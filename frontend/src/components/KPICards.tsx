import { TrendingUp, TrendingDown, Minus } from 'lucide-react'
import type { MetricData } from '../types'

interface Props {
  kpis: MetricData[]
  colors: string[]
}

export default function KPICards({ kpis, colors }: Props) {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {kpis.map((kpi, i) => (
        <div
          key={i}
          className="bg-white rounded-xl shadow p-5 border-l-4"
          style={{ borderLeftColor: colors[i % colors.length] }}
        >
          <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">
            {kpi.label}
          </p>
          <p className="text-2xl font-bold text-gray-800 mt-1">
            {typeof kpi.value === 'number' ? kpi.value.toLocaleString('pt-BR') : kpi.value}
            {kpi.unit && <span className="text-sm font-normal text-gray-500 ml-1">{kpi.unit}</span>}
          </p>
          {kpi.trend && (
            <div className="flex items-center gap-1 mt-2">
              {kpi.trend === 'up' && <TrendingUp className="w-4 h-4 text-green-500" />}
              {kpi.trend === 'down' && <TrendingDown className="w-4 h-4 text-red-500" />}
              {kpi.trend === 'stable' && <Minus className="w-4 h-4 text-gray-400" />}
              {kpi.percent_change !== undefined && (
                <span
                  className={`text-xs font-medium ${
                    kpi.trend === 'up' ? 'text-green-600' : kpi.trend === 'down' ? 'text-red-600' : 'text-gray-500'
                  }`}
                >
                  {kpi.percent_change > 0 ? '+' : ''}{kpi.percent_change}%
                </span>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
