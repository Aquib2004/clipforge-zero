export interface Project {
  id: string;
  name: string;
  source_title: string | null;
  source_creator: string | null;
  source_url: string | null;
  language: string;
  status: string;
  output_location: string | null;
  created_at: string;
  updated_at: string;
}

export interface HealthResponse {
  status: string;
  version: string;
}

export interface DiagnosticsResponse {
  status: string;
  disk: { total_bytes: number; used_bytes: number; free_bytes: number };
  memory: { total_bytes: number; available_bytes: number; percent: number };
  cpu_percent: number;
  ffmpeg_available: boolean;
  whisper_available: boolean;
  ollama_available: boolean;
}