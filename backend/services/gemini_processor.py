"""
Serviço de integração com Google Gemini API.
Processa dados brutos policiais e gera análises estruturadas.
"""

import json
import os

import google.generativeai as genai
from models.schemas import AnalysisResult, ChartData, MetricData, RankingEntry, DashboardData


class GeminiProcessor:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY não configurada.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    async def analyze_police_data(
        self,
        raw_data: dict,
        unit_name: str | None = None,
        period: str | None = None,
    ) -> AnalysisResult:
        """Envia dados brutos ao Gemini e retorna análise estruturada."""

        context = self._build_context(raw_data, unit_name, period)

        prompt = f"""Você é um analista de dados especializado em segurança pública e produtividade policial.
Analise os dados a seguir e retorne um JSON com a seguinte estrutura EXATA:

{{
  "summary": "Resumo executivo da análise (2-3 parágrafos)",
  "kpis": [
    {{"label": "Nome do KPI", "value": 123.4, "unit": "unidade", "trend": "up|down|stable", "percent_change": 5.2}}
  ],
  "charts": [
    {{
      "chart_type": "bar|line|pie|area|radar",
      "title": "Título do gráfico",
      "labels": ["Label1", "Label2"],
      "datasets": [{{"name": "Série", "data": [10, 20], "color": "#3B82F6"}}]
    }}
  ],
  "rankings": [
    {{"name": "Nome", "score": 95.5, "category": "Categoria"}}
  ],
  "insights": ["Insight 1", "Insight 2"],
  "recommendations": ["Recomendação 1", "Recomendação 2"]
}}

Gere pelo menos:
- 4 KPIs relevantes (prisões, apreensões, operações, ocorrências, etc.)
- 3 gráficos distintos (barras, linhas e pizza)
- 3 insights baseados nos dados
- 2 recomendações estratégicas

DADOS PARA ANÁLISE:
{context}

Responda APENAS com o JSON válido, sem markdown ou texto adicional."""

        response = self.model.generate_content(prompt)
        return self._parse_analysis_response(response.text)

    async def generate_custom_dashboard(
        self,
        analysis: AnalysisResult,
        chart_types: list[str],
        metrics: list[str],
        title: str,
        color_scheme: str,
    ) -> DashboardData:
        """Gera dashboard personalizado com base nas preferências."""

        color_palettes = {
            "default": ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"],
            "dark": ["#60A5FA", "#34D399", "#FBBF24", "#F87171", "#A78BFA"],
            "institutional": ["#1E3A5F", "#2D5F2D", "#8B7D3C", "#6B1A1A", "#4A3B6B"],
        }
        colors = color_palettes.get(color_scheme, color_palettes["default"])

        filtered_kpis = analysis.kpis
        if metrics:
            filtered_kpis = [k for k in analysis.kpis if k.label in metrics]

        filtered_charts = [c for c in analysis.charts if c.chart_type in chart_types]
        for i, chart in enumerate(filtered_charts):
            for ds in chart.datasets:
                ds["color"] = colors[i % len(colors)]

        return DashboardData(
            title=title,
            charts=filtered_charts,
            kpis=filtered_kpis if filtered_kpis else analysis.kpis,
            summary=analysis.summary,
        )

    def _build_context(self, raw_data: dict, unit_name: str | None, period: str | None) -> str:
        """Monta contexto textual para o prompt do Gemini."""
        parts = []

        if unit_name:
            parts.append(f"Unidade Policial: {unit_name}")
        if period:
            parts.append(f"Período: {period}")

        if raw_data.get("source") == "pdf":
            if raw_data.get("text"):
                parts.append(f"Texto extraído:\n{raw_data['text'][:8000]}")
            for table in raw_data.get("tables", []):
                parts.append(f"Tabela (página {table['page']}):")
                parts.append(json.dumps(table["rows"][:100], ensure_ascii=False))
        elif raw_data.get("source") == "excel":
            for sheet_name, sheet_data in raw_data.get("sheets", {}).items():
                parts.append(f"Planilha '{sheet_name}' ({sheet_data['row_count']} linhas):")
                parts.append(f"Colunas: {', '.join(sheet_data['headers'])}")
                parts.append(json.dumps(sheet_data["rows"][:100], ensure_ascii=False))

        return "\n\n".join(parts)

    def _parse_analysis_response(self, text: str) -> AnalysisResult:
        """Faz parse seguro da resposta JSON do Gemini."""
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

        data = json.loads(cleaned)

        return AnalysisResult(
            summary=data.get("summary", ""),
            kpis=[MetricData(**k) for k in data.get("kpis", [])],
            charts=[ChartData(**c) for c in data.get("charts", [])],
            rankings=[RankingEntry(**r) for r in data.get("rankings", [])],
            insights=data.get("insights", []),
            recommendations=data.get("recommendations", []),
        )
