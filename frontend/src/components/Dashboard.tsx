import type { AnalysisResponse } from '../types'
import KPICards from './KPICards'
import ChartPanel from './ChartPanel'
import InsightsPanel from './InsightsPanel'
import RankingTable from './RankingTable'

interface Props {
  analysis: AnalysisResponse
  colorScheme: 'default' | 'dark' | 'institutional'
}

const COLOR_PALETTES = {
  default: ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899'],
  dark: ['#60A5FA', '#34D399', '#FBBF24', '#F87171', '#A78BFA', '#F472B6'],
  institutional: ['#1E3A5F', '#2D5F2D', '#8B7D3C', '#6B1A1A', '#4A3B6B', '#5F4B2D'],
}

export default function Dashboard({ analysis, colorScheme }: Props) {
  const { analysis: data } = analysis
  const colors = COLOR_PALETTES[colorScheme]

  return (
    <div className="space-y-6">
      {/* Header info */}
      <div className="bg-white rounded-xl shadow p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-gray-800">
              {analysis.unit_name || 'Análise Geral'}
            </h2>
            <p className="text-sm text-gray-500">
              {analysis.period || 'Período não especificado'} &middot; {analysis.filename}
            </p>
          </div>
          <span className="px-3 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded-full">
            Processado com IA
          </span>
        </div>
        <p className="mt-4 text-gray-600 text-sm leading-relaxed">{data.summary}</p>
      </div>

      {/* KPIs */}
      <KPICards kpis={data.kpis} colors={colors} />

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {data.charts.map((chart, i) => (
          <ChartPanel key={i} chart={chart} colors={colors} />
        ))}
      </div>

      {/* Bottom row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <InsightsPanel
          insights={data.insights}
          recommendations={data.recommendations}
        />
        {data.rankings.length > 0 && <RankingTable rankings={data.rankings} />}
      </div>
    </div>
  )
}
