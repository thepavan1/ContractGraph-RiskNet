<div align="center">
  <img src="https://img.shields.io/badge/Status-Production_Ready-brightgreen?style=for-the-badge" alt="Status" />
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/TypeScript-Ready-blue?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/React-Vite-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB" />
</div>

<br />

<div align="center">
  <h1 align="center">ContractGraph-RiskNet</h1>
  <p align="center">
    <strong>A Neuro-Symbolic AI Platform for Engineering Contract Risk & Delay Prediction</strong>
    <br />
    <br />
    <a href="#overview">Overview</a>
    ·
    <a href="#key-features">Features</a>
    ·
    <a href="#system-architecture">Architecture</a>
    ·
    <a href="#getting-started">Installation</a>
    ·
    <a href="#research--novelty">Research Novelty</a>
  </p>
</div>

<hr />

## 📖 Overview

**ContractGraph-RiskNet** is a research-grade, production-ready AI platform designed to transform unstructured infrastructure contracts and Monthly Progress Reports (DPRs) into deterministic, actionable risk intelligence. 

Unlike standard LLM wrappers that hallucinate schedule projections, RiskNet fuses **Symbolic Engineering Logic** (Earned Value Management, Critical Path tracking) with **Neural Architectures** (SHAP-explained Machine Learning, Context-Injected RAG) to predict delays, automatically trigger Liquidated Damages (LD) clauses, and simulate engineering-grade recovery scenarios.

This platform bridges the gap between legal contractual obligations and on-the-ground engineering reality.

---

## ✨ Key Features

### 🧠 1. Neuro-Symbolic Deviation Engine
*   **Activity-Level Variance:** Extracts project milestones directly from PDF contracts and compares them against uploaded monthly DPR PDFs.
*   **Deterministic LD Activation:** If delays exceed contract-specified thresholds, the engine dynamically calculates the exact Liquidated Damages (LD) financial exposure (e.g., *₹150 Cr Penalty*).
*   **Metrics Calculation:** Automatically tracks Schedule Variance, Schedule Performance Index (SPI), Cost Performance Index (CPI), and Financial Progress.

### 🏭 2. Live Project Digital Twin (Control Room)
*   Provides a real-time, pulsing dashboard that tracks the project's **Current Reality** against its **Original Baseline** and **AI Prediction**.
*   Maps the **Risk Propagation Chain**, visualizing exactly how a localized schedule deviation ripples into a critical legal/financial termination warning.
*   Presents **SHAP Feature Importance** to explain exactly *why* the AI assigned a specific risk profile.

### ⏱️ 3. Engineering-Grade Recovery Simulator
*   A strict, mathematically bounded "What-If" simulator that refuses to output impossible recovery times.
*   Uses realistic construction productivity constraints (e.g., 1 worker = 0.08 days recovered; 1 excavator = 0.35 days recovered) subject to diminishing returns (shift limits).
*   Visualizes real-time risk category transitions (e.g., `CRITICAL_RISK` → `HIGH_RISK`) based on simulated resource deployment.

### 🤖 4. Context-Injected AI Expert (RAG)
*   Powered by `Llama-3` (via Groq), this AI assistant is immune to hallucination.
*   **Zero-Prompting Context:** The system forcibly injects the *entire* parsed project state (current delay, LD exposure, delayed activities) into the system prompt *before* your query reaches the LLM.
*   The AI Expert acts as a highly specialized claims consultant, citing specific contract clauses and precise schedule variances in its answers.

---

## 🏗️ System Architecture

The architecture separates the heavy ML processing from the lightweight reactive frontend.

*   **Frontend**: React + TypeScript + Vite. Styled with TailwindCSS. Centralized state managed via a unified `ProjectContext`.
*   **Backend**: Python + FastAPI. Uses `pdfplumber` for zero-shot text extraction and `scikit-learn` for predictive modeling.
*   **Database**: MongoDB Atlas. Uses robust document storage for baselines, reports, and timeline histories.
*   **Seeder Script**: Includes an automated deterministic seeder that generates 10 explicit infrastructure projects (ranging from NO RISK to CRITICAL RISK) with perfectly escalating 5-month timelines.

---

## 🛠️ Tech Stack

| Category | Technologies |
| :--- | :--- |
| **Frontend** | React 18, TypeScript, Vite, TailwindCSS, Lucide Icons |
| **Backend** | Python 3.10+, FastAPI, Uvicorn, Pydantic |
| **Data Extraction** | `pdfplumber`, `re` (Regex) |
| **Machine Learning** | `scikit-learn` (TruncatedSVD, RandomForest, SHAP) |
| **Generative AI** | Groq API (`llama3-8b-8192`) |
| **Database** | MongoDB Atlas, `motor` (AsyncIO Driver) |
| **Report Generation** | `reportlab` (Dynamic PDF creation) |

---

## 🚀 Getting Started

Follow these instructions to get the platform running locally for development and demonstration.

### Prerequisites
*   Node.js (v18+)
*   Python (3.10+)
*   MongoDB Atlas cluster URI
*   Groq API Key

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ContractGraph-RiskNet.git
cd ContractGraph-RiskNet/Website
```

### 2. Backend Setup
Navigate to the backend directory, create a virtual environment, and install dependencies:
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

#### Environment Variables
Create a `.env` file in the `backend/` directory using the provided `.env.example`:
```env
MONGODB_URL=mongodb+srv://<USER>:<PASSWORD>@cluster0.xxx.mongodb.net/?retryWrites=true&w=majority
GROQ_API_KEY=gsk_YOUR_GROQ_API_KEY
```

### 3. Frontend Setup
Open a new terminal, navigate to the frontend directory, and install the dependencies:
```bash
cd frontend
npm install
```

---

## 🏃 Running the Application

### Start the Backend
The backend includes a self-executing seed script. On the very first startup (when your MongoDB is empty), it will automatically generate and seed 10 distinct, fully documented sample projects spanning 5 months of escalating risk history.

```bash
cd backend
# Ensure your venv is activated
python main.py
```
*The API will be available at `http://localhost:8000`*

### Start the Frontend
```bash
cd frontend
npm run dev
```
*The application will be available at `http://localhost:5173`*

---

## 🧪 Resetting the Database (Demo Prep)

If you need to wipe your database and recreate the perfect escalating presentation dataset:

1. Stop the backend server.
2. Run the reset script:
   ```bash
   cd backend
   python scripts/reset_db.py
   ```
3. Restart the backend server (`python main.py`). The seeder will recreate the 10 perfectly formatted sample projects.

---

## 🎓 Research & Novelty

ContractGraph-RiskNet was built to demonstrate a leap in **Construction Informatics**. 

Standard predictive tools rely solely on structured historical data (which is rare). Standard LLMs process unstructured data but cannot perform deterministic engineering math (they hallucinate numbers). 

This platform proves that by **routing unstructured contract text into deterministic rule-engines**, and subsequently mapping the mathematical variance back into an LLM's context window, we achieve a system that is both **lexically aware** of the contract and **mathematically rigid** regarding schedule delays.

---

<div align="center">
  <p>Engineered for Infrastructure Reliability.</p>
</div>
