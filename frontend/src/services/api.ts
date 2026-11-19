const API_BASE = import.meta.env.VITE_API_BASE || "/api";

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error || `Request failed with status ${res.status}`);
  }
  return res.json();
}

export const api = {
  getHealth: () => request<HealthResponse>("/system/health"),
  getDiagnostics: () => request<DiagnosticsResponse>("/system/diagnostics"),
  listProjects: () => request<Project[]>("/projects"),
  createProject: (body: Partial<Project>) => request<Project>("/projects", {
    method: "POST",
    body: JSON.stringify(body),
  }),
  getProject: (id: string) => request<Project>(`/projects/${id}`),
  updateProject: (id: string, body: Partial<Project>) => request<Project>(`/projects/${id}`, {
    method: "PATCH",
    body: JSON.stringify(body),
  }),
  deleteProject: (id: string) => request<void>(`/projects/${id}`, { method: "DELETE" }),
};