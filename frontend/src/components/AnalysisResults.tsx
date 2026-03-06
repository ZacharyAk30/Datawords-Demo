import { motion } from "framer-motion";
import { Sparkles, Copy, Check } from "lucide-react";
import { useState } from "react";
import ScoreGauge from "./ScoreGauge";
import IssueCard from "./IssueCard";

/** Aligné sur le schéma backend (schemas.AnalysisResult) */
export interface AnalysisResult {
  score: number;
  issues: string[];
  suggestedTranslation: string;
}

interface AnalysisResultsProps {
  result: AnalysisResult;
}

const AnalysisResults = ({ result }: AnalysisResultsProps) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(result.suggestedTranslation);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-5 md:space-y-6 overflow-x-hidden break-words"
    >
      {/* Score */}
      <div className="flex flex-col items-center py-3 md:py-4">
        <h3 className="text-base md:text-lg font-display font-semibold text-foreground mb-3 md:mb-4">Translation Quality Score</h3>
        <ScoreGauge score={result.score} />
      </div>

      {/* Issues */}
      {result.issues.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-lg font-display font-semibold text-foreground">Issues Detected</h3>
          <div className="space-y-3">
            {result.issues.map((issue, i) => (
              <IssueCard key={i} index={i} title="Issue" description={issue} severity="medium" />
            ))}
          </div>
        </div>
      )}

      {/* Suggested Translation */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
        className="space-y-3"
      >
        <div className="flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-accent" />
          <h3 className="text-lg font-display font-semibold text-foreground">Suggested Translation</h3>
        </div>
        <div className="relative rounded-lg border border-accent/30 bg-accent/5 p-4 md:p-5">
          <p className="text-foreground leading-relaxed pr-10 italic font-display text-base md:text-lg break-words">
            "{result.suggestedTranslation}"
          </p>
          <button
            onClick={handleCopy}
            className="absolute top-4 right-4 p-2 rounded-md hover:bg-accent/10 transition-colors text-muted-foreground hover:text-foreground"
          >
            {copied ? <Check className="w-4 h-4 text-success" /> : <Copy className="w-4 h-4" />}
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default AnalysisResults;
