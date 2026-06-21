import { useProject } from '../context/ProjectContext';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RTooltip, Legend, ResponsiveContainer, AreaChart, Area, PieChart, Pie, Cell } from 'recharts';
import { AlertTriangle, TrendingUp, IndianRupee, ShieldAlert, Loader2 } from 'lucide-react';

const DashboardPage = () => {
  const { activeProject, profile, profileLoading } = useProject();
  if (!activeProject) return <div className="text-white p-6">Select a project to continue.</div>;
  if (profileLoading || !profile) return <div className="text-white p-6 flex items-center gap-2"><Loader2 className="animate-spin text-primary" /> Loading...</div>;

  const d = profile.deviations;
  const ch = profile.charts;
  const health = d.overall_health_score ?? 100;
  const isHigh = health < 50;

  // Risk contribution from breakdown
  const riskPie = (profile.risk.risk_breakdown || []).map((r: any) => ({ name: r.name, value: r.score }));
  const COLORS = ['#3b82f6', '#ef4444', '#f59e0b', '#10b981', '#8b5cf6', '#06b6d4', '#ec4899', '#6366f1'];

  return (
    <div className="flex flex-col gap-5 mt-2">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-2xl font-bold text-white">Project Health Dashboard</h2>
          <p className="text-slate-400 text-sm mt-1"><strong className="text-white">{activeProject.name}</strong></p>
        </div>
        <div className="text-right">
          <span className="text-[10px] text-slate-500 uppercase tracking-widest font-bold">Overall Health</span>
          <div className={`text-3xl font-black ${isHigh ? 'text-red-400' : 'text-accent'}`}>{health.toFixed(1)}%</div>
        </div>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-3">
        <KPI label="Contract Risk" value={`${profile.risk.probability}%`} color="purple" />
        <KPI label="Execution Risk" value={`${d.execution_risk_score ?? 0}%`} color="orange" />
        <KPI label="Current Phase" value={profile.baseline.milestones?.[0]?.name || "N/A"} color="blue" />
        <KPI label="Delay Days" value={`${d.estimated_delay_days ?? 0}`} color="red" />
        <KPI label="Cost Variance" value={`₹${d.cost_variance_crores ?? 0} Cr`} color="yellow" />
        <KPI label="LD Exposure" value={`₹${d.ld_penalty_exposure_crores ?? 0} Cr`} color="red" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* S-Curve */}
        <div className="glass-card p-5">
          <h3 className="text-sm font-bold text-white mb-3 flex items-center gap-2"><TrendingUp size={16} className="text-primary" /> S-Curve (Planned vs Actual)</h3>
          <div className="h-[260px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={ch.s_curve}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="month" stroke="#64748b" tick={{ fontSize: 10 }} />
                <YAxis stroke="#64748b" tick={{ fontSize: 10 }} />
                <RTooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', fontSize: 11 }} />
                <Legend wrapperStyle={{ fontSize: 10 }} />
                <Line type="monotone" dataKey="planned" name="Planned %" stroke="#3b82f6" strokeWidth={2} />
                <Line type="monotone" dataKey="actual" name="Actual %" stroke={isHigh ? '#ef4444' : '#10b981'} strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Cost */}
        <div className="glass-card p-5">
          <h3 className="text-sm font-bold text-white mb-3 flex items-center gap-2"><IndianRupee size={16} className="text-secondary" /> Cost Performance</h3>
          <div className="h-[260px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={ch.cost_curve}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="month" stroke="#64748b" tick={{ fontSize: 10 }} />
                <YAxis stroke="#64748b" tick={{ fontSize: 10 }} />
                <RTooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', fontSize: 11 }} />
                <Legend wrapperStyle={{ fontSize: 10 }} />
                <Bar dataKey="budget" name="Budget (Cr)" fill="#3b82f6" radius={[3, 3, 0, 0]} />
                <Bar dataKey="actual_spend" name="Spend (Cr)" fill="#f59e0b" radius={[3, 3, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Risk Evolution */}
        <div className="glass-card p-5">
          <h3 className="text-sm font-bold text-white mb-3 flex items-center gap-2"><ShieldAlert size={16} className="text-orange-400" /> Risk Evolution</h3>
          <div className="h-[260px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={ch.risk_evolution}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="month" stroke="#64748b" tick={{ fontSize: 10 }} />
                <YAxis stroke="#64748b" tick={{ fontSize: 10 }} />
                <RTooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', fontSize: 11 }} />
                <Legend wrapperStyle={{ fontSize: 10 }} />
                <Area type="monotone" dataKey="contractRisk" name="Contract Risk" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.3} />
                <Area type="monotone" dataKey="executionRisk" name="Execution Risk" stroke="#f43f5e" fill="#f43f5e" fillOpacity={0.4} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Risk Contribution Pie */}
        <div className="glass-card p-5">
          <h3 className="text-sm font-bold text-white mb-3 flex items-center gap-2"><AlertTriangle size={16} className="text-red-400" /> Risk Contribution</h3>
          <div className="h-[260px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={riskPie} cx="50%" cy="50%" innerRadius={50} outerRadius={90} paddingAngle={2} dataKey="value" label={({ name, value }: any) => `${name.split(' ')[0]} ${value}%`} labelLine={false}>
                  {riskPie.map((_: any, i: number) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <RTooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', fontSize: 11 }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Executive Summary */}
      <div className={`glass-card p-5 border-l-4 ${isHigh ? 'border-l-red-500 bg-red-500/5' : 'border-l-accent bg-accent/5'}`}>
        <h3 className="text-lg font-bold text-white mb-2">Executive Summary</h3>
        <p className="text-slate-300 text-sm leading-relaxed">
          {isHigh
            ? `CRITICAL: Project health at ${health.toFixed(1)}%. ${d.estimated_delay_days} day delay detected. LD clause exposure at ₹${d.ld_penalty_exposure_crores} Cr. Immediate recovery action required.`
            : `Project tracking within acceptable parameters. Health score ${health.toFixed(1)}%. Schedule and cost variances are within tolerance limits.`}
        </p>
      </div>
    </div>
  );
};

const KPI = ({ label, value, color }: { label: string; value: string; color: string }) => {
  const colors: Record<string, string> = { purple: 'border-b-purple-500', orange: 'border-b-orange-500', red: 'border-b-red-500', blue: 'border-b-blue-500', yellow: 'border-b-yellow-500', green: 'border-b-green-500' };
  return (
    <div className={`glass-card p-3 border-b-4 ${colors[color] || 'border-b-slate-500'}`}>
      <span className="text-[10px] text-slate-400 uppercase tracking-widest font-bold block">{label}</span>
      <span className="text-lg font-black text-white">{value}</span>
    </div>
  );
};

export default DashboardPage;
