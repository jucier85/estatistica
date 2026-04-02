export interface MetricData {
  label: string
  value: number
  unit: string
  trend?: 'up' | 'down' | 'stable'
  percent_change?: number
}

export interface ChartDataset {
  name: string
  data: number[]
  color: string
}

export interface ChartData {
  chart_type: 'bar' | 'line' | 'pie' | 'area' | 'radar'
  title: string
  labels: string[]
  datasets: ChartDataset[]
}

export interface RankingEntry {
  name: string
  score: number
  category: string
}

export interface AnalysisResult {
  summary: string
  kpis: MetricData[]
  charts: ChartData[]
  rankings: RankingEntry[]
  insights: string[]
  recommendations: string[]
}

export interface AnalysisResponse {
  id: string
  filename: string
  unit_name?: string
  period?: string
  raw_data: Record<string, unknown>
  analysis: AnalysisResult
}

export interface ReportConfig {
  analysis: AnalysisResult
  report_title: string
  chart_types: string[]
  selected_metrics: string[]
  color_scheme: 'default' | 'dark' | 'institutional'
}
