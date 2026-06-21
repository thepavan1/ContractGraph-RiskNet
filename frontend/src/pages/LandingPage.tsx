import { motion } from 'framer-motion';
import { Network, FileSearch, BrainCircuit, Activity } from 'lucide-react';

const LandingPage = () => {
  return (
    <div className="flex flex-col gap-12 mt-10">
      {/* Hero Section */}
      <section className="text-center space-y-6">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <div className="inline-block border border-primary/30 bg-primary/10 rounded-full px-4 py-1.5 text-sm text-primary font-medium mb-4">
            NHAI • Smart Cities • Metro Rail
          </div>
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white mb-6">
            AI-Powered Contract <br />
            <span className="text-gradient">Risk Prediction</span>
          </h1>
          <p className="text-lg md:text-xl text-slate-400 max-w-3xl mx-auto leading-relaxed">
            Analyze EPC agreements, government contracts, and progress reports for Indian Infrastructure Projects using Knowledge Graphs, NLP, and Deep Learning to detect project risks before failures occur.
          </p>
        </motion.div>
      </section>

      {/* Architecture Cards */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { icon: FileSearch, title: "Semantic Parsing", desc: "TF-IDF & SVD reduction of contractual clauses" },
          { icon: Network, title: "Graph Embedding", desc: "Node2Vec topological embeddings of risk causality" },
          { icon: BrainCircuit, title: "Deep Fusion", desc: "PyTorch 3-layer neural network (AUC 0.871)" },
          { icon: Activity, title: "RAG Verification", desc: "Llama-3 powered semantic Q&A and retrieval" },
        ].map((item, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: i * 0.1 }}
            className="glass-card p-6 flex flex-col items-center text-center gap-4 hover:-translate-y-2 transition-transform cursor-default"
          >
            <div className="bg-slate-800 p-4 rounded-2xl border border-slate-700">
              <item.icon className="text-primary w-8 h-8" />
            </div>
            <h3 className="text-lg font-semibold text-white">{item.title}</h3>
            <p className="text-sm text-slate-400">{item.desc}</p>
          </motion.div>
        ))}
      </section>

      {/* Problems Section */}
      <section className="glass-card p-8 mt-8 border-orange-500/20">
        <h2 className="text-2xl font-bold mb-6 border-b border-slate-700 pb-4 text-orange-400">Challenges in Indian Infrastructure Projects</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-slate-300">
          <div className="bg-slate-800/50 p-3 rounded-lg border border-slate-700">⚠️ Land acquisition delays</div>
          <div className="bg-slate-800/50 p-3 rounded-lg border border-slate-700">📈 Cost escalation</div>
          <div className="bg-slate-800/50 p-3 rounded-lg border border-slate-700">🌧️ Monsoon schedule delays</div>
          <div className="bg-slate-800/50 p-3 rounded-lg border border-slate-700">⚖️ Contract disputes</div>
          <div className="bg-slate-800/50 p-3 rounded-lg border border-slate-700">👷 Contractor performance issues</div>
          <div className="bg-slate-800/50 p-3 rounded-lg border border-slate-700">💰 Material price fluctuation</div>
          <div className="bg-slate-800/50 p-3 rounded-lg border border-slate-700">🌲 Environmental clearance delays</div>
          <div className="bg-slate-800/50 p-3 rounded-lg border border-slate-700">🏛️ Approvals dependency</div>
        </div>
      </section>

      {/* Diagrams Section */}
      <section className="glass-card p-8 mt-2">
        <h2 className="text-2xl font-bold mb-6 border-b border-slate-700 pb-4">System Architecture & Results</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-slate-300">Methodology</h3>
            <div className="bg-slate-900/80 rounded-xl aspect-video border border-slate-800 flex items-center justify-center relative overflow-hidden">
                <span className="text-slate-500 absolute z-0">Architecture Diagram Placeholder</span>
                <img src="/Fig4.png" alt="Architecture" className="w-full h-full object-contain relative z-10" onError={(e) => e.currentTarget.style.display = 'none'} />
            </div>
          </div>
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-slate-300">Model Performance</h3>
             <div className="bg-slate-900/80 rounded-xl aspect-video border border-slate-800 flex items-center justify-center relative overflow-hidden">
                <span className="text-slate-500 absolute z-0">ROC Curve Placeholder</span>
                <img src="/Fig8.png" alt="ROC Curve" className="w-full h-full object-contain relative z-10" onError={(e) => e.currentTarget.style.display = 'none'} />
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
