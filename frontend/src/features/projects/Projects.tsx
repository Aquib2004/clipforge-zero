import { useEffect, useState, FormEvent } from "react";
import { api } from "../../services/api";
import { Project } from "../../types";
import { Plus, Trash2, AlertCircle } from "lucide-react";

export default function Projects() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [creating, setCreating] = useState(false);
  const [name, setName] = useState("");
  const [sourceTitle, setSourceTitle] = useState("");
  const [sourceUrl, setSourceUrl] = useState("");

  useEffect(() => {
    api.listProjects().then(setProjects).catch((err) => setError(err.message)).finally(() => setLoading(false));
  }, []);

  const handleCreate = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const created = await api.createProject({ name, source_title: sourceTitle || undefined, source_url: sourceUrl || undefined });
      setProjects((prev) => [created, ...prev]);
      setName(""); setSourceTitle(""); setSourceUrl(""); setCreating(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create project");
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm("Delete this project? This cannot be undone.")) return;
    try {
      await api.deleteProject(id);
      setProjects((prev) => prev.filter((p) => p.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete project");
    }
  };

  if (loading) return <div className="slate-card p-12 rounded-xl border slate-border text-center"><span className="text-slate-500">Loading projects…</span></div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Projects</h1>
          <p className="text-slate-400">Manage your video projects</p>
        </div>
        <button onClick={() => setCreating(!creating)} className="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-800 text-slate-200 hover:bg-slate-700 border border-slate-700 transition-colors">
          <Plus size={16} /> {creating ? "Cancel" : "New Project"}
        </button>
      </div>

      {error && <div className="slate-card p-4 rounded-xl border border-red-500/30 bg-red-500/5"><AlertCircle className="w-5 h-5 text-red-500 mr-2" /><span className="text-sm text-red-400">{error}</span></div>}

      {creating && (
        <div className="slate-card p-6 rounded-xl border slate-border space-y-4">
          <form onSubmit={handleCreate} className="space-y-4">
            <div><label className="block text-xs font-medium text-slate-300 mb-1">Project name</label><input className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-slate-100 focus:border-emerald-500 focus:outline-none" value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. Podcast Interview #42" required /></div>
            <div><label className="block text-xs font-medium text-slate-300 mb-1">Source title (optional)</label><input className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-slate-100 focus:border-emerald-500 focus:outline-none" value={sourceTitle} onChange={(e) => setSourceTitle(e.target.value)} placeholder="Video title" /></div>
            <div><label className="block text-xs font-medium text-slate-300 mb-1">Source URL (optional)</label><input className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-slate-100 focus:border-emerald-500 focus:outline-none" value={sourceUrl} onChange={(e) => setSourceUrl(e.target.value)} placeholder="https://youtube.com/watch?v=..." /></div>
            <div className="flex justify-end gap-2">
              <button type="button" onClick={() => setCreating(false)} className="px-4 py-2 rounded-lg bg-transparent text-slate-400 hover:text-slate-200">Cancel</button>
              <button type="submit" disabled={!name} className="px-4 py-2 rounded-lg bg-emerald-600 text-white hover:bg-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">Create Project</button>
            </div>
          </form>
        </div>
      )}

      <div className="slate-card rounded-xl border slate-border overflow-hidden">
        {projects.length === 0 ? <div className="p-12 text-center"><p className="text-slate-400">No projects yet.</p></div> : (
          <table className="w-full text-left"><thead><tr className="border-b border-slate-800"><th className="px-6 py-3 text-xs font-semibold text-slate-400 uppercase">Name</th><th className="px-6 py-3 text-xs font-semibold text-slate-400 uppercase">Source</th><th className="px-6 py-3 text-xs font-semibold text-slate-400 uppercase">Status</th><th className="px-6 py-3 text-xs font-semibold text-slate-400 uppercase">Actions</th></tr></thead><tbody className="divide-y divide-slate-800">{projects.map((p) => (
            <tr key={p.id} className="hover:bg-slate-800/30 transition-colors"><td className="px-6 py-4"><p className="font-medium">{p.name}</p><p className="text-xs slate-text-dim">{p.source_title || "—"}</p></td><td className="px-6 py-4"><p className="text-xs text-slate-300">{p.source_url || "Local file"}</p></td><td className="px-6 py-4"><span className="px-2 py-1 rounded text-xs border border-slate-700 text-slate-300 bg-slate-800/50">{p.status}</span></td><td className="px-6 py-4"><button onClick={() => handleDelete(p.id)} className="text-slate-400 hover:text-red-400" title="Delete"><Trash2 size={16} /></button></td></tr>
          ))}</tbody></table>
        )}
      </div>
    </div>
  );
}