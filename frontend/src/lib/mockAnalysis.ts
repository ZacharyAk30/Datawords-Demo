import type { AnalysisResult } from "@/components/AnalysisResults";

// Mock analysis — will be replaced by real AI backend
export async function analyzeTranslation(data: {
  originalText: string;
  translatedText: string;
  brandTone: string;
  sourceLanguage: string;
  targetLanguage: string;
}): Promise<AnalysisResult> {
  // Simulate network delay
  await new Promise(r => setTimeout(r, 2000));

  // Demo result for the example input (format backend: score, issues string[], suggested_translation)
  if (data.originalText.toLowerCase().includes("wild side")) {
    return {
      score: 68,
      issues: [
        'The expression "côté sauvage" feels too aggressive for a luxury fragrance brand. It lacks the refined sophistication expected in high-end beauty marketing.',
        "Luxury fragrance marketing in France typically uses more poetic, evocative language. A literal translation misses the aspirational quality of the original.",
        '"Libérez" (unleash/free) carries a slightly confrontational tone. Consider softer alternatives like "Révélez" (reveal) that better align with luxury positioning.',
      ],
      suggestedTranslation: "Révélez votre élégance naturelle avec notre nouveau parfum d'exception.",
    };
  }

  // Generic response for other inputs
  const score = Math.min(95, Math.max(40, 75 + Math.floor(Math.random() * 20) - 10));

  return {
    score,
    issues: [
      `The translation's register may not fully align with the "${data.brandTone}" brand positioning. Consider adjusting vocabulary choices.`,
      "Some phrases could be more compelling in the target market. The translation is accurate but lacks the persuasive edge of the original.",
    ],
    suggestedTranslation: data.translatedText + " [AI-improved version would appear here with real backend]",
  };
}
