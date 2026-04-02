# Estatística Policial - Dashboard de Produtividade com IA

Sistema web para análise de produtividade policial utilizando IA (Google Gemini) para processar dados brutos e gerar dashboards executivos de alto impacto visual.

---

## Arquitetura do Sistema

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Frontend      │     │   Backend API    │     │   Google        │
│   React + TS    │────▶│   FastAPI        │────▶│   Gemini API    │
│   Recharts      │◀────│   Python         │◀────│   (LLM)         │
│   TailwindCSS   │     │   Pandas         │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                              │
                        ┌─────┴─────┐
                        │  Parser   │
                        │ PDF / XLS │
                        └───────────┘
```

## Stack Tecnológica

### Backend
| Tecnologia | Função |
|---|---|
| **FastAPI** | Framework API REST async de alta performance |
| **pdfplumber** | Extração de tabelas e texto de PDFs |
| **openpyxl + pandas** | Parsing de planilhas XLS/XLSX |
| **google-generativeai** | SDK do Google Gemini para análise com LLM |
| **Pydantic** | Validação e serialização de dados |

### Frontend
| Tecnologia | Função |
|---|---|
| **React 18** | UI reativa com componentes |
| **TypeScript** | Tipagem estática |
| **Recharts** | Gráficos dinâmicos (bar, line, pie, area, radar) |
| **TailwindCSS** | Estilização utility-first |
| **Lucide React** | Ícones |
| **Axios** | HTTP client |
| **Vite** | Build tool |

## Fluxo de Engenharia de Dados

```
1. UPLOAD          2. EXTRAÇÃO           3. PROCESSAMENTO IA      4. VISUALIZAÇÃO
┌──────────┐     ┌──────────────┐      ┌──────────────────┐    ┌────────────────┐
│ PDF/XLS  │────▶│ pdfplumber   │─────▶│ Google Gemini    │───▶│ KPI Cards      │
│ Upload   │     │ pandas       │      │ Prompt           │    │ Charts         │
│ (drag &  │     │              │      │ Engineering      │    │ Rankings       │
│  drop)   │     │ Extrai:      │      │                  │    │ Insights       │
│          │     │ - Tabelas    │      │ Retorna:         │    │ Recomendações  │
│          │     │ - Texto      │      │ - KPIs           │    │                │
│          │     │ - Metadados  │      │ - Gráficos       │    │ Temas:         │
│          │     │              │      │ - Insights       │    │ - Padrão       │
│          │     │              │      │ - Rankings       │    │ - Escuro       │
│          │     │              │      │ - Recomendações  │    │ - Institucional│
└──────────┘     └──────────────┘      └──────────────────┘    └────────────────┘
```

### Etapa 1: Upload e Validação
- Validação de formato (PDF, XLS, XLSX) e tamanho (máx. 50MB)
- Campos opcionais: unidade policial e período de análise

### Etapa 2: Extração de Dados
- **PDF**: `pdfplumber` extrai tabelas estruturadas e texto livre
- **XLS/XLSX**: `pandas` lê todas as sheets, normaliza headers, remove linhas vazias

### Etapa 3: Processamento com LLM (Gemini)
- Dados brutos são convertidos em contexto textual (máx. 8000 chars)
- Prompt engineering direciona o Gemini para gerar JSON estruturado com:
  - KPIs quantificados com tendência (up/down/stable)
  - Datasets formatados para 5 tipos de gráfico
  - Rankings de desempenho
  - Insights analíticos e recomendações estratégicas

### Etapa 4: Visualização
- Dashboard responsivo com cards de KPI, gráficos Recharts e tabelas
- 3 esquemas de cores para diferentes contextos de apresentação
- Layout grid adaptativo (mobile-first)

## Segurança de Dados Sensíveis

- Arquivos processados em memória com `tempfile` e removidos imediatamente após parsing
- Nenhum dado é persistido em disco ou banco de dados
- API key do Gemini isolada em variáveis de ambiente (`.env`)
- CORS configurável via `ALLOWED_ORIGINS`
- Limite de tamanho de upload configurável
- `.gitignore` exclui `.env`, uploads e caches

## Instalação

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Configure sua GEMINI_API_KEY
uvicorn main:main --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Acesse `http://localhost:5173`

## Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/api/upload` | Upload + análise com IA |
| `POST` | `/api/customize-report` | Personalização do dashboard |

## Personalização de Relatórios

O endpoint `/api/customize-report` aceita:
- `report_title`: Título personalizado
- `chart_types`: Filtro de tipos de gráfico (`bar`, `line`, `pie`, `area`, `radar`)
- `selected_metrics`: Filtro de KPIs por label
- `color_scheme`: Tema visual (`default`, `dark`, `institutional`)
