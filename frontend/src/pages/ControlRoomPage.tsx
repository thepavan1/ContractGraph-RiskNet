import { useProject } from '../context/ProjectContext';
import { Network, Clock, ShieldAlert, Cpu, Loader2, ArrowRight, Download } from 'lucide-react';
import api from '../api';

const ControlRoomPage = () => {
  const { activeProject, profile, profileLoading } = useProject();
  if (!activeProject) return <div className="text-white p-6">Select a project to continue.</div>;
  if (profileLoading || !profile) return <div className="text-white p-6 flex items-center gap-2"><Loader2 className="animate-spin text-primary" /> Loading Digital Twin...</div>;

  const d = profile.deviations;
  const delay = d.estimated_delay_days ?? 0;
  const currentProgress = profile.dpr_reports?.length ? profile.dpr_reports[profile.dpr_reports.length - 1].actual_progress : 0;
  const plannedProgress = profile.dpr_reports?.length ? profile.dpr_reports[profile.dpr_reports.length - 1].planned_progress : 0;

  // Predicted completion
  const remainingWork = 100 - currentProgress;
  const monthlyRate = currentProgress / Math.max(profile.dpr_reports.length, 1);
  const monthsToComplete = monthlyRate > 0 ? Math.ceil(remainingWork / monthlyRate) : 99;
  const predictedTotalMonths = profile.dpr_reports.length + monthsToComplete;

  const handleExport = async () => {
    try {
      const res = await api.get(`/projects/${activeProject.id}/generate-report`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `AI_Risk_Report_${activeProject.name.replace(/ /g, '_')}.pdf`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch { alert("Report generation failed."); }
  };

  return (
    <div className="flex flex-col gap-5 mt-2">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold text-white flex items-center gap-2"><Network className="text-primary" size={22} /> Project Digital Twin</h2>
          <p className="text-slate-400 text-sm mt-1"><strong className="text-white">{activeProject.name}</strong></p>
        </div>
        <button onClick={handleExport} className="bg-accent hover:bg-emerald-600 text-white font-bold py-2 px-4 rounded-lg text-xs flex items-center gap-2">
          <Download size={14} /> Export Report
        </button>
      </div>

      {/* Plan vs Reality vs Prediction */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-card p-4 border-t-4 border-t-blue-500">
          <h4 className="text-xs font-bold text-blue-400 uppercase tracking-widest mb-3">Original Plan</h4>
          <div className="space-y-2 text-xs text-slate-300">
            <div className="flex justify-between"><span>Duration</span><span className="text-white font-bold">{profile.baseline.milestones?.length * 2 || 24} Months</span></div>
            <div className="flex justify-between"><span>Expected Progress</span><span className="text-white font-bold">{plannedProgress}%</span></div>
            <div className="flex justify-between"><span>Contract Value</span><span className="text-white font-bold">₹{profile.baseline.contract_value} Cr</span></div>
          </div>
        </div>
        <div className={`glass-card p-4 border-t-4 ${delay > 15 ? 'border-t-red-500' : 'border-t-green-500'} relative overflow-hidden`}>
          <div className={`absolute -right-10 -top-10 w-32 h-32 rounded-full blur-3xl opacity-20 animate-pulse ${delay > 15 ? 'bg-red-500' : 'bg-green-500'}`} />
          <h4 className="text-xs font-bold text-orange-400 uppercase tracking-widest mb-3 flex items-center justify-between">
            Current Reality
            <span className="flex items-center gap-1 text-[8px] bg-slate-800 px-2 py-0.5 rounded text-white"><span className={`w-1.5 h-1.5 rounded-full animate-pulse ${delay > 15 ? 'bg-red-500' : 'bg-green-500'}`} /> LIVE</span>
          </h4>
          <div className="space-y-2 text-xs text-slate-300 relative z-10">
            <div className="flex justify-between"><span>Actual Progress</span><span className="text-white font-bold">{currentProgress}%</span></div>
            <div className="flex justify-between"><span>Schedule Status</span><span className={`font-bold ${delay > 0 ? 'text-red-400' : 'text-green-400'}`}>{d.schedule_status}</span></div>
            <div className="flex justify-between"><span>Delay</span><span className="text-red-400 font-bold">{delay} days</span></div>
          </div>
        </div>
        <div className="glass-card p-4 border-t-4 border-t-purple-500">
          <h4 className="text-xs font-bold text-purple-400 uppercase tracking-widest mb-3">AI Prediction</h4>
          <div className="space-y-2 text-xs text-slate-300">
            <div className="flex justify-between"><span>At Current Rate</span><span className="text-white font-bold">~{predictedTotalMonths} months total</span></div>
            <div className="flex justify-between"><span>LD Exposure</span><span className="text-red-400 font-bold">₹{d.ld_penalty_exposure_crores} Cr</span></div>
            <div className="flex justify-between"><span>Risk Level</span><span className="text-white font-bold">{profile.risk.category}</span></div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Timeline */}
        <div className="glass-card p-5">
          <h3 className="text-sm font-bold text-white mb-4 flex items-center gap-2"><Clock className="text-blue-400" size={16} /> Schedule Baseline</h3>
          <div className="relative border-l-2 border-slate-700 ml-2 space-y-4">
            {profile.timeline.map((m: any, i: number) => (
              <div key={i} className="pl-5 relative">
                <div className="absolute w-2.5 h-2.5 bg-slate-400 rounded-full -left-[6px] top-1 border border-slate-900" />
                <h4 className="text-xs font-bold text-slate-200">{m.name}</h4>
                <p className="text-[10px] text-slate-500">{m.planned_start} → {m.planned_end} | {m.weightage}%</p>
              </div>
            ))}
          </div>
        </div>

        {/* Risk Chain + SHAP */}
        <div className="lg:col-span-2 flex flex-col gap-4">
          {profile.risk_chain.length > 0 && (
            <div className="glass-card p-5 border border-red-500/30 bg-red-500/5">
              <h3 className="text-sm font-bold text-white mb-4 flex items-center gap-2"><ShieldAlert className="text-red-400" size={16} /> Risk Propagation Chain</h3>
              <div className="flex flex-col md:flex-row items-center gap-4 justify-between relative">
                <div className="hidden md:block absolute left-0 right-0 top-1/2 h-0.5 bg-slate-800 -translate-y-1/2 z-0" />
                {profile.risk_chain.map((r: any, i: number) => (
                  <div key={i} className="flex items-center gap-2 w-full relative z-10">
                    <div className={`bg-slate-900 border-2 ${i === profile.risk_chain.length - 1 ? 'border-red-500 shadow-[0_0_15px_rgba(239,68,68,0.2)]' : 'border-slate-700'} p-3 rounded-lg flex-1 text-center transition-all hover:-translate-y-1`}>
                      <span className={`text-xs font-bold ${i === profile.risk_chain.length - 1 ? 'text-white' : 'text-red-400'} block`}>{r.node}</span>
                      <span className="text-[10px] text-slate-400">{r.desc}</span>
                    </div>
                    {i < profile.risk_chain.length - 1 && <ArrowRight size={16} className="text-red-500/50 hidden md:block shrink-0 bg-slate-900 rounded-full" />}
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="glass-card p-5 border-t-4 border-t-accent">
            <h3 className="text-sm font-bold text-white mb-3 flex items-center gap-2"><Cpu className="text-accent" size={16} /> SHAP Feature Analysis</h3>
            <div className="space-y-2">
              {profile.risk.shap_values.map((s: any, i: number) => (
                <div key={i} className="flex justify-between items-center bg-slate-900 p-2 rounded border border-slate-800 text-xs">
                  <span className="text-slate-300">{s.feature}</span>
                  <span className="text-accent font-bold">+{s.impact_value.toFixed(3)}</span>
                </div>
              ))}
            </div>
            <p className="text-[10px] text-slate-500 mt-3">{profile.risk.shap_values[0]?.description}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ControlRoomPage;
