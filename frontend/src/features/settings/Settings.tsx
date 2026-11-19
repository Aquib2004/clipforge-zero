import { useEffect, useState } from "react";
import { api } from "../../services/api";
import { DiagnosticsResponse } from "../../types";
import { AlertTriangle, CheckCircle, Cpu, HardDrive, Shield, Wifi } from "lucide-react";

export default function SettingsPage() {
  const [diag, setDiag] = useState<DiagnosticsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.getDiagnostics()
      .then(setDiag)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Settings</h1>
        <p className="text-slate-400">Application configuration and diagnostics</p>
      </div>

      <div className="slate-card p-6 rounded-xl border slate-border">
        <h2 className="text-lg font-semibold mb-4">System Status</h2>
        {loading ? (
          <p className="text-slate-400">Loading diagnostics…</p>
        ) : error ? (
          <div className="flex items-center gap-2 p-3 rounded-lg bg-red-500/10 border border-red-500/30">
            <AlertTriangle className="w-5 h-5 text-red-500" />
            <span className="text-sm text-red-400">Failed to load diagnostics: {error}</span>
          </div>
        ) : diag ? (
          <div className="space-y-4">
            <div className="flex items-center gap-3 p-3 rounded-lg bg-slate-900/50 border border-slate-700/50">
              <Cpu className="w-5 h-5 text-slate-400" />
              <div>
                <p className="text-sm font-medium">CPU usage</p>
                <p className="text-xs slate-text-dim">{diag.cpu_percent.toFixed(1)}%</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 rounded-lg bg-slate-900/50 border border-slate-700/50">
              <HardDrive className="w-5 h-5 text-slate-400" />
              <div>
                <p className="text-sm font-medium">Memory</p>
                <p className="text-xs slate-text-dim">{diag.memory.percent.toFixed(1)}% used</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 rounded-lg bg-slate-900/50 border border-slate-700/50">
              <HardDrive className="w-5 h-5 text-slate-400" />
              <div>
                <p className="text-sm font-medium">Disk free</p>
                <p className="text-xs slate-text-dim">
                  {((diag.disk.free_bytes / 1024 / 1024 / 1024) / 1).toFixed(1)} GB
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 rounded-lg bg-slate-900/50 border border-slate-700/50">
              <Shield className="w-5 h-5 text-slate-400" />
              <div>
                <p className="text-sm font-medium">Server binding</p>
                <p className="text-xs slate-text-dim">127.0.0.1 (localhost only)</p>
              </div>
            </div>
          </div>
        ) : (
          <p className="text-slate-400">No diagnostics available</p>
        )}
      </div>

      <div className="slate-card p-6 rounded-xl border slate-border">
        <h2 className="text-lg font-semibold mb-4">AI Providers</h2>
        <p className="text-sm slate-text-dim mb-4">Configure BYOK credentials for AI moment detection.</p>
        <div className="space-y-3">
          {[
            { name: "Ollama (local)", status: "unavailable", icon: Wifi },
            { name: "Gemini API", status: "unavailable", icon: AlertTriangle },
            { name: "Groq API", status: "unavailable", icon: AlertTriangle },
          ].map((provider) => (
            <div key={provider.name} className="flex items-center justify-between p-3 rounded-lg bg-slate-900/50 border border-slate-700/50">
              <div className="flex items-center gap-3">
                {React.cloneElement(provider.icon, { size: 16, className: "text-slate-500" })}
                <span className="text-sm">{provider.name}</span>
              </div>
              <span className="px-2 py-1 rounded text-xs border border-slate-700 text-slate-400 bg-slate-800/50">
                Not configured
              </span>
            </div>
          ))}
          <p className="text-xs slate-text-dim mt-2">
            Credentials are stored securely in the OS keychain via the UI Vault (coming in Phase 4).
            AI is optional — core clipping works without any provider.
          </p>
        </div>
      </div>

      <div className="slate-card p-6 rounded-xl border slate-border">
        <h2 className="text-lg font-semibold mb-4">Processing Mode</h2>
        <p className="text-sm slate-text-dim mb-4">This machine is classed as low-resource (i3 CPU, integrated GPU).</p>
        <div className="p-3 rounded-lg bg-slate-900/50 border border-slate-700/50">
          <p className="text-sm font-medium">Current mode: <span className="text-emerald-400">Low Resource</span></p>
          <ul className="text-xs text-slate-400 mt-2 space-y-1 list-disc list-inside">
            <li>CPU-only transcription</li>
            <li>Quantized Whisper models (tiny/base)</li>
            <li>Sequential job processing</li>
            <li>Conservative memory usage</li>
          </ul>
        </div>
      </div>
    </div>
  );
}