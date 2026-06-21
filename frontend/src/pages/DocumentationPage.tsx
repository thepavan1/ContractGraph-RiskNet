import { BookOpen } from 'lucide-react';

const DocumentationPage = () => {
  const sections = [
    {
      title: "1. Abstract",
      content: "ContractGraph-RiskNet is a Neuro-Symbolic AI platform for Indian Infrastructure projects. It combines Natural Language Processing (NLP) for contract extraction, Graph Neural Networks (Node2Vec) for topological risk modeling, and standard ML (MLP) for execution risk prediction. The system acts as a Digital Twin, simulating delays, liquidated damages (LD), and engineering recovery strategies."
    },
    {
      title: "2. Problem Statement",
      content: "Indian EPC (Engineering, Procurement, and Construction) and HAM (Hybrid Annuity Model) projects suffer from chronic cost overruns and schedule delays due to disconnected contract baselines, manual Monthly Progress Reports (DPRs), and lack of causal risk traceability. Existing systems cannot predict the cascading financial penalties of early-stage delays."
    },
    {
      title: "3. Objectives",
      content: "1. Automate the extraction of milestones, materials, and obligations from contract PDFs.\n2. Compare monthly DPRs against the contract baseline to calculate SPI, CPI, and activity-level delays.\n3. Predict future project health and LD exposure using a Neuro-Symbolic pipeline.\n4. Provide an engineering-grade What-If recovery simulator."
    },
    {
      title: "4. Existing System",
      content: "Current infrastructure monitoring relies on manual Primavera P6 or MS Project updates. Risk is assessed qualitatively by consultants. Contractual obligations are stored in static PDFs, disconnected from execution data. There is no automated early-warning system for liquidated damages."
    },
    {
      title: "5. Proposed System",
      content: "We propose an end-to-end AI platform that ingests the contract to create a 'Baseline Snapshot'. Monthly DPR uploads automatically trigger deviation analysis. A Knowledge Graph maps causal relationships between delays and contract clauses, feeding into an ML model that predicts execution risk and generates actionable recovery plans via a RAG-based AI Expert."
    },
    {
      title: "6. Dataset",
      content: "The system is validated on a curated dataset of Indian highway contracts (NHAI) and corresponding monthly DPRs. The dataset includes various risk profiles: NO RISK (on track), LOW, MEDIUM, HIGH, and CRITICAL (severe delays activating LD clauses)."
    },
    {
      title: "7. Knowledge Graph Architecture",
      content: "The KG represents the project topology. Nodes include Activities (Earthwork, Paving), Resources (Labor, Machinery), and Contract Clauses (Penalty, Force Majeure). Edges represent causal links (e.g., 'Delay in Earthwork' -> 'Triggers' -> 'LD Clause')."
    },
    {
      title: "8. Node2Vec Embedding",
      content: "Node2Vec is used to learn continuous feature representations for the nodes in the Knowledge Graph. It performs random walks to capture both the local neighborhood (homophily) and structural equivalence of project risks, converting topological risk into mathematical vectors."
    },
    {
      title: "9. Semantic Encoder",
      content: "A TF-IDF + SVD (Singular Value Decomposition) pipeline processes the extracted contract clauses. It identifies high-risk keywords ('penalty', 'termination', 'liquidated') and encodes the severity of the contract's legal framework into dense semantic features."
    },
    {
      title: "10. Model Architecture",
      content: "The final prediction engine is a Multi-Layer Perceptron (MLP). It concatenates:\n1. Base Project Features (Cost, State, Duration)\n2. Semantic Clause Embeddings\n3. Node2Vec Topological Embeddings\n\nThe MLP outputs a normalized probability representing the overall Contractual Risk Exposure."
    },
    {
      title: "11. Deviation Engine (Execution Risk)",
      content: "The Deviation Engine is deterministic. It compares the DPR Actual Progress against the Baseline Expected Progress. It calculates the Schedule Performance Index (SPI), Cost Performance Index (CPI), and Activity-Level Variances to generate a real-time Execution Risk score and estimated Delay Days."
    },
    {
      title: "12. Recovery Simulator",
      content: "An engineering-based What-If module. It uses standard productivity rates (e.g., 1 worker = 0.08 days recovered/day) and shift multipliers to calculate how additional resources (labor, machinery, budget) can reduce the delay days and lower the risk category."
    },
    {
      title: "13. Context-Aware RAG Expert",
      content: "A Llama-3 based AI assistant. It does not require user context. The backend injects the complete project profile (baseline, deviations, SHAP explanations, LD exposure) directly into the system prompt, enabling the AI to give highly specific, mathematically backed recovery advice."
    },
    {
      title: "14. SHAP Explainability",
      content: "SHapley Additive exPlanations (SHAP) is integrated to deconstruct the ML prediction. It provides a ranked list of features (e.g., 'High Cost', 'Strict Legal Clause', 'State Risk') that contributed most significantly to the predicted risk score, ensuring transparency."
    },
    {
      title: "15. Future Scope",
      content: "1. Integration with real-time IoT sensors on heavy machinery for automated progress tracking.\n2. Expanding the Knowledge Graph to cross-reference past dispute resolution outcomes.\n3. Direct integration with NHAI's Data Lake (Bhoomi Rashi) for automated land acquisition risk assessment."
    }
  ];

  return (
    <div className="flex flex-col gap-5 mt-2">
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2"><BookOpen className="text-primary" size={22} /> Research Documentation</h2>
        <p className="text-slate-400 text-sm mt-1">Neuro-Symbolic Architecture & Mathematical Formulations</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {sections.map((section, i) => (
          <div key={i} className="glass-card p-5 border-t border-slate-700 hover:border-primary transition-colors">
            <h3 className="text-sm font-bold text-white mb-2">{section.title}</h3>
            <p className="text-xs text-slate-300 leading-relaxed whitespace-pre-wrap">{section.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DocumentationPage;
