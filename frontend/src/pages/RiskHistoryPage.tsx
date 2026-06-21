import { useProject } from '../context/ProjectContext';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RTooltip, Legend, ResponsiveContainer } from 'recharts';
import { Clock, Loader2, ShieldAlert } from 'lucide-react';

const RiskHistoryPage = () => {
  const { activeProject, profile, profileLoading } = useProject();
  if (!activeProject) return <div className="text-white p-6">Select a project to continue.</div>;
  if (profileLoading || !profile) return <div className="text-white p-6 flex items-center gap-2"><Loader2 className="animate-spin text-primary" /> Loading...</div>;

  const history = profile.risk_history || [];
  const chartData = profile.charts.risk_evolution || [];

  return (
    <div className="flex flex-col gap-5 mt-2">
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2"><Clock className="text-primary" size={22} /> Risk Timeline</h2>
        <p className="text-slate-400 text-sm mt-1"><strong className="text-white">{activeProject.name}</strong></p>
      </div>

      {/* Chart */}
      {chartData.length > 0 && (
        <div className="glass-card p-5">
          <h3 className="text-sm font-bold text-white mb-3">Risk Trend</h3>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="month" stroke="#64748b" tick={{ fontSize: 10 }} />
                <YAxis stroke="#64748b" tick={{ fontSize: 10 }} />
                <RTooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', fontSize: 11 }} />
                <Legend wrapperStyle={{ fontSize: 10 }} />
                <Line type="monotone" dataKey="contractRisk" name="Contract Risk" stroke="#8b5cf6" strokeWidth={2} />
                <Line type="monotone" dataKey="executionRisk" name="Execution Risk" stroke="#ef4444" strokeWidth={2} />
                <Line type="monotone" dataKey="totalHealth" name="Health Score" stroke="#10b981" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Event Log */}
      <div className="glass-card p-5">
        <h3 className="text-sm font-bold text-white mb-4">Event Log</h3>
        {history.length > 0 ? (
          <div className="relative border-l-2 border-slate-700 ml-2 space-y-4">
            {history.map((h: any, i: number) => (
              <div key={i} className="pl-5 relative">
                <div className="absolute w-2.5 h-2.5 bg-primary rounded-full -left-[6px] top-1 border border-slate-900" />
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="text-xs font-bold text-white">{h.event}</h4>
                    <p className="text-[10px] text-slate-500">{h.timestamp}</p>
                  </div>
                  <div className="flex gap-2">
                    {h.risk_score !== undefined && <span className="text-[10px] bg-purple-500/20 text-purple-400 px-2 py-0.5 rounded font-bold">Risk: {h.risk_score.toFixed?.(1) ?? h.risk_score}%</span>}
                    {h.execution_risk !== undefined && <span className="text-[10px] bg-red-500/20 text-red-400 px-2 py-0.5 rounded font-bold">Exec: {h.execution_risk}%</span>}
                    {h.overall_health !== undefined && <span className="text-[10px] bg-green-500/20 text-green-400 px-2 py-0.5 rounded font-bold">Health: {h.overall_health}%</span>}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center text-slate-500 py-10">
            <ShieldAlert size={32} className="mx-auto mb-2 opacity-20" />
            <p className="text-xs">No risk events logged yet for this project.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default RiskHistoryPage;
