import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, FileText, Share2, MessageSquare, BarChart, Activity, Network, Clock, HardHat, BookOpen, HelpCircle } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

import LandingPage from './pages/LandingPage';
import AnalyzerPage from './pages/AnalyzerPage';
import DashboardPage from './pages/DashboardPage';
import KGPage from './pages/KGPage';
import RAGPage from './pages/RAGPage';
import ActionCenterPage from './pages/ActionCenterPage';
import DocumentationPage from './pages/DocumentationPage';
import QAPage from './pages/QAPage';
import ReportPage from './pages/ReportPage';
import ControlRoomPage from './pages/ControlRoomPage';
import RiskHistoryPage from './pages/RiskHistoryPage';
import { ProjectProvider, useProject } from './context/ProjectContext';

const NavIcon = ({ to, icon: Icon, label }: { to: string; icon: React.ElementType; label: string }) => {
  const location = useLocation();
  const isActive = location.pathname === to;
  return (
    <Link to={to} title={label}
      className={cn(
        "relative flex items-center justify-center w-9 h-9 rounded-lg transition-all duration-200 group",
        isActive ? "bg-primary/20 text-primary" : "text-slate-500 hover:text-white hover:bg-slate-800"
      )}
    >
      <Icon size={18} />
      <span className="absolute -bottom-7 left-1/2 -translate-x-1/2 text-[10px] font-medium whitespace-nowrap bg-slate-800 text-slate-300 px-2 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50">{label}</span>
    </Link>
  );
};

const Navbar = () => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 glass-card mx-3 mt-3 px-4 py-2.5 flex items-center justify-between">
      <Link to="/" className="flex items-center gap-2 shrink-0">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
          <Activity className="text-white" size={18} />
        </div>
        <div className="hidden sm:block">
          <h1 className="text-sm font-bold text-white leading-tight">ContractGraph<span className="text-primary">-RiskNet</span></h1>
          <p className="text-[8px] text-slate-500 uppercase tracking-widest">Infra AI Platform</p>
        </div>
      </Link>

      <div className="flex items-center gap-1">
        <NavIcon to="/analyzer" icon={FileText} label="Baseline" />
        <NavIcon to="/reports" icon={BarChart} label="DPR Upload" />
        <NavIcon to="/dashboard" icon={LayoutDashboard} label="Dashboard" />
        <NavIcon to="/control-room" icon={Network} label="Digital Twin" />
        <NavIcon to="/action-center" icon={HardHat} label="Recovery" />
        <NavIcon to="/risk-history" icon={Clock} label="Timeline" />
        <NavIcon to="/kg" icon={Share2} label="KG" />
        <NavIcon to="/rag" icon={MessageSquare} label="AI Expert" />
        <NavIcon to="/documentation" icon={BookOpen} label="Docs" />
        <NavIcon to="/qa" icon={HelpCircle} label="Q&A" />
      </div>

      <div className="flex items-center gap-2 shrink-0">
        <ProjectSelector />
      </div>
    </nav>
  );
};

const ProjectSelector = () => {
  const { projects, activeProject, setActiveProject, loading, profileLoading } = useProject();
  if (loading) return <span className="text-xs text-slate-500">Loading...</span>;
  if (!projects.length) return <span className="text-xs text-slate-500">No projects</span>;
  return (
    <div className="flex items-center gap-2">
      {profileLoading && <div className="w-3 h-3 border-2 border-primary border-t-transparent rounded-full animate-spin" />}
      <select
        className="bg-slate-800 border border-slate-700 text-white text-xs rounded-lg px-2 py-1.5 focus:ring-1 focus:ring-primary outline-none max-w-[180px]"
        value={activeProject?.id || ''}
        onChange={(e) => {
          const p = projects.find(p => p.id === e.target.value);
          if (p) setActiveProject(p);
        }}
      >
        {projects.map(p => (
          <option key={p.id} value={p.id}>{p.name}</option>
        ))}
      </select>
    </div>
  );
};

function AppContent() {
  return (
    <Router>
      <div className="min-h-screen bg-background relative selection:bg-primary/30">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/20 rounded-full blur-[120px] pointer-events-none" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-secondary/20 rounded-full blur-[120px] pointer-events-none" />
        <Navbar />
        <main className="pt-20 px-4 pb-12 max-w-7xl mx-auto relative z-10">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/analyzer" element={<AnalyzerPage />} />
            <Route path="/kg" element={<KGPage />} />
            <Route path="/rag" element={<RAGPage />} />
            <Route path="/reports" element={<ReportPage />} />
            <Route path="/action-center" element={<ActionCenterPage />} />
            <Route path="/control-room" element={<ControlRoomPage />} />
            <Route path="/risk-history" element={<RiskHistoryPage />} />
            <Route path="/documentation" element={<DocumentationPage />} />
            <Route path="/qa" element={<QAPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

function App() {
  return (
    <ProjectProvider>
      <AppContent />
    </ProjectProvider>
  );
}

export default App;
