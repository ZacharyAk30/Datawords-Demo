import type { AnalysisResult } from "@/components/AnalysisResults";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:5001";

export interface AnalyzeRequest {
  originalText: string;
  translatedText: string;
  brandTone: string;
  sourceLanguage: string;
  targetLanguage: string;
}

/** Réponse brute du backend (alignée sur schemas.AnalysisResult) */
interface BackendAnalysisResult {
  score: number;
  issues: string[];
  suggested_translation: string;
}

function mapBackendToFrontend(backend: BackendAnalysisResult): AnalysisResult {
  return {
    score: backend.score,
    issues: backend.issues ?? [],
    suggestedTranslation: backend.suggested_translation ?? "",
  };
}

export async function analyzeTranslation(data: AnalyzeRequest): Promise<AnalysisResult> {
  const res = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      originalText: data.originalText,
      translatedText: data.translatedText,
      brandTone: data.brandTone,
      sourceLanguage: data.sourceLanguage,
      targetLanguage: data.targetLanguage,
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    const message = err?.error ?? err?.details ?? res.statusText;
    throw new Error(typeof message === "string" ? message : JSON.stringify(message));
  }

  const raw: BackendAnalysisResult = await res.json();
  return mapBackendToFrontend(raw);
}
