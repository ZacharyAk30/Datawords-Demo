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
    <div className="min-h-screen md:h-screen flex flex-col bg-background md:overflow-hidden">
      {/* Header */}
      <header className="shrink-0 border-b border-border bg-card/80 backdrop-blur-sm z-10">
        <div className="max-w-6xl mx-auto px-4 md:px-6 h-14 md:h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 md:w-9 md:h-9 rounded-lg bg-primary flex items-center justify-center">
              <Globe className="w-4 h-4 md:w-5 md:h-5 text-primary-foreground" />
            </div>
            <div>
              <span className="font-display font-bold text-foreground text-base md:text-lg tracking-tight">BrandLinguist</span>
              <span className="text-muted-foreground text-xs ml-2 font-body hidden sm:inline">by Datawords</span>
            </div>
          </div>
          <div className="flex items-center gap-1.5 text-xs text-muted-foreground font-body">
            <Sparkles className="w-3.5 h-3.5 text-accent" />
            AI-Powered
          </div>
        </div>
      </header>

      {/* Hero — compact sur desktop pour tenir dans la page */}
      <section className="shrink-0 max-w-6xl mx-auto px-4 md:px-6 pt-4 md:pt-6 pb-3 md:pb-4 text-center">
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-2xl sm:text-3xl md:text-4xl lg:text-[2.25rem] font-display font-bold text-foreground tracking-tight leading-tight"
        >
          Translation Quality
          <br />
          <span className="text-accent">&amp; Brand Voice</span> Checker
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
          className="mt-2 md:mt-3 text-muted-foreground max-w-xl mx-auto text-sm md:text-base font-body"
        >
          Analyze your marketing translations for accuracy, cultural relevance and brand tone alignment — instantly.
        </motion.p>
      </section>

      {/* Main content — prend le reste, scroll interne sur desktop */}
      <main className="flex-1 min-h-0 max-w-6xl mx-auto w-full px-4 md:px-6 pb-4 md:pb-6 overflow-hidden">
        <div className="grid lg:grid-cols-2 gap-4 md:gap-6 md:h-full min-h-0 items-stretch">
          {/* Left: Form — scroll interne uniquement sur desktop (pas de scroll page) */}
          <div className="bg-card rounded-2xl border border-border p-4 md:p-6 shadow-sm min-h-0 flex flex-col md:overflow-hidden">
            <div className="min-h-0 md:overflow-y-auto md:overflow-x-hidden">
              <TranslationForm onSubmit={handleSubmit} isLoading={isLoading} />
            </div>
          </div>

          {/* Right: Results — scroll interne uniquement sur desktop */}
          <div className="bg-card rounded-2xl border border-border p-4 md:p-6 shadow-sm min-h-[280px] md:min-h-0 flex flex-col md:overflow-hidden">
            <div className="min-h-0 md:overflow-y-auto md:overflow-x-hidden flex-1">
              <AnimatePresence mode="wait">
                {isLoading ? (
                  <motion.div
                    key="loading"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="flex flex-col items-center justify-center min-h-[260px] md:min-h-[200px] gap-4 py-6"
                  >
                    <div className="w-12 h-12 rounded-full border-2 border-accent border-t-transparent animate-spin" />
                    <p className="text-muted-foreground font-body text-sm">Analyzing translation quality...</p>
                  </motion.div>
                ) : result ? (
                  <motion.div key="result" className="pb-4">
                    <AnalysisResults result={result} />
                  </motion.div>
                ) : (
                  <motion.div
                    key="empty"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="flex flex-col items-center justify-center min-h-[260px] md:min-h-[200px] text-center gap-4 py-6"
                  >
                    <div className="w-14 h-14 md:w-16 md:h-16 rounded-2xl bg-muted flex items-center justify-center">
                      <Globe className="w-7 h-7 md:w-8 md:h-8 text-muted-foreground" />
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
        </div>
      </main>
    </div>
  );
};

export default Index;
