import { useState, useRef } from 'react';
import { Upload, FileText, BarChart3, Activity, AlertTriangle } from 'lucide-react';
import api from '../api';
import { useProject } from '../context/ProjectContext';

const ReportPage = () => {
  const { activeProject, profile, refreshProfile } = useProject();
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!activeProject) return <div className="text-white p-6">Select a project to continue.</div>;

  const handleUpload = async () => {
    if (!file || !activeProject) return;
    setLoading(true);
    try {
      const fd = new FormData();
      fd.append('project_id', activeProject.id);
      fd.append('file', file);
      const res = await api.post('/reports/upload', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
      setResult(res.data);
      refreshProfile();
    } catch { alert("DPR processing failed."); }
    finally { setLoading(false); }
  };

  // Show latest DPR from context if no fresh upload
  const data = result || (profile?.dpr_reports?.length ? profile.dpr_reports[profile.dpr_reports.length - 1] : null);

  return (
    <div className="flex flex-col gap-5 mt-2">
      <div>
        <h2 className="text-2xl font-bold text-white">Monthly DPR Upload</h2>
        <p className="text-slate-400 text-sm mt-1">Upload DPR for <strong className="text-white">{activeProject.name}</strong> — compares against contract baseline</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Upload Panel */}
        <div className="glass-card p-5 flex flex-col gap-3">
          <h3 className="text-lg font-bold text-white">Upload DPR PDF</h3>
          <div className="flex-1 min-h-[150px] bg-slate-900/50 border-dashed border-2 border-slate-600 rounded-lg flex flex-col items-center justify-center cursor-pointer hover:border-primary transition-colors" onClick={() => fileInputRef.current?.click()}>
            <input type="file" className="hidden" ref={fileInputRef} onChange={(e) => e.target.files?.[0] && setFile(e.target.files[0])} accept=".pdf" />
            <Upload size={28} className="text-primary mb-2" />
            <p className="text-white font-medium text-xs">Click to select DPR</p>
            {file && <div className="mt-2 bg-slate-800 px-2 py-1 rounded text-[10px] text-accent flex items-center gap-1"><FileText size={10} /> {file.name}</div>}
          </div>
          <button className="w-full bg-primary hover:bg-blue-600 text-white font-bold py-2.5 rounded-lg text-sm disabled:opacity-50" disabled={!file || loading} onClick={handleUpload}>
            {loading ? "Processing..." : "Analyze DPR"}
          </button>
        </div>

        {/* Results */}
        <div className="lg:col-span-2 flex flex-col gap-4">
          {data ? (
            <>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <Metric title="Health" value={`${data.overall_health_score?.toFixed?.(1) ?? data.overall_health_score}%`} good={(data.overall_health_score ?? 0) > 70} />
                <Metric title="Execution Risk" value={`${data.execution_risk_score?.toFixed?.(1) ?? data.execution_risk_score}%`} good={(data.execution_risk_score ?? 0) < 30} />
                <Metric title="Delay" value={`${data.estimated_delay_days} days`} good={(data.estimated_delay_days ?? 0) < 5} />
                <Metric title="LD Exposure" value={`₹${data.ld_penalty_exposure_crores} Cr`} good={(data.ld_penalty_exposure_crores ?? 0) === 0} />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Baseline vs DPR */}
                <div className="glass-card p-4">
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3 flex items-center gap-2"><Activity size={14} className="text-blue-400" /> Baseline vs DPR</h4>
                  <div className="space-y-2 text-xs text-slate-300">
                    <Row label="Planned Progress" value={`${data.planned_progress}%`} />
                    <Row label="Actual Progress" value={`${data.actual_progress}%`} />
                    <Row label="Schedule Variance" value={`${data.schedule_variance}%`} warn={data.schedule_variance < -5} />
                    <Row label="SPI" value={data.spi ?? "N/A"} warn={(data.spi ?? 1) < 0.9} />
                    <Row label="CPI" value={data.cpi ?? "N/A"} warn={(data.cpi ?? 1) < 0.9} />
                    <Row label="Status" value={data.schedule_status || "ON TRACK"} warn={data.schedule_status?.includes("DELAY")} />
                  </div>
                </div>

                {/* Delayed Activities */}
                <div className="glass-card p-4">
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3 flex items-center gap-2"><AlertTriangle size={14} className="text-orange-400" /> Delayed Activities</h4>
                  {(data.delayed_activities?.length ?? 0) > 0 ? (
                    <div className="space-y-2">
                      {data.delayed_activities.map((a: any, i: number) => (
                        <div key={i} className="bg-slate-900 p-2 rounded border border-slate-800 text-xs">
                          <span className="text-white font-medium block">{a.activity}</span>
                          <span className="text-slate-400">Expected: {a.expected}% | Actual: {a.actual}% | <span className="text-red-400 font-bold">{a.variance}%</span></span>
                        </div>
                      ))}
                    </div>
                  ) : <p className="text-xs text-slate-500 italic">No significant activity-level delays detected.</p>}
                </div>
              </div>

              {/* Issues & Mitigation */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {data.issues?.length > 0 && (
                  <div className="glass-card p-4">
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3 flex items-center gap-2"><AlertTriangle size={14} className="text-orange-400" /> Reported Issues</h4>
                    <ul className="space-y-1">
                      {data.issues.map((issue: string, i: number) => (
                        <li key={i} className="flex gap-2 text-xs text-slate-300 bg-slate-900/50 p-2 rounded"><span className="text-orange-400 shrink-0 mt-0.5">•</span>{issue}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {data.mitigation_steps?.length > 0 && (
                  <div className="glass-card p-4 border-l-4 border-l-green-500">
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3 flex items-center gap-2"><Activity size={14} className="text-green-400" /> Recommended Mitigation</h4>
                    <ul className="space-y-1">
                      {data.mitigation_steps.map((step: string, i: number) => (
                        <li key={i} className="flex gap-2 text-xs text-slate-300 bg-slate-900/50 p-2 rounded"><span className="text-green-400 shrink-0 mt-0.5">✓</span>{step}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </>
          ) : (
            <div className="glass-card h-full flex flex-col items-center justify-center p-10 text-slate-500 text-center">
              <BarChart3 size={40} className="mb-3 opacity-20" />
              <p className="text-sm">Upload a DPR to generate deviation analysis.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const Metric = ({ title, value, good }: { title: string; value: string; good: boolean }) => (
  <div className={`glass-card p-3 text-center border-b-4 ${good ? 'border-b-accent' : 'border-b-red-500'}`}>
    <span className="text-[10px] text-slate-400 uppercase tracking-widest font-bold block">{title}</span>
    <span className={`text-lg font-black ${good ? 'text-white' : 'text-red-400'}`}>{value}</span>
  </div>
);

const Row = ({ label, value, warn }: { label: string; value: any; warn?: boolean }) => (
  <div className="flex justify-between border-b border-slate-800 pb-1">
    <span>{label}</span>
    <span className={`font-mono font-bold ${warn ? 'text-red-400' : 'text-white'}`}>{value}</span>
  </div>
);

export default ReportPage;
