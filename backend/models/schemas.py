"""Schemas Pydantic para request/response da API."""

from typing import Optional
from pydantic import BaseModel


class MetricData(BaseModel):
    label: str
    value: float
    unit: str = ""
    trend: Optional[str] = None  # "up" | "down" | "stable"
    percent_change: Optional[float] = None


class ChartData(BaseModel):
    chart_type: str  # "bar" | "line" | "pie" | "area" | "radar"
    title: str
    labels: list[str]
    datasets: list[dict]


class RankingEntry(BaseModel):
    name: str
    score: float
    category: str = ""


class AnalysisResult(BaseModel):
    summary: str
    kpis: list[MetricData]
    charts: list[ChartData]
    rankings: list[RankingEntry] = []
    insights: list[str] = []
    recommendations: list[str] = []


class AnalysisResponse(BaseModel):
    id: str
    filename: str
    unit_name: Optional[str] = None
    period: Optional[str] = None
    raw_data: dict
    analysis: AnalysisResult


class ReportConfig(BaseModel):
    analysis: AnalysisResult
    report_title: str = "Relatório de Produtividade Policial"
    chart_types: list[str] = ["bar", "line", "pie"]
    selected_metrics: list[str] = []
    color_scheme: str = "default"  # "default" | "dark" | "institutional"


class DashboardData(BaseModel):
    title: str
    charts: list[ChartData]
    kpis: list[MetricData]
    summary: str
