"""
Estatística Policial - Backend API
Processamento de dados de produtividade policial com IA (Gemini).
"""

import os
import uuid
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from services.file_parser import parse_uploaded_file
from services.gemini_processor import GeminiProcessor
from models.schemas import (
    AnalysisResponse,
    ReportConfig,
    DashboardData,
)

load_dotenv()

app = FastAPI(
    title="Estatística Policial API",
    description="API para análise de produtividade policial com IA",
    version="1.0.0",
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50")) * 1024 * 1024

gemini = GeminiProcessor()


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/api/upload", response_model=AnalysisResponse)
async def upload_and_analyze(
    file: UploadFile = File(...),
    unit_name: Optional[str] = Form(None),
    period: Optional[str] = Form(None),
):
    """Upload de arquivo PDF ou XLS e análise via Gemini."""

    if not file.filename:
        raise HTTPException(status_code=400, detail="Nome do arquivo ausente.")

    ext = Path(file.filename).suffix.lower()
    if ext not in (".pdf", ".xls", ".xlsx"):
        raise HTTPException(
            status_code=400,
            detail="Formato não suportado. Envie PDF ou XLS/XLSX.",
        )

    contents = await file.read()
    if len(contents) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"Arquivo excede o limite de {MAX_UPLOAD_SIZE // (1024*1024)}MB.",
        )

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        raw_data = parse_uploaded_file(tmp_path, ext)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Erro ao processar arquivo: {e}")
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

    analysis = await gemini.analyze_police_data(
        raw_data=raw_data,
        unit_name=unit_name,
        period=period,
    )

    return AnalysisResponse(
        id=str(uuid.uuid4()),
        filename=file.filename,
        unit_name=unit_name,
        period=period,
        raw_data=raw_data,
        analysis=analysis,
    )


@app.post("/api/customize-report", response_model=DashboardData)
async def customize_report(config: ReportConfig):
    """Gera dashboard personalizado com base nas preferências do usuário."""

    dashboard = await gemini.generate_custom_dashboard(
        analysis=config.analysis,
        chart_types=config.chart_types,
        metrics=config.selected_metrics,
        title=config.report_title,
        color_scheme=config.color_scheme,
    )

    return dashboard
