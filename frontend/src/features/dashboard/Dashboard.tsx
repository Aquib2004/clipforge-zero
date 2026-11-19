import { useEffect, useState } from "react";
import { api } from "../../services/api";
import { HealthResponse, DiagnosticsResponse, Project } from "../../types";
import { AlertTriangle, CheckCircle, Database, HardDrive, Monitor, Clock } from "lucide-react";

function StatCard({ title, value, icon: Icon, label }: { title: string; value: string | number; icon: any; label?: string }) {
  return (
    <div className="slate-card p-6 rounded-xl border slate-border">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm slate-text-dim">{title}</p>
          <p className="text-2xl font-semibold mt-1">{value}</p>
          {label && <p className="text-xs slate-text-muted mt-1">{label}</p>}
        </div>
        <Icon className="w-8 h-8 text-slate-500" />
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [diag, setDiag] = useState<DiagnosticsResponse | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    Promise.all([
      api.getHealth().catch(() => null),
      api.getDiagnostics().catch(() => null),
      api.listProjects().catch((): Project[] => []),
    ])
      .then(([h, d, p]) => {
        if (!cancelled) {
          setHealth(h ?? null);
          setDiag(d ?? null);
          setProjects(p);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err.message);
          setLoading(false);
        }
      });
    return () => { cancelled = true; };
  }, []);

  if (loading) {
    return (
      <div className="slate-card p-12 rounded-xl border slate-border text-center">
        <span className="text-slate-500">Loading dashboard…</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="slate-card p-6 rounded-xl border border-red-500/30 bg-red-500/5">
        <AlertTriangle className="w-5 h-5 text-red-500 mr-2" />
        <span className="text-sm text-red-400">Failed to load dashboard: {error}</span>
      </div>
    );
  }

  const freeGB = diag ? ((diag.disk.free_bytes / 1024 / 1024 / 1024) / 1).toFixed(1) : "—";
  const memPct = diag ? diag.memory.percent : 0;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <p className="text-slate-400">Your ClipForge Zero workspace</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          title="Server"
          value={health?.status === "ok" ? "Online" : "Offline"}
          icon={Monitor}
          label={health?.status === "ok" ? "All systems operational" : "Backend unreachable"}
        />
        <StatCard
          title="Projects"
          value={projects.length}
          icon={Database}
          label={projects.length === 0 ? "No projects yet — create one to get started" : `${projects.length} project${projects.length === 1 ? "" : "s"} in workspace`}
        />
        <StatCard
          title="Disk Free"
          value={freeGB}
          icon={HardDrive}
          label="GB available on workspace drive"
        />
        <StatCard
          title="Memory"
          value={`${memPct}%`}
          icon={Clock}
          label="System memory in use"
        />
      </div>

      <div className="slate-card p-6 rounded-xl border slate-border">
        <h2 className="text-lg font-semibold mb-4">System Diagnostics</h2>
        {diag ? (
          <div className="space-y-3 text-sm">
            <div className="flex justify-between">
              <span className="slate-text-dim">FFmpeg</span>
              <span className={diag.ffmpeg_available ? "text-emerald-500" : "text-slate-400"}>
                {diag.ffmpeg_available ? <CheckCircle className="w-4 h-4 mr-2" /> : <AlertTriangle className="w-4 h-4 mr-2" />}Not installed
              </span>
            </div>
            <div className="flex justify-between">
              <span className="slate-text-dim">Whisper</span>
              <span className={diag.whisper_available ? "text-emerald-500" : "text-slate-400"}>
                {diag.whisper_available ? <CheckCircle className="w-4 h-4 mr-2" /> : <AlertTriangle className="w-4 h-4 mr-2" />}Not installed
              </span>
            </div>
            <div className="flex justify-between">
              <span className="slate-text-dim">Ollama</span>
              <span className={diag.ollama_available ? "text-emerald-500" : "text-slate-400"}>
                {diag.ollama_available ? <CheckCircle className="w-4 h-4 mr-2" /> : <AlertTriangle className="w-4 h-4 mr-2" />}Not running
              </span>
            </div>
          </div>
        ) : (
          <p className="text-slate-500">Diagnostics unavailable</p>
        )}
      </div>

      <div className="slate-card p-6 rounded-xl border slate-border">
        <h2 className="text-lg font-semibold mb-4">Recent Projects</h2>
        {projects.length === 0 ? (
          <p className="text-slate-400 text-sm">No projects yet. Create your first project to begin.</p>
        ) : (
          <div className="space-y-3">
            {projects.map((p) => (
              <div key={p.id} className="flex items-center justify-between p-3 rounded-lg bg-slate-900/50 border border-slate-800/50">
                <div>
                  <p className="font-medium">{p.name}</p>
                  <p className="text-xs slate-text-dim">{p.source_title || "No title"} · {p.language}</p>
                </div>
                <span className="px-2 py-1 rounded text-xs border border-slate-700 text-slate-300 bg-slate-800/50">
                  {p.status}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}