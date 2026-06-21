import { useState, useRef, useEffect } from 'react';
import { Send, Loader2, MessageSquare, ShieldAlert, FileText, CheckCircle2 } from 'lucide-react';
import api from '../api';
import { useProject } from '../context/ProjectContext';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const RAGPage = () => {
  const { activeProject, profile } = useProject();
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! I am the ContractGraph-RiskNet AI Expert. I have already loaded the complete profile for your active project. Ask me anything about the schedule, risks, penalty exposure, or recovery plans.' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Reset chat if project changes
  useEffect(() => {
    if (activeProject) {
      setMessages([{ role: 'assistant', content: `Context switched to **${activeProject.name}**. I have analyzed the baseline, recent DPRs, and SHAP risk drivers. What would you like to know?` }]);
    }
  }, [activeProject?.id]);

  if (!activeProject) return <div className="text-white p-6">Select a project to continue.</div>;

  const handleSend = async () => {
    if (!input.trim() || !profile) return;
    
    const userMsg = input.trim();
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setInput('');
    setLoading(true);

    // Prepare context from profile
    const contextStr = JSON.stringify({
      project_name: profile.project.name,
      contract_value: profile.baseline.contract_value,
      current_health: profile.deviations.overall_health_score,
      current_delay_days: profile.deviations.estimated_delay_days,
      ld_exposure_crores: profile.deviations.ld_penalty_exposure_crores,
      delayed_activities: profile.deviations.delayed_activities,
      contract_obligations: profile.baseline.obligations,
      shap_risk_drivers: profile.risk.shap_values,
      latest_issues: profile.dpr_reports[profile.dpr_reports.length - 1]?.issues || []
    }, null, 2);

    try {
      const res = await api.post('/chat', {
        message: userMsg,
        context: contextStr
      });
      setMessages(prev => [...prev, { role: 'assistant', content: res.data.response }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I couldn't reach the AI service right now." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-5 mt-2 h-[calc(100vh-140px)]">
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2"><MessageSquare className="text-primary" size={22} /> Context-Aware AI Expert</h2>
        <p className="text-slate-400 text-sm mt-1">Chatting about <strong className="text-white">{activeProject.name}</strong></p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-5 h-full min-h-0">
        {/* Context Status Panel */}
        <div className="glass-card p-5 hidden lg:flex flex-col gap-4 overflow-y-auto">
          <h3 className="text-sm font-bold text-white mb-2 uppercase tracking-widest text-slate-400">Injected Context</h3>
          
          <div className="space-y-3">
            <ContextItem icon={<FileText size={14} className="text-blue-400" />} label="Project Identity" value={profile?.project.name} />
            <ContextItem icon={<CheckCircle2 size={14} className="text-green-400" />} label="Overall Health" value={`${profile?.deviations?.overall_health_score ?? 100}%`} />
            <ContextItem icon={<ShieldAlert size={14} className="text-orange-400" />} label="Execution Risk" value={`${profile?.deviations?.execution_risk_score ?? 0}%`} />
            <ContextItem icon={<ShieldAlert size={14} className="text-red-400" />} label="LD Exposure" value={`₹${profile?.deviations?.ld_penalty_exposure_crores ?? 0} Cr`} />
          </div>

          <div className="mt-4 pt-4 border-t border-slate-800">
            <span className="text-[10px] text-slate-500 uppercase tracking-widest font-bold block mb-2">Knowledge Graph Integration</span>
            <p className="text-xs text-slate-400 leading-relaxed">
              The AI Expert utilizes Node2Vec embeddings and SHAP values extracted from your contract to provide mathematically backed recovery recommendations.
            </p>
          </div>
        </div>

        {/* Chat Interface */}
        <div className="glass-card lg:col-span-3 flex flex-col h-full overflow-hidden">
          <div className="flex-1 p-5 overflow-y-auto space-y-6">
            {messages.map((m, i) => (
              <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[85%] rounded-2xl px-5 py-3 ${
                  m.role === 'user' 
                    ? 'bg-primary text-white rounded-br-none shadow-lg shadow-primary/20' 
                    : 'bg-slate-800 border border-slate-700 text-slate-200 rounded-bl-none shadow-xl'
                }`}>
                  {m.role === 'assistant' ? (
                    <div className="text-sm leading-relaxed whitespace-pre-wrap font-sans">
                      {m.content}
                    </div>
                  ) : (
                    <p className="text-sm whitespace-pre-wrap font-sans">{m.content}</p>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-slate-800 border border-slate-700 rounded-2xl rounded-bl-none px-5 py-4 shadow-xl">
                  <div className="flex items-center gap-2 text-slate-400">
                    <Loader2 size={16} className="animate-spin" />
                    <span className="text-xs font-medium">Analyzing project data...</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="p-4 border-t border-slate-800 bg-slate-900/50">
            <div className="relative flex items-center">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
                placeholder="Ask about delays, LD clauses, or recovery plans..."
                className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl pl-4 pr-12 py-3 focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary text-sm shadow-inner"
                disabled={loading}
              />
              <button
                onClick={handleSend}
                disabled={!input.trim() || loading}
                className="absolute right-2 p-2 bg-primary hover:bg-blue-600 disabled:bg-slate-700 text-white rounded-lg transition-colors"
              >
                <Send size={16} />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const ContextItem = ({ icon, label, value }: { icon: React.ReactNode, label: string, value: any }) => (
  <div className="flex items-center gap-3 bg-slate-900 p-2 rounded border border-slate-800">
    <div className="shrink-0">{icon}</div>
    <div className="flex-1 min-w-0">
      <span className="text-[10px] text-slate-500 uppercase font-bold block truncate">{label}</span>
      <span className="text-xs font-medium text-white truncate block">{value || "N/A"}</span>
    </div>
  </div>
);

export default RAGPage;
