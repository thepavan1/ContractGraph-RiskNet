import { useState } from 'react';
import { HelpCircle, ChevronDown, ChevronUp } from 'lucide-react';

const QAPage = () => {
  const [openCategory, setOpenCategory] = useState<string | null>("Research & Novelty");
  const [openQuestion, setOpenQuestion] = useState<number | null>(0);

  const categories = [
    {
      name: "Research & Novelty",
      items: [
        { q: "What is the primary contribution of ContractGraph-RiskNet?", a: "It bridges the gap between static legal contracts and dynamic execution data. By creating a 'Digital Twin' of the contract baseline and continually comparing it against monthly DPRs, it provides real-time, mathematically backed risk quantification and LD exposure forecasting, which is currently absent in standard EPC monitoring." },
        { q: "Why use a Neuro-Symbolic architecture?", a: "Pure deep learning cannot reason about explicit legal clauses (Symbolic logic), and pure rule-based systems cannot generalize execution risks (Neural logic). ContractGraph-RiskNet combines NLP/KG for symbolic representation of the contract with an MLP for predictive neural modeling, offering both accuracy and explainability." }
      ]
    },
    {
      name: "Data & Processing",
      items: [
        { q: "How is the Contract Baseline extracted?", a: "We use the pdfplumber library coupled with regex-based pattern matching to extract the Project Identity, Contract Value, Milestone Schedule, Material Requirements, and Legal Obligations directly from the uploaded EPC/HAM PDF." },
        { q: "How does the Deviation Engine work?", a: "It compares the Expected Progress (from the Baseline) against the Actual Progress (from the monthly DPR). It calculates deterministic metrics like SPI (Schedule Performance Index) and CPI (Cost Performance Index) and triggers risk warnings if delays breach threshold limits." }
      ]
    },
    {
      name: "Machine Learning (ML)",
      items: [
        { q: "What is the purpose of the Node2Vec embedding?", a: "Node2Vec maps the topological structure of the project's Knowledge Graph into a dense vector space. This allows the MLP to understand the causal relationships between different risk factors (e.g., how a 'Land Acquisition Delay' node is structurally connected to a 'Financial Penalty' node)." },
        { q: "How does the SHAP explainer work?", a: "SHAP (SHapley Additive exPlanations) breaks down the MLP's final risk prediction. It assigns an 'impact value' to each feature (like Cost, State Risk, or Semantic Clause Severity), allowing the user to see exactly WHY the model predicted a high risk score." }
      ]
    },
    {
      name: "System Workflows",
      items: [
        { q: "What happens if I upload a DPR without a Contract Baseline?", a: "The system will block the DPR analysis. The deviation engine mathematically requires a Baseline (Expected Progress, Total Duration, Contract Value) to compute the variances and penalty exposures." },
        { q: "How does the Recovery Simulator calculate recovery days?", a: "It uses standard engineering productivity rates (e.g., 0.08 days recovered per worker, 0.35 per machine) multiplied by shift factors. It caps the maximum recoverable delay at 70% to maintain realistic engineering constraints, and recalculates the risk category post-recovery." }
      ]
    },
    {
      name: "AI Expert (RAG)",
      items: [
        { q: "Why doesn't the AI Expert ask for project details?", a: "We implemented Context-Aware RAG. Before your message is sent to the LLM (Llama-3 via Groq), the backend injects the complete project profile—including baseline, deviations, LD exposure, and SHAP features—directly into the system prompt. The AI already knows everything about the active project." },
        { q: "Can the AI hallucinate penalty values?", a: "It is highly constrained. The system prompt forces the LLM to only cite the LD Exposure and Schedule Variances explicitly provided in the injected JSON context. It acts as an analytical synthesizer rather than an open-ended generator." }
      ]
    },
    {
      name: "Deployment & Architecture",
      items: [
        { q: "What database is used and why?", a: "MongoDB Atlas is used as the primary persistence layer because project profiles (Baseline + Array of DPRs) are inherently document-oriented (JSON). A Memory-DB fallback is implemented for demo environments where cluster access might be restricted." },
        { q: "How is global state managed in the frontend?", a: "Through a unified React Context (ProjectContext). Whenever a project is selected, the context fetches the `/complete-profile` endpoint. All pages (Dashboard, Control Room, Recovery, RAG) consume from this single source of truth, ensuring zero data inconsistency." }
      ]
    }
  ];

  return (
    <div className="flex flex-col gap-5 mt-2 max-w-4xl mx-auto w-full">
      <div className="text-center mb-4">
        <h2 className="text-2xl font-bold text-white flex items-center justify-center gap-2"><HelpCircle className="text-primary" size={22} /> Project Q&A Defense</h2>
        <p className="text-slate-400 text-sm mt-1">Common academic and technical defense questions</p>
      </div>

      <div className="space-y-4">
        {categories.map((cat, cIdx) => (
          <div key={cIdx} className="glass-card overflow-hidden">
            <button 
              className="w-full p-4 flex items-center justify-between bg-slate-800/50 hover:bg-slate-800 transition-colors"
              onClick={() => {
                setOpenCategory(openCategory === cat.name ? null : cat.name);
                setOpenQuestion(null);
              }}
            >
              <h3 className="font-bold text-white text-sm">{cat.name}</h3>
              {openCategory === cat.name ? <ChevronUp size={18} className="text-primary" /> : <ChevronDown size={18} className="text-slate-500" />}
            </button>
            
            {openCategory === cat.name && (
              <div className="p-2 space-y-2 bg-slate-900/50">
                {cat.items.map((item, qIdx) => (
                  <div key={qIdx} className="border border-slate-700 rounded-lg overflow-hidden">
                    <button 
                      className="w-full p-3 flex items-center justify-between text-left hover:bg-slate-800/80 transition-colors"
                      onClick={() => setOpenQuestion(openQuestion === qIdx ? null : qIdx)}
                    >
                      <span className={`text-xs font-medium ${openQuestion === qIdx ? 'text-primary' : 'text-slate-300'}`}>{item.q}</span>
                      {openQuestion === qIdx ? <ChevronUp size={14} className="text-primary shrink-0 ml-2" /> : <ChevronDown size={14} className="text-slate-500 shrink-0 ml-2" />}
                    </button>
                    {openQuestion === qIdx && (
                      <div className="p-4 bg-slate-900 border-t border-slate-800 text-xs text-slate-300 leading-relaxed">
                        {item.a}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default QAPage;
