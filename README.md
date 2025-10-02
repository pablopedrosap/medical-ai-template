# Medical AI Platform - Template

> **Production-ready starter template for building AI-powered medical document analysis systems**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 15](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org/)

**🚀 This is a sanitized template** based on a production medical-legal expertise platform that has processed:
- **1,000+ medical reports**
- **€4M+ in litigation value**
- **60+ medical experts** using the system
- **90% reduction** in report generation time (8-15 hours → 4-8 minutes)

All client data removed. Includes synthetic dataset for testing.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Pipeline Stages](#pipeline-stages)
- [Configuration](#configuration)
- [Evaluation & Testing](#evaluation--testing)
- [Deployment](#deployment)
- [Cost Estimation](#cost-estimation)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This template demonstrates a **multi-stage AI pipeline** for processing medical documents and generating professional reports. The system orchestrates 5 different AI models to achieve production-grade quality.

### Processing Pipeline

```
Document Upload → OCR → Classification → Medical Analysis → Literature Search → Report Synthesis
     (PDF/DOCX)   (Gemini)   (GPT-4o)        (O1/O3)        (Perplexity)      (Gemini/O3)
```

### Tech Stack at a Glance

**Frontend**: Next.js 15 + React 19 + Tailwind CSS
**Backend**: FastAPI + Python 3.10+
**AI Models**: OpenAI (GPT-4o, O1, O3) + Google Gemini (2.0 Flash, 2.5 Pro) + Perplexity Sonar
**Storage**: Google Cloud Storage + Supabase
**Deployment**: Google Cloud Run (serverless) + Vercel

---

## Features

### ✨ Multi-Model AI Orchestration
- **Gemini 2.0 Flash**: Fast OCR with 8 concurrent calls (~40 pages/min)
- **GPT-4o**: Document classification with structured outputs
- **O1/O3**: Deep medical reasoning with `reasoning_effort='high'`
- **Gemini 2.5 Pro**: Long-form report synthesis
- **Perplexity Sonar**: Evidence-based medical literature search

### 📄 Multi-Format Document Support
- **PDF**: High-DPI conversion (200 DPI for medical documents)
- **DOCX**: Native text extraction with table support
- **Images**: PNG, JPG, JPEG with OCR

### 🔄 Production-Grade Error Handling
- **Retry Logic**: 3 attempts with exponential backoff (0s, 60s, 180s)
- **Graceful Degradation**: Continues processing on partial failures
- **Rate Limit Management**: Semaphore-based concurrency control

### 📊 Synthetic Data Generator
- Generate realistic medical records for testing
- No PHI/PII - 100% synthetic
- Configurable complexity levels (simple, medium, complex)
- Supports multiple report types (VDC, Praxis, Incapacidad)

### 🧪 Comprehensive Test Suite
- End-to-end pipeline tests with synthetic data
- Performance benchmarking
- Accuracy evaluation metrics
- Pytest-based test framework

---

## Architecture

### High-Level System Design

```
┌─────────────────────────────────────────────────────────────┐
│  CLIENT (Next.js 15)                                         │
│  • Dashboard for case management                            │
│  • Multi-file upload (drag-drop)                            │
│  • Real-time processing status                              │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTPS/REST
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  API (FastAPI on Cloud Run)                                 │
│  • POST /generate_upload_url → GCS signed URLs             │
│  • POST /process → Pipeline orchestration                   │
│  • GET /status/{job_id} → Real-time progress               │
└────────────────┬────────────────────────────────────────────┘
                 │
      ┌──────────┼──────────┬──────────┬──────────┐
      │          │           │          │          │
      ▼          ▼           ▼          ▼          ▼
   ┌────┐    ┌────────┐  ┌──────┐  ┌──────┐  ┌──────┐
   │GCS │    │Supabase│  │OpenAI│  │Gemini│  │Perplex│
   │    │    │   DB   │  │ API  │  │ API  │  │  API │
   └────┘    └────────┘  └──────┘  └──────┘  └──────┘
```

See [diagrams/architecture.mermaid](../portfolio-case-study/diagrams/architecture.mermaid) for detailed architecture.

---

## Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **Docker** (optional, for deployment)
- **API Keys**:
  - [OpenAI API key](https://platform.openai.com/api-keys)
  - [Google Gemini API key](https://aistudio.google.com/app/apikey)
  - [Perplexity API key](https://www.perplexity.ai/settings/api)
  - [Supabase project](https://supabase.com) (free tier available)

### 1. Clone Repository

```bash
git clone https://github.com/pablopedrosa/medical-ai-template.git
cd medical-ai-template
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys
```

**.env.example**:
```env
# AI APIs
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
PERPLEXITY_API_KEY=your_perplexity_key_here

# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Google Cloud (for deployment)
PROJECT_ID=your_gcp_project_id
REGION=us-central1

# Optional
AWS_ACCESS_KEY_ID=your_aws_key  # for Textract fallback
AWS_SECRET_ACCESS_KEY=your_aws_secret
```

### 3. Generate Synthetic Data

```bash
cd data/synthetic
python generate_synthetic_data.py --count 10 --output test_dataset.json

# Options:
# --count: Number of cases to generate (default: 10)
# --report_types: praxis,vdc,incapacidad (comma-separated)
# --complexity: simple, medium, complex
# --output: Output filename
```

### 4. Run Backend

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8080

# API will be available at http://localhost:8080
# Docs at http://localhost:8080/docs
```

### 5. Frontend Setup (Optional)

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local with your Supabase keys

# Run development server
npm run dev

# Frontend at http://localhost:3000
```

### 6. Run Tests

```bash
cd backend
pytest tests/ -v

# Run specific test
pytest tests/test_e2e_synthetic.py -v

# Run with coverage
pytest tests/ --cov=pipelines
```

---

## Pipeline Stages

### Stage 1: OCR & Text Extraction

**Model**: Gemini 2.0 Flash
**Concurrency**: 8 parallel calls
**Throughput**: ~40 pages/minute
**Cost**: ~$0.05 per 100 pages

```python
from pipelines.ocr_pipeline import extract_text_from_documents

files = [Path("medical_record.pdf"), Path("claim.docx")]
results = await extract_text_from_documents(files)
```

**Features**:
- High-DPI conversion (200 DPI for medical documents)
- Retry logic (3 attempts with exponential backoff)
- Text cleaning (remove OCR artifacts)
- Supports PDF, DOCX, PNG, JPG

See [backend/pipelines/ocr_pipeline.py](backend/pipelines/ocr_pipeline.py)

### Stage 2: Document Classification

**Model**: GPT-4o
**Output**: Structured (Pydantic BaseModel)
**Accuracy**: >98% on validation set

```python
from pipelines.classification_pipeline import classify_document

result = classify_document(extracted_text)
print(result.is_claim)  # True/False/None
print(result.confidence)  # 0.0-1.0
```

**Classifies into**:
- **Medical Documentation**: Objective clinical observations
- **Legal Claim**: Allegations, blame attribution
- **Ambiguous**: Mixed content (written to both categories)

See [backend/pipelines/classification_pipeline.py](backend/pipelines/classification_pipeline.py)

### Stage 3: Medical Data Extraction

**Models**: O1/O3 (complex docs) or Gemini 2.5 Pro (normal docs)
**Structured Output**: Demographics, history, timeline, diagnoses

```python
from pipelines.extraction_pipeline import extract_medical_details

medical_data = await extract_medical_details(
    text=medical_text,
    use_reasoning=True  # Use O3 for complex cases
)
```

**Extracts**:
- Patient demographics (age, sex, occupation)
- Medical history (chronic conditions)
- Surgical history
- Episode timeline (dates, events, diagnoses, treatments)
- Current status

See [backend/pipelines/extraction_pipeline.py](backend/pipelines/extraction_pipeline.py)

### Stage 4: Literature Search

**Model**: Perplexity Sonar Reasoning Pro
**Rate Limit**: 2 RPM (requests per minute)
**Output**: 10-20 Q&A pairs with PubMed citations

```python
from pipelines.literature_search import search_medical_literature

questions = [
    "What is the standard of care for acute coronary syndrome in 2024?",
    "What are typical complications of PCI with stent placement?"
]

faq = await search_medical_literature(questions)
```

**Process**:
1. Generate 10-20 clinical questions (O3 reasoning)
2. Batch search with rate limiting
3. Format bibliography (APA style)

See [backend/pipelines/literature_search.py](backend/pipelines/literature_search.py)

### Stage 5: Report Synthesis

**Models**: Gemini 2.5 Pro (VDC, Incapacidad) or O3 (Praxis)
**Output**: 20-40 page professional reports in DOCX format

```python
from pipelines.synthesis_pipeline import generate_report

report = await generate_report(
    medical_data=medical_data,
    claim_data=claim_summary,
    literature=faq,
    report_type="praxis"
)
```

**Report Types**:
- **VDC**: Body damage assessment with legal tables
- **Praxis**: Malpractice analysis (defense or accusation)
- **Incapacidad**: Disability evaluation
- **Discapacidad**: Disability report
- **Dependencia**: Dependency assessment

**Formatting**:
```
Markdown (AI output) → HTML → DOCX → Professional styling
```

See [backend/pipelines/synthesis_pipeline.py](backend/pipelines/synthesis_pipeline.py)

---

## Configuration

All settings in YAML files (easier to manage than code):

### AI Models Configuration

**File**: `backend/config/ai_models.yaml`

```yaml
models:
  ocr:
    provider: gemini
    model: gemini-2.0-flash
    max_tokens: 8024
    concurrent_calls: 8

  classification:
    provider: openai
    model: gpt-4o
    temperature: 0.0

  reasoning:
    provider: openai
    model: o3
    reasoning_effort: high
```

### Pipeline Settings

**File**: `backend/config/pipeline_settings.yaml`

```yaml
document_processing:
  pdf:
    conversion_dpi: 200
    fallback_dpi: 100

  ocr:
    max_concurrent: 8
    timeout_per_page: 30

text_cleaning:
  max_consecutive_chars: 20
  max_line_repetitions: 20

report_generation:
  default_length_pages: 20
  include_bibliography: true
```

---

## Evaluation & Testing

### Run Synthetic Evaluation

```bash
cd backend
python scripts/run_synthetic_eval.py \
  --dataset ../data/synthetic/test_dataset.json \
  --output eval_results.json
```

**Example Output**:

```
============================================================
EVALUATION RESULTS
============================================================
Metric                  | Value
============================================================
Total Cases             | 50
Successful              | 48
Failed                  | 2
Success Rate            | 96.0%
Avg Processing Time     | 4.3s
Avg Accuracy            | 87.5%
============================================================

Results saved to eval_results.json
```

### Metrics Tracked

- **Processing Time**: End-to-end pipeline duration
- **Success Rate**: Percentage of jobs completed without errors
- **Accuracy**: Comparison vs. expected outputs (synthetic ground truth)
- **Cost per Report**: Estimated from token usage
- **Throughput**: Reports per hour

### Unit Tests

```bash
# Test individual pipelines
pytest tests/test_ocr_pipeline.py -v
pytest tests/test_classification.py -v
pytest tests/test_extraction.py -v

# Test full pipeline
pytest tests/test_e2e_synthetic.py -v
```

---

## Deployment

### Google Cloud Run (Backend)

```bash
cd backend

# Build and push container
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/medical-ai-api .

# Deploy to Cloud Run
gcloud run deploy medical-ai-api \
  --image gcr.io/YOUR-PROJECT-ID/medical-ai-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=$OPENAI_API_KEY,GEMINI_API_KEY=$GEMINI_API_KEY

# Get service URL
gcloud run services describe medical-ai-api --region us-central1 --format 'value(status.url)'
```

### Vercel (Frontend)

```bash
cd frontend

# Install Vercel CLI
npm install -g vercel

# Deploy
vercel deploy --prod

# Configure environment variables in Vercel dashboard
```

### Docker Compose (Local Development)

```bash
# Run both frontend and backend
docker-compose up

# Backend: http://localhost:8080
# Frontend: http://localhost:3000
```

---

## Cost Estimation

Based on processing **100 reports per month** with average 50-page documents:

| Component       | Model            | Cost/Report | Monthly (100) |
|-----------------|------------------|-------------|---------------|
| OCR             | Gemini Flash     | $0.05       | $5            |
| Classification  | GPT-4o           | $0.10       | $10           |
| Reasoning       | O3               | $0.50       | $50           |
| Synthesis       | Gemini 2.5 Pro   | $0.15       | $15           |
| Literature      | Perplexity Sonar | $0.20       | $20           |
| **AI Total**    |                  | **$1.00**   | **$100**      |
| Cloud Run       | GCP              | $0.10       | $10           |
| Storage         | GCS + Supabase   | $0.05       | $5            |
| **Grand Total** |                  | **$1.15**   | **$115**      |

**Compare to**:
- Manual expert fee: $500-1,500 per report
- Time savings: 8-15 hours → 4-8 minutes (90% reduction)

---

## Project Structure

```
medical-ai-template/
├── backend/
│   ├── pipelines/
│   │   ├── ocr_pipeline.py              # Stage 1: OCR
│   │   ├── classification_pipeline.py   # Stage 2: Classification
│   │   ├── extraction_pipeline.py       # Stage 3: Medical extraction
│   │   ├── literature_search.py         # Stage 4: PubMed search
│   │   └── synthesis_pipeline.py        # Stage 5: Report generation
│   ├── utils/
│   │   ├── text_cleaning.py
│   │   ├── retry_logic.py
│   ��   └── document_converter.py
│   ├── config/
│   │   ├── ai_models.yaml
│   │   └── pipeline_settings.yaml
│   ├── tests/
│   │   ├── test_ocr_pipeline.py
│   │   ├── test_classification.py
│   │   ├── test_extraction.py
│   │   └── test_e2e_synthetic.py
│   ├── main.py                          # FastAPI application
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── app/
│   │   ├── page.tsx                     # Dashboard
│   │   └── api/
│   │       └── upload.ts
│   ├── components/
│   │   ├── DocumentUpload.tsx
│   │   └── ProcessingStatus.tsx
│   ├── package.json
│   └── next.config.ts
├── data/
│   ├── synthetic/
│   │   ├── generate_synthetic_data.py
│   │   └── sample_medical_records.json
│   └── schemas/
│       ├── medical_record_schema.json
│       └── report_schema.json
├── scripts/
│   ├── run_synthetic_eval.py
│   └── deploy_cloudrun.sh
├── docs/
│   ├── ARCHITECTURE.md
│   ├── PIPELINE.md
│   └── DEPLOYMENT.md
├── docker-compose.yml
├── LICENSE (MIT)
└── README.md (this file)
```

---

## Contributing

Contributions welcome! Please follow these steps:

1. **Fork** the repository
2. **Create feature branch**: `git checkout -b feature/AmazingFeature`
3. **Run tests**: `pytest tests/ -v`
4. **Commit changes**: `git commit -m 'Add AmazingFeature'`
5. **Push to branch**: `git push origin feature/AmazingFeature`
6. **Open Pull Request**

**Guidelines**:
- Add tests for new features
- Update documentation
- Follow PEP 8 style guide (Python)
- Use ESLint/Prettier (TypeScript)

---

## License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

You are free to:
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Private use

**Attribution appreciated but not required.**

---

## Acknowledgments

- **Based on**: Production medical-legal platform (1,000+ reports, €4M+ litigation)
- **Synthetic data**: Generated with GPT-4o (no real patient data)
- **Architecture**: Inspired by LangChain RAG patterns
- **AI Models**: OpenAI, Google Gemini, Perplexity

---

## Related Resources

### Case Study

See the full **production case study** with metrics, architecture diagrams, and user testimonials:

🔗 **[Medical AI Platform Case Study](https://github.com/pablopedrosa/medical-ai-case-study)**

**Includes**:
- Problem statement & business impact
- Architecture diagrams (Mermaid)
- Production metrics (1,000+ reports, 60+ users)
- User testimonials from medical experts
- Technology deep dive

### Author

**Pablo Pedrosa**
Technical Lead & AI Engineer

- **GitHub**: [github.com/pablopedrosa](https://github.com/pablopedrosa)
- **LinkedIn**: [linkedin.com/in/pablopedrosa](https://linkedin.com/in/pablopedrosa)
- **Email**: pablo@example.com

**Looking for**: Solutions Engineering roles, Technical AI Product positions, Healthcare AI opportunities

---

## Support

- **Issues**: [GitHub Issues](https://github.com/pablopedrosa/medical-ai-template/issues)
- **Discussions**: [GitHub Discussions](https://github.com/pablopedrosa/medical-ai-template/discussions)
- **Documentation**: [docs/](docs/)

---

**Star ⭐ this repo if you find it useful!**

Built with: Next.js 15 • FastAPI • OpenAI (GPT-4o, O1, O3) • Google Gemini (2.0 Flash, 2.5 Pro) • Perplexity Sonar • Supabase • Google Cloud Platform

**Last Updated**: January 2025
