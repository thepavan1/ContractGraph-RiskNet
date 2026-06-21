import { useState, useRef } from 'react';
import { Upload, FileText, Scale, Construction, IndianRupee, ShieldAlert, Loader2 } from 'lucide-react';
import api from '../api';
import { useProject } from '../context/ProjectContext';

const AnalyzerPage = () => {
  const { activeProject, profile, refreshProfile } = useProject();
  const [file, setFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!activeProject) return <div className="text-white p-6">Select a project to continue.</div>;

  const baseline = profile?.baseline;
  const hasBaseline = baseline && baseline.contract_value > 0;

  const startAnalysis = async () => {
    if (!file || !activeProject) return;
    setIsAnalyzing(true);
    try {
      const fd = new FormData();
      fd.append('project_id', activeProject.id);
      fd.append('file', file);
      const res = await api.post('/extract/baseline', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
      setResult(res.data);
      refreshProfile();
    } catch { alert("Extraction failed."); }
    finally { setIsAnalyzing(false); }
  };

  const data = result || (hasBaseline ? { ...baseline, risk_breakdown: profile?.risk?.risk_breakdown } : null);

  return (
    <div className="flex flex-col gap-5 mt-2">
      <div>
        <h2 className="text-2xl font-bold text-white">Contract Baseline Analyzer</h2>
        <p className="text-slate-400 text-sm mt-1">Extract obligations for <strong className="text-white">{activeProject.name}</strong></p>
      </div>

      {/* Upload Section */}
      {!data && !isAnalyzing && (
        <div className="glass-card p-10 flex flex-col items-center border-dashed border-2 border-slate-600 hover:border-primary transition-colors cursor-pointer" onClick={() => fileInputRef.current?.click()}>
          <input type="file" className="hidden" ref={fileInputRef} onChange={(e) => e.target.files?.[0] && setFile(e.target.files[0])} accept=".pdf,.txt" />
          <Upload size={48} className="text-primary mb-4 opacity-80" />
          <h3 className="text-lg font-bold text-white mb-1">Upload Contract PDF</h3>
          <p className="text-slate-400 text-xs text-center max-w-md mb-4">Upload EPC/HAM contract to extract milestones, materials, obligations.</p>
          {file && <div className="flex items-center gap-2 bg-slate-800 px-3 py-1 rounded text-xs text-accent mb-4"><FileText size={14} /> {file.name}</div>}
          <button className="bg-primary hover:bg-blue-600 text-white font-bold py-2 px-6 rounded-lg text-sm disabled:opacity-50 flex items-center gap-2" disabled={!file} onClick={(e) => { e.stopPropagation(); startAnalysis(); }}>
            <Construction size={16} /> Analyze Contract
          </button>
        </div>
      )}

      {isAnalyzing && (
        <div className="glass-card h-64 flex items-center justify-center">
          <div className="flex flex-col items-center"><Loader2 size={40} className="text-primary animate-spin mb-4" /><p className="text-white text-sm">Extracting baseline intelligence...</p></div>
        </div>
      )}

      {data && (
        <div className="space-y-5">
          {/* Project Identity */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <Card label="Project" value={data.project_name || activeProject.name} />
            <Card label="Type" value={data.contract_type || "EPC"} />
            <Card label="State" value={data.state || "N/A"} />
            <Card label="Contract Value" value={`₹${data.contract_value} Cr`} />
          </div>

          {/* Milestones Table */}
          <div className="glass-card p-5">
            <h3 className="text-white font-bold text-sm mb-3 flex items-center gap-2"><Construction size={16} className="text-blue-400" /> Contract Milestones</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="text-slate-500 uppercase bg-slate-900/50">
                  <tr><th className="px-3 py-2">Activity</th><th className="px-3 py-2">Start</th><th className="px-3 py-2">End</th><th className="px-3 py-2">Weight</th></tr>
                </thead>
                <tbody>
                  {data.milestones?.map((m: any, i: number) => (
                    <tr key={i} className="border-b border-slate-800 text-slate-300">
                      <td className="px-3 py-2 font-medium text-white">{m.name}</td>
                      <td className="px-3 py-2">{m.planned_start}</td>
                      <td className="px-3 py-2">{m.planned_end}</td>
                      <td className="px-3 py-2 text-blue-400 font-bold">{m.weightage}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Materials Table */}
          <div className="glass-card p-5">
            <h3 className="text-white font-bold text-sm mb-3 flex items-center gap-2"><IndianRupee size={16} className="text-green-400" /> Material Requirements</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="text-slate-500 uppercase bg-slate-900/50">
                  <tr><th className="px-3 py-2">Material</th><th className="px-3 py-2">Quantity</th><th className="px-3 py-2">Phase</th></tr>
                </thead>
                <tbody>
                  {data.materials?.map((m: any, i: number) => (
                    <tr key={i} className="border-b border-slate-800 text-slate-300">
                      <td className="px-3 py-2 font-medium text-white">{m.name}</td>
                      <td className="px-3 py-2 font-mono">{m.qty}</td>
                      <td className="px-3 py-2">{m.phase}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* 8-Category Risk Breakdown */}
          <div className="glass-card p-5">
            <h3 className="text-white font-bold text-sm mb-3 flex items-center gap-2"><ShieldAlert size={16} className="text-orange-400" /> Multi-Category Risk Intelligence</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {(data.risk_breakdown || profile?.risk?.risk_breakdown || []).map((r: any, i: number) => (
                <div key={i} className="bg-slate-900 border border-slate-800 rounded-lg p-3">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-xs font-bold text-white">{r.name}</span>
                    <span className={`text-xs font-black px-2 py-0.5 rounded ${r.score > 60 ? 'bg-red-500/20 text-red-400' : r.score > 30 ? 'bg-orange-500/20 text-orange-400' : 'bg-green-500/20 text-green-400'}`}>{r.score}%</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-1.5 mb-2">
                    <div className={`h-1.5 rounded-full ${r.score > 60 ? 'bg-red-500' : r.score > 30 ? 'bg-orange-500' : 'bg-green-500'}`} style={{ width: `${r.score}%` }} />
                  </div>
                  <p className="text-[10px] text-slate-400">{r.reason}</p>
                  <p className="text-[10px] text-slate-500 mt-1">Impact: {r.impact}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Obligations */}
          <div className="glass-card p-5">
            <h3 className="text-white font-bold text-sm mb-3 flex items-center gap-2"><Scale size={16} className="text-orange-400" /> Mined Legal Obligations</h3>
            <div className="space-y-2">
              {data.obligations?.map((c: any, i: number) => (
                <div key={i} className="bg-slate-900 p-3 rounded border-l-2 border-l-orange-500 border border-slate-800">
                  <p className="text-xs text-slate-300 italic">"{c.clause}"</p>
                  <span className="text-[10px] uppercase font-bold text-orange-400 mt-1 inline-block">{c.impact}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const Card = ({ label, value }: { label: string; value: string }) => (
  <div className="glass-card p-3">
    <span className="text-[10px] text-slate-500 uppercase tracking-widest font-bold block">{label}</span>
    <span className="text-sm font-bold text-white mt-1 block">{value}</span>
  </div>
);

export default AnalyzerPage;
