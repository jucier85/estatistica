import { useState } from 'react'
import type { AnalysisResponse } from './types'
import FileUpload from './components/FileUpload'
import Dashboard from './components/Dashboard'
import Header from './components/Header'

export default function App() {
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null)
  const [colorScheme, setColorScheme] = useState<'default' | 'dark' | 'institutional'>('default')

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-7xl mx-auto px-4 py-8">
        {!analysis ? (
          <FileUpload onAnalysisComplete={setAnalysis} />
        ) : (
          <div>
            <div className="flex items-center justify-between mb-6">
              <button
                onClick={() => setAnalysis(null)}
                className="text-sm text-blue-600 hover:text-blue-800 font-medium"
              >
                &larr; Nova Análise
              </button>
              <div className="flex gap-2">
                {(['default', 'dark', 'institutional'] as const).map((scheme) => (
                  <button
                    key={scheme}
                    onClick={() => setColorScheme(scheme)}
                    className={`px-3 py-1 text-xs rounded-full border transition-colors ${
                      colorScheme === scheme
                        ? 'bg-blue-600 text-white border-blue-600'
                        : 'bg-white text-gray-600 border-gray-300 hover:border-blue-400'
                    }`}
                  >
                    {scheme === 'default' ? 'Padrão' : scheme === 'dark' ? 'Escuro' : 'Institucional'}
                  </button>
                ))}
              </div>
            </div>
            <Dashboard analysis={analysis} colorScheme={colorScheme} />
          </div>
        )}
      </main>
    </div>
  )
}
