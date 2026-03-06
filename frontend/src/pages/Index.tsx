import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Globe, Sparkles } from "lucide-react";
import TranslationForm from "@/components/TranslationForm";
import AnalysisResults, { type AnalysisResult } from "@/components/AnalysisResults";
import { analyzeTranslation } from "@/lib/analysisApi";

const Index = () => {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (data: {
    originalText: string;
    translatedText: string;
    brandTone: string;
    sourceLanguage: string;
    targetLanguage: string;
  }) => {
    setIsLoading(true);
    setResult(null);
    try {
      const res = await analyzeTranslation(data);
      setResult(res);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-primary flex items-center justify-center">
              <Globe className="w-5 h-5 text-primary-foreground" />
            </div>
            <div>
              <span className="font-display font-bold text-foreground text-lg tracking-tight">BrandLinguist</span>
              <span className="text-muted-foreground text-xs ml-2 font-body hidden sm:inline">by Datawords</span>
            </div>
          </div>
          <div className="flex items-center gap-1.5 text-xs text-muted-foreground font-body">
            <Sparkles className="w-3.5 h-3.5 text-accent" />
            AI-Powered
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="max-w-6xl mx-auto px-6 pt-16 pb-10 text-center">
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl md:text-5xl font-display font-bold text-foreground tracking-tight"
        >
          Translation Quality
          <br />
          <span className="text-accent">&amp; Brand Voice</span> Checker
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
          className="mt-4 text-muted-foreground max-w-xl mx-auto text-lg font-body"
        >
          Analyze your marketing translations for accuracy, cultural relevance and brand tone alignment — instantly.
        </motion.p>
      </section>

      {/* Main content */}
      <main className="max-w-6xl mx-auto px-6 pb-20">
        <div className="grid lg:grid-cols-2 gap-10 items-start">
          {/* Left: Form */}
          <div className="bg-card rounded-2xl border border-border p-6 md:p-8 shadow-sm">
            <TranslationForm onSubmit={handleSubmit} isLoading={isLoading} />
          </div>

          {/* Right: Results */}
          <div className="bg-card rounded-2xl border border-border p-6 md:p-8 shadow-sm min-h-[400px]">
            <AnimatePresence mode="wait">
              {isLoading ? (
                <motion.div
                  key="loading"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="flex flex-col items-center justify-center h-full min-h-[350px] gap-4"
                >
                  <div className="w-12 h-12 rounded-full border-2 border-accent border-t-transparent animate-spin" />
                  <p className="text-muted-foreground font-body text-sm">Analyzing translation quality...</p>
                </motion.div>
              ) : result ? (
                <motion.div key="result">
                  <AnalysisResults result={result} />
                </motion.div>
              ) : (
                <motion.div
                  key="empty"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex flex-col items-center justify-center h-full min-h-[350px] text-center gap-4"
                >
                  <div className="w-16 h-16 rounded-2xl bg-muted flex items-center justify-center">
                    <Globe className="w-8 h-8 text-muted-foreground" />
                  </div>
                  <div>
                    <p className="text-foreground font-display font-semibold">No analysis yet</p>
                    <p className="text-muted-foreground text-sm font-body mt-1">
                      Enter your texts and click <strong>Analyze</strong> to see results
                    </p>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
