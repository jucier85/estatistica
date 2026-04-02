import { Lightbulb, Target } from 'lucide-react'

interface Props {
  insights: string[]
  recommendations: string[]
}

export default function InsightsPanel({ insights, recommendations }: Props) {
  return (
    <div className="bg-white rounded-xl shadow p-6 space-y-6">
      <div>
        <h3 className="text-sm font-semibold text-gray-700 flex items-center gap-2 mb-3">
          <Lightbulb className="w-4 h-4 text-yellow-500" />
          Insights
        </h3>
        <ul className="space-y-2">
          {insights.map((insight, i) => (
            <li key={i} className="text-sm text-gray-600 flex gap-2">
              <span className="text-blue-500 font-bold mt-0.5">•</span>
              {insight}
            </li>
          ))}
        </ul>
      </div>

      <div>
        <h3 className="text-sm font-semibold text-gray-700 flex items-center gap-2 mb-3">
          <Target className="w-4 h-4 text-green-500" />
          Recomendações
        </h3>
        <ul className="space-y-2">
          {recommendations.map((rec, i) => (
            <li key={i} className="text-sm text-gray-600 flex gap-2">
              <span className="text-green-500 font-bold mt-0.5">•</span>
              {rec}
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
