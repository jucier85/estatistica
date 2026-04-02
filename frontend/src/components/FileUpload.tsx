import { useState, useCallback } from 'react'
import { Upload, FileText, Loader2 } from 'lucide-react'
import { uploadFile } from '../services/api'
import type { AnalysisResponse } from '../types'

interface Props {
  onAnalysisComplete: (data: AnalysisResponse) => void
}

export default function FileUpload({ onAnalysisComplete }: Props) {
  const [file, setFile] = useState<File | null>(null)
  const [unitName, setUnitName] = useState('')
  const [period, setPeriod] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [dragActive, setDragActive] = useState(false)

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragActive(false)
    const dropped = e.dataTransfer.files[0]
    if (dropped) {
      validateAndSetFile(dropped)
    }
  }, [])

  const validateAndSetFile = (f: File) => {
    const ext = f.name.split('.').pop()?.toLowerCase()
    if (!ext || !['pdf', 'xls', 'xlsx'].includes(ext)) {
      setError('Formato inválido. Envie PDF ou XLS/XLSX.')
      return
    }
    if (f.size > 50 * 1024 * 1024) {
      setError('Arquivo excede 50MB.')
      return
    }
    setError('')
    setFile(f)
  }

  const handleSubmit = async () => {
    if (!file) return
    setLoading(true)
    setError('')
    try {
      const result = await uploadFile(file, unitName || undefined, period || undefined)
      onAnalysisComplete(result)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao processar arquivo.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-2xl shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Análise de Produtividade</h2>
        <p className="text-gray-500 mb-6">
          Faça upload dos dados policiais para gerar dashboards inteligentes com IA.
        </p>

        <div
          onDragOver={(e) => { e.preventDefault(); setDragActive(true) }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-xl p-10 text-center transition-colors cursor-pointer ${
            dragActive
              ? 'border-blue-500 bg-blue-50'
              : file
                ? 'border-green-400 bg-green-50'
                : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
          }`}
          onClick={() => document.getElementById('file-input')?.click()}
        >
          <input
            id="file-input"
            type="file"
            accept=".pdf,.xls,.xlsx"
            className="hidden"
            onChange={(e) => e.target.files?.[0] && validateAndSetFile(e.target.files[0])}
          />
          {file ? (
            <div className="flex flex-col items-center gap-2">
              <FileText className="w-12 h-12 text-green-500" />
              <p className="font-medium text-green-700">{file.name}</p>
              <p className="text-sm text-gray-500">
                {(file.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          ) : (
            <div className="flex flex-col items-center gap-2">
              <Upload className="w-12 h-12 text-gray-400" />
              <p className="font-medium text-gray-600">
                Arraste o arquivo ou clique para selecionar
              </p>
              <p className="text-sm text-gray-400">PDF, XLS ou XLSX (máx. 50MB)</p>
            </div>
          )}
        </div>

        <div className="grid grid-cols-2 gap-4 mt-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Unidade Policial
            </label>
            <input
              type="text"
              value={unitName}
              onChange={(e) => setUnitName(e.target.value)}
              placeholder="Ex: 1º BPM"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Período
            </label>
            <input
              type="text"
              value={period}
              onChange={(e) => setPeriod(e.target.value)}
              placeholder="Ex: Jan-Mar 2026"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
          </div>
        </div>

        {error && (
          <p className="mt-4 text-sm text-red-600 bg-red-50 p-3 rounded-lg">{error}</p>
        )}

        <button
          onClick={handleSubmit}
          disabled={!file || loading}
          className="mt-6 w-full bg-blue-600 text-white py-3 rounded-xl font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Processando com IA...
            </>
          ) : (
            <>
              <Upload className="w-5 h-5" />
              Analisar Dados
            </>
          )}
        </button>
      </div>
    </div>
  )
}
