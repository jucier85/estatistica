import axios from 'axios'
import type { AnalysisResponse, ReportConfig } from '../types'

const api = axios.create({
  baseURL: '/api',
  timeout: 120000,
})

export async function uploadFile(
  file: File,
  unitName?: string,
  period?: string,
): Promise<AnalysisResponse> {
  const formData = new FormData()
  formData.append('file', file)
  if (unitName) formData.append('unit_name', unitName)
  if (period) formData.append('period', period)

  const { data } = await api.post<AnalysisResponse>('/upload', formData)
  return data
}

export async function customizeReport(config: ReportConfig) {
  const { data } = await api.post('/customize-report', config)
  return data
}
