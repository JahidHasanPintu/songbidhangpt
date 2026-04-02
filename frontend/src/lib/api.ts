import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: `${API_BASE}/api/v1`,
  headers: { "Content-Type": "application/json" },
});

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  sources?: SourceDocument[];
  language?: string;
}

export interface SourceDocument {
  content: string;
  source: string;
  page?: number;
  article?: string;
}

export interface ChatRequest {
  question: string;
  language: "bn" | "en" | "auto";
  chat_history?: { role: string; content: string }[];
}

export interface ChatResponse {
  answer: string;
  sources: SourceDocument[];
  language_detected: string;
  question: string;
}

export async function sendMessage(req: ChatRequest): Promise<ChatResponse> {
  const { data } = await api.post<ChatResponse>("/chat", req);
  return data;
}

export async function getHealth() {
  const { data } = await api.get("/health".replace("/api/v1", ""), {
    baseURL: API_BASE,
  });
  return data;
}