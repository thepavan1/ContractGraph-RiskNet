<div align="center">

# ContractGraph-RiskNet

### A Neuro-Symbolic AI Framework for Infrastructure Contract Risk Prediction using Knowledge Graphs and Deep Learning

<img src="https://img.shields.io/badge/Research-Neuro--Symbolic_AI-purple?style=for-the-badge"/>
<img src="https://img.shields.io/badge/PyTorch-Deep_Learning-red?style=for-the-badge&logo=pytorch"/>
<img src="https://img.shields.io/badge/Knowledge_Graph-Node2Vec-blue?style=for-the-badge"/>
<img src="https://img.shields.io/badge/FastAPI-Deployment-green?style=for-the-badge&logo=fastapi"/>
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge"/>

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Research Motivation](#-research-motivation)
- [Proposed Architecture](#️-proposed-architecture)
- [Dataset](#-dataset)
- [Model Artifacts](#-model-artifacts)
- [Experimental Results](#-experimental-results)
- [Explainable AI](#-explainable-ai)
- [Ablation Study](#-ablation-study)
- [Generated Research Figures](#-generated-research-figures)
- [Deployment Prototype](#-deployment-prototype)
- [AI Contract Assistant](#-ai-contract-assistant)
- [Technology Stack](#️-technology-stack)
- [Installation](#️-installation)
- [Repository Structure](#-repository-structure)
- [Research Contribution](#-research-contribution)
- [Future Work](#-future-work)
- [Citation](#-citation)
- [Contributing](#-contributing)
- [License](#-license)
- [Authors](#-authors)
- [Acknowledgements](#-acknowledgements)

---

## 🔎 Overview

**ContractGraph-RiskNet** is a research-oriented Neuro-Symbolic Artificial Intelligence framework designed for predicting risk in large-scale infrastructure projects by combining:

- Contractual knowledge representation
- Graph-based reasoning
- Semantic contract understanding
- Deep learning based risk inference

Traditional infrastructure risk prediction approaches mainly depend on structured project attributes and ignore valuable information hidden inside contractual documents.

ContractGraph-RiskNet bridges this gap by converting contract clauses into a **Contract Risk Knowledge Graph**, learning graph representations, extracting semantic risk features, and combining them with project parameters using a neural inference model.

The framework supports:

- EPC / HAM infrastructure contract analysis
- Early risk prediction
- Contract clause intelligence
- Explainable AI based decision support
- Project monitoring through a Digital Twin dashboard

---

## 🎯 Research Motivation

Large infrastructure projects frequently suffer from:

- Schedule delays
- Cost overruns
- Contract disputes
- Quality failures
- Termination risks

Existing ML approaches fail to capture contractual dependencies such as:

```text
Delayed Milestone
       ↓
Liquidated Damages
       ↓
Financial Stress
       ↓
Termination Risk
```

Therefore, ContractGraph-RiskNet introduces **contract-aware reasoning** into risk prediction.

---

## 🏗️ Proposed Architecture

The framework consists of **five major layers**:

### 1. Contract Intelligence Extraction Layer

**Input:**

- Government Contract Corpus
- EPC Agreements
- World Bank Standard Procurement Documents

**Processing:**

- PDF extraction
- Text preprocessing
- Risk keyword mining
- Clause identification

**Output:** Structured contract risk entities.

---

### 2. Contract Risk Knowledge Graph

Extracted contract concepts are represented as a graph.

**Entities:**

- Delay
- Cost Overrun
- Liquidated Damages
- Quality Failure
- Termination
- Financial Stress

**Relations:**

- `CAUSES`
- `INCREASES`
- `TRIGGERS`
- `DEPENDS_ON`

**Graph structure:**

```text
Risk Entity → Relation → Risk Entity
```

This enables **symbolic reasoning** over contract dependencies.

---

### 3. Graph Representation Learning

Knowledge Graph nodes are transformed into numerical embeddings using **Node2Vec**.

Random walks capture:

- Local neighbourhood information
- Risk dependency patterns
- Structural relationships

**Output:** `KG Embedding Vector = 8 dimensions`

---

### 4. Semantic Contract Encoder

Contract clauses are converted into semantic risk representations.

**Pipeline:**

```text
Contract Text
     ↓
TF-IDF Vectorization
     ↓
Truncated SVD
     ↓
Semantic Risk Vector
```

**Output:** `Semantic Features = 4 dimensions`

---

### 5. ContractGraph-RiskNet Neural Model

**Final feature fusion:**

```text
Project Features        ( 3 )
+ Knowledge Graph        ( 8 )
+ Semantic Features      ( 4 )
-----------------------------
= 15 Total Features
```

**Neural Architecture:**

```text
Input Layer (15)
      ↓
Dense Layer (32) → ReLU → BatchNorm → Dropout
      ↓
Dense Layer (16) → ReLU → BatchNorm → Dropout
      ↓
Sigmoid Classifier
      ↓
Risk Probability
```

---

## 📊 Dataset

The dataset combines structured, graph, and semantic features.

### Project Features

| Feature            | Description                       |
| ------------------ | --------------------------------- |
| Project Cost       | Infrastructure investment value   |
| Region             | Location based risk encoding      |
| Environmental Risk | External impact factor            |

### Knowledge Features

```text
KG_embedding_0
KG_embedding_1
...
KG_embedding_7
```

### Semantic Features

```text
semantic_risk_0
semantic_risk_1
semantic_risk_2
semantic_risk_3
```

**Final Dataset:** `ContractGraph_RiskNet_FinalDataset.csv`

---

## 📦 Model Artifacts

The trained system produces the following artifacts:

```text
models/
├── ContractGraph_RiskNet.pt
├── risk_scaler.pkl
├── feature_columns.pkl
├── tfidf.pkl
├── svd.pkl
├── contract_embedding.pkl
└── semantic_embedding.pkl
```

These artifacts are directly integrated into the deployment platform.

---

## 🧪 Experimental Results

### Model Comparison

| Model                     | Accuracy  | Precision | Recall    | F1 Score  | AUC       |
| ------------------------- | :-------:  | :-------: | :-------: | :-------: | :-------: |
| Logistic Regression       | 0.612     | 0.383     | 0.899     | 0.537     | 0.721     |
| Random Forest             | 0.808     | 0.618     | 0.609     | 0.613     | 0.859     |
| XGBoost                   | 0.781     | 0.551     | 0.667     | 0.603     | 0.854     |
| LightGBM                  | 0.777     | 0.545     | 0.659     | 0.597     | 0.849     |
| **ContractGraph-RiskNet** | **0.792** | **0.560** | **0.775** | **0.650** | **0.871** |

### Key Results

| Metric   | Score    |
| -------- | -------- |
| Accuracy | 79.16 %  |
| F1 Score | 65.04 %  |
| AUC      | 87.07 %  |

> The proposed model achieved the **highest AUC score**, showing improved risk separation ability.

---

## 🔍 Explainable AI

Model interpretation is performed using:

- Feature importance analysis
- SHAP explanations

Risk contribution is analyzed from:

- Project attributes
- Knowledge graph features
- Semantic contract features

---

## 🧬 Ablation Study

To validate the Knowledge Graph contribution:

| Experiment            | Recall    | F1        |
| --------------------- | :-------: | :-------: |
| Without Contract KG   | 0.725     | 0.635     |
| **With Contract KG**  | **0.775** | **0.650** |

> The Knowledge Graph improves risk detection by capturing hidden contractual dependencies.

---

## 📈 Generated Research Figures

```text
figures/
├── Fig1 System Architecture Diagram
├── Fig2 Risk Distribution
├── Fig3 Knowledge Graph
├── Fig4 Model Performance
├── Fig5 ROC Curve
├── Fig6 Confusion Matrix
├── Fig7 Ablation Study
└── Fig8 Feature Importance
```

---

## 🚀 Deployment Prototype

A complete **AI Project Control Room** was developed for real-world demonstration.

### Frontend

**Technology:**

- React
- TypeScript
- TailwindCSS
- Recharts

**Modules:**

#### 📄 Contract Baseline Analyzer

Uploads EPC/HAM contracts and extracts:

- Clauses
- Risks
- Milestones
- Obligations

#### 📊 DPR Monitoring System

Compares monthly progress reports:

```text
Planned Progress   vs   Actual Progress
```

Generates:

- Schedule deviation
- Cost deviation
- Risk escalation

#### 🛰️ Digital Twin Dashboard

Displays:

- Risk evolution
- Timeline analysis
- Delay propagation
- Recovery planning

---

## 🤖 AI Contract Assistant

Implemented using:

- Retrieval Augmented Generation (RAG)
- Groq Llama Models

The assistant receives:

- Contract information
- Risk outputs
- DPR history

…and provides **project-specific explanations**.

---

## 🛠️ Technology Stack

### Research

- Python
- PyTorch
- Scikit-learn
- NetworkX
- Node2Vec
- NLP

### Backend

- FastAPI
- MongoDB Atlas
- pdfplumber
- Groq API

### Frontend

- React
- TypeScript
- Tailwind CSS

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/username/ContractGraph-RiskNet.git
cd ContractGraph-RiskNet
```

### Install Backend

```bash
cd Website/backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
python main.py
```

### Run Frontend

```bash
cd Website/frontend
npm install
npm run dev
```

---

## 📁 Repository Structure

```text
ContractGraph-RiskNet/
│
├── Notebook/
│   └── ContractGraph_RiskNet.ipynb
│
├── Dataset/
│   ├── HighwayRiskDataset.csv
│   └── ContractGraph_FinalDataset.csv
│
├── Models/
│   ├── ContractGraph_RiskNet.pt
│   └── pickle artifacts (.pkl)
│
├── Results/
│   └── figures/
│
└── Website/
    ├── backend/   (FastAPI)
    └── frontend/  (React)
```

---

## 🏆 Research Contribution

The major contributions are:

1. **Contract-aware Knowledge Graph** construction for infrastructure risk reasoning.
2. **Hybrid fusion** of structured project features, graph embeddings, and semantic contract vectors.
3. **Deep learning based ContractGraph-RiskNet** prediction model.
4. **Explainable risk intelligence** using SHAP and feature analysis.
5. **Full-stack Digital Twin prototype** for real-world infrastructure monitoring.

---

## 🔮 Future Work

- Integration of Large Language Models for end-to-end clause extraction.
- Expansion of the Contract Risk Knowledge Graph with multi-domain contracts.
- Graph Neural Network (GNN) based reasoning instead of Node2Vec embeddings.
- Real-time risk streaming from live project management systems.
- Multi-lingual contract support for global infrastructure projects.

---

## 📚 Citation

If you use this work in your research, please cite:

```bibtex
@software{contractgraph_risknet,
  title   = {ContractGraph-RiskNet: A Neuro-Symbolic AI Framework for
             Infrastructure Contract Risk Prediction using Knowledge Graphs
             and Deep Learning},
  author  = {Pavan P S},
  year    = {2026},
  url     = {https://github.com/username/ContractGraph-RiskNet}
}
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code follows the project's style guidelines and includes appropriate documentation.

---


## 👥 Authors

- **Pavan P S** — *Research & Development* — [@thepavan1](https://github.dev/thepavan1/)

---

## 🙏 Acknowledgements

- World Bank Standard Procurement Documents
- Government Infrastructure Contract Corpus
- Open-source communities: PyTorch, Scikit-learn, NetworkX, FastAPI, React

---

<div align="center">

### ContractGraph-RiskNet

**From Contracts → Knowledge → Prediction → Action**

⭐ If you find this project useful, please consider giving it a star!

</div>
