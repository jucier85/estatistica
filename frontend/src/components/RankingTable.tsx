import { Trophy } from 'lucide-react'
import type { RankingEntry } from '../types'

interface Props {
  rankings: RankingEntry[]
}

export default function RankingTable({ rankings }: Props) {
  const sorted = [...rankings].sort((a, b) => b.score - a.score)

  return (
    <div className="bg-white rounded-xl shadow p-6">
      <h3 className="text-sm font-semibold text-gray-700 flex items-center gap-2 mb-4">
        <Trophy className="w-4 h-4 text-yellow-500" />
        Ranking de Desempenho
      </h3>
      <div className="overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-100">
              <th className="text-left py-2 text-gray-500 font-medium">#</th>
              <th className="text-left py-2 text-gray-500 font-medium">Nome</th>
              <th className="text-left py-2 text-gray-500 font-medium">Categoria</th>
              <th className="text-right py-2 text-gray-500 font-medium">Score</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((entry, i) => (
              <tr key={i} className="border-b border-gray-50 hover:bg-gray-50">
                <td className="py-2.5 font-semibold text-gray-400">{i + 1}</td>
                <td className="py-2.5 font-medium text-gray-700">{entry.name}</td>
                <td className="py-2.5 text-gray-500">{entry.category}</td>
                <td className="py-2.5 text-right">
                  <span className={`font-semibold ${
                    i === 0 ? 'text-yellow-600' : i === 1 ? 'text-gray-500' : i === 2 ? 'text-orange-600' : 'text-gray-700'
                  }`}>
                    {entry.score.toLocaleString('pt-BR', { maximumFractionDigits: 1 })}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
