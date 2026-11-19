import { Routes, Route, NavLink, useLocation } from "react-router-dom";
import { Layout, MoreHorizontal, Settings, Play, RefreshCw } from "lucide-react";
import Dashboard from "./features/dashboard/Dashboard";
import Projects from "./features/projects/Projects";
import SettingsPage from "./features/settings/Settings";

const NAV = [
  { href: "/", label: "Home", icon: Play },
  { href: "/projects", label: "Projects", icon: Layout },
  { href: "/create", label: "Create", icon: RefreshCw, disabled: true },
  { href: "/clips", label: "Clip Library", icon: Play, disabled: true },
  { href: "/render", label: "Render Queue", icon: RefreshCw, disabled: true },
  { href: "/publishing", label: "Publishing", icon: MoreHorizontal, disabled: true },
  { href: "/settings", label: "Settings", icon: Settings },
];

function ActiveNavLink({ href, label, icon: Icon, disabled }: { href: string; label: string; icon: any; disabled?: boolean }) => {
  const location = useLocation();
  const isActive = location.pathname === href;
  return (
    <NavLink
      to={href}
      className={({ isActive: active }) =>
        `flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${
          disabled
            ? "text-slate-400"
            : active
              ? "bg-slate-800 text-slate-100"
              : "text-slate-300 hover:bg-slate-800/50 hover:text-slate-100"
        }`
      }
      disabled={disabled}
    >
      <Icon size={18} />
      {label}
    </NavLink>
  );
}

export default function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <nav className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
        <div className="flex items-center gap-4 px-6 py-4">
          <span className="font-bold text-xl tracking-tight">ClipForge Zero</span>
          <div className="ml-auto flex items-center gap-2">
            <span className="text-xs text-slate-500">v0.1.0</span>
            <span className="w-2 h-2 rounded-full bg-emerald-500" title="Local server running" />
          </div>
        </div>
        <div className="px-6 space-y-1">
          {NAV.map((item) => (
            <ActiveNavLink key={item.href} {...item} />
          ))}
        </div>
      </nav>
      <main className="max-w-6xl mx-auto px-6 py-8">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </main>
    </div>
  );
}