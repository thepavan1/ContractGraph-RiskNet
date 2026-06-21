import { useState } from 'react';
import { HardHat, Wrench, Clock, Zap, IndianRupee, Loader2, ArrowRight } from 'lucide-react';
import api from '../api';
import { useProject } from '../context/ProjectContext';

const ActionCenterPage = () => {
  const { activeProject, profile } = useProject();
  const [workers, setWorkers] = useState(0);
  const [excavators, setExcavators] = useState(0);
  const [shifts, setShifts] = useState(1);
  const [budget, setBudget] = useState(0);
  const [simulating, setSimulating] = useState(false);
  const [result, setResult] = useState<any>(null);

  if (!activeProject) return <div className="text-white p-6">Select a project to continue.</div>;

  const delay = profile?.deviations?.estimated_delay_days ?? 0;
  const currentRisk = profile?.deviations?.execution_risk_score ?? 0;

  const handleSimulate = async () => {
    setSimulating(true);
    try {
      const res = await api.post(`/projects/${activeProject.id}/simulate`, { workers, excavators, shifts, budget });
      setResult(res.data);
    } catch { console.error("Simulation failed"); }
    finally { setSimulating(false); }
  };

  return (
    <div className="flex flex-col gap-5 mt-2">
      <div>
        <h2 className="text-2xl font-bold text-white">Recovery Simulator</h2>
        <p className="text-slate-400 text-sm mt-1">Engineering-grade What-If analysis for <strong className="text-white">{activeProject.name}</strong></p>
      </div>

      {/* Current Status */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="glass-card p-3 border-b-4 border-b-red-500">
          <span className="text-[10px] text-slate-400 uppercase tracking-widest font-bold block">Current Delay</span>
          <span className="text-xl font-black text-red-400">{delay} days</span>
        </div>
        <div className="glass-card p-3 border-b-4 border-b-orange-500">
          <span className="text-[10px] text-slate-400 uppercase tracking-widest font-bold block">Execution Risk</span>
          <span className="text-xl font-black text-orange-400">{currentRisk}%</span>
        </div>
        <div className="glass-card p-3 border-b-4 border-b-purple-500">
          <span className="text-[10px] text-slate-400 uppercase tracking-widest font-bold block">LD Exposure</span>
          <span className="text-xl font-black text-white">₹{profile?.deviations?.ld_penalty_exposure_crores ?? 0} Cr</span>
        </div>
        <div className="glass-card p-3 border-b-4 border-b-blue-500">
          <span className="text-[10px] text-slate-400 uppercase tracking-widest font-bold block">Status</span>
          <span className="text-xl font-black text-white">{profile?.deviations?.schedule_status ?? "ON TRACK"}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Inputs */}
        <div className="glass-card p-5">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2"><Wrench size={18} className="text-primary" /> Resource Inputs</h3>
          <div className="space-y-4">
            <InputSlider icon={<HardHat size={14} />} label="Additional Workers" value={workers} onChange={setWorkers} max={200} unit="workers" step={5} />
            <InputSlider icon={<Wrench size={14} />} label="Additional Excavators/Machines" value={excavators} onChange={setExcavators} max={30} unit="machines" step={1} />
            <div>
              <label className="block text-xs text-slate-300 mb-1 flex items-center gap-1"><Clock size={14} /> Working Shifts</label>
              <select value={shifts} onChange={(e) => setShifts(Number(e.target.value))} className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white text-sm">
                <option value={1}>1 Shift (8 hrs)</option>
                <option value={2}>2 Shifts (16 hrs)</option>
                <option value={3}>3 Shifts (24/7)</option>
              </select>
            </div>
            <InputSlider icon={<IndianRupee size={14} />} label="Additional Budget" value={budget} onChange={setBudget} max={10} unit="Cr" step={0.5} />
          </div>

          <button className="w-full bg-primary hover:bg-blue-600 text-white font-bold py-3 rounded-lg text-sm mt-5 flex items-center justify-center gap-2 disabled:opacity-50" onClick={handleSimulate} disabled={simulating || delay === 0}>
            {simulating ? <><Loader2 size={16} className="animate-spin" /> Running...</> : <><Zap size={16} /> Simulate Recovery</>}
          </button>
          {delay === 0 && <p className="text-xs text-slate-500 text-center mt-2">No delay detected — simulation not needed.</p>}
        </div>

        {/* Results */}
        <div className="glass-card p-5 flex flex-col justify-center">
          {result ? (
            <div className="space-y-5">
              <h3 className="text-lg font-bold text-white mb-2">Recovery Analysis</h3>

              <div className="flex items-center justify-between gap-4">
                <div className="text-center flex-1 p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
                  <span className="text-[10px] text-red-400 uppercase font-bold block">Before</span>
                  <span className="text-xl font-black text-red-400">{result.risk_before}</span>
                </div>
                <ArrowRight className="text-slate-500 shrink-0" />
                <div className="text-center flex-1 p-3 bg-green-500/10 border border-green-500/30 rounded-lg">
                  <span className="text-[10px] text-green-400 uppercase font-bold block">After</span>
                  <span className="text-xl font-black text-green-400">{result.risk_after}</span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <Stat label="Recovered Days" value={`${result.recovered_days}`} />
                <Stat label="Remaining Delay" value={`${result.remaining_delay_days} days`} />
                <Stat label="Productivity Gain" value={`${result.productivity_increase_percent}%`} />
                <Stat label="Recovery Cost" value={`₹${result.recovery_cost_crores} Cr`} />
              </div>
            </div>
          ) : (
            <div className="text-center text-slate-500">
              <Wrench size={40} className="mx-auto mb-3 opacity-20" />
              <p className="text-sm">Configure resources and run the simulation.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const InputSlider = ({ icon, label, value, onChange, max, unit, step }: any) => (
  <div>
    <label className="block text-xs text-slate-300 mb-1 flex items-center gap-1">{icon} {label}</label>
    <input type="range" min="0" max={max} step={step} value={value} onChange={(e) => onChange(Number(e.target.value))} className="w-full accent-primary" />
    <div className="text-right text-[10px] text-slate-400">+{value} {unit}</div>
  </div>
);

const Stat = ({ label, value }: { label: string; value: string }) => (
  <div className="bg-slate-900 border border-slate-800 p-3 rounded-lg text-center">
    <span className="text-[10px] text-slate-500 uppercase font-bold block">{label}</span>
    <span className="text-sm font-black text-white">{value}</span>
  </div>
);

export default ActionCenterPage;
