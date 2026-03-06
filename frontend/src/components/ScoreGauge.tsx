import { motion } from "framer-motion";

interface ScoreGaugeProps {
  score: number;
  label?: string;
}

const getScoreColor = (score: number) => {
  if (score >= 85) return "text-success";
  if (score >= 70) return "text-score-good";
  if (score >= 50) return "text-score-fair";
  return "text-score-poor";
};

const getScoreLabel = (score: number) => {
  if (score >= 85) return "Excellent";
  if (score >= 70) return "Good";
  if (score >= 50) return "Needs Work";
  return "Poor";
};

const ScoreGauge = ({ score, label }: ScoreGaugeProps) => {
  const circumference = 2 * Math.PI * 54;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="relative w-36 h-36">
        <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
          <circle
            cx="60" cy="60" r="54"
            fill="none"
            stroke="hsl(var(--muted))"
            strokeWidth="8"
          />
          <motion.circle
            cx="60" cy="60" r="54"
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1.2, ease: "easeOut", delay: 0.3 }}
            className={getScoreColor(score)}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.span
            className={`text-3xl font-display font-bold ${getScoreColor(score)}`}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            {score}
          </motion.span>
          <span className="text-xs text-muted-foreground font-body">/ 100</span>
        </div>
      </div>
      <span className={`text-sm font-semibold font-body ${getScoreColor(score)}`}>
        {label || getScoreLabel(score)}
      </span>
    </div>
  );
};

export default ScoreGauge;
