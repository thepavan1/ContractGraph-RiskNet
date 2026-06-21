import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import type { ReactNode } from 'react';
import api from '../api';

export interface Project {
  id: string;
  name: string;
  status: string;
  category: string;
}

export interface CompleteProfile {
  project: Project;
  baseline: any;
  dpr_reports: any[];
  risk: any;
  deviations: any;
  recovery: any;
  charts: any;
  risk_chain: any[];
  timeline: any[];
  risk_history: any[];
}

interface ProjectContextType {
  projects: Project[];
  activeProject: Project | null;
  setActiveProject: (project: Project) => void;
  profile: CompleteProfile | null;
  profileLoading: boolean;
  refreshProfile: () => void;
  loading: boolean;
}

const ProjectContext = createContext<ProjectContextType | undefined>(undefined);

export const ProjectProvider = ({ children }: { children: ReactNode }) => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [activeProject, setActiveProject] = useState<Project | null>(null);
  const [profile, setProfile] = useState<CompleteProfile | null>(null);
  const [profileLoading, setProfileLoading] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/projects').then(res => {
      setProjects(res.data);
      if (res.data.length > 0) setActiveProject(res.data[0]);
    }).catch(console.error).finally(() => setLoading(false));
  }, []);

  const fetchProfile = useCallback(async (projectId: string) => {
    setProfileLoading(true);
    try {
      const res = await api.get(`/projects/${projectId}/complete-profile`);
      setProfile(res.data);
    } catch (err) {
      console.error("Failed to load profile", err);
      setProfile(null);
    } finally {
      setProfileLoading(false);
    }
  }, []);

  useEffect(() => {
    if (activeProject) {
      fetchProfile(activeProject.id);
    }
  }, [activeProject, fetchProfile]);

  const refreshProfile = useCallback(() => {
    if (activeProject) fetchProfile(activeProject.id);
  }, [activeProject, fetchProfile]);

  return (
    <ProjectContext.Provider value={{ projects, activeProject, setActiveProject, profile, profileLoading, refreshProfile, loading }}>
      {children}
    </ProjectContext.Provider>
  );
};

export const useProject = () => {
  const ctx = useContext(ProjectContext);
  if (!ctx) throw new Error('useProject must be within ProjectProvider');
  return ctx;
};
