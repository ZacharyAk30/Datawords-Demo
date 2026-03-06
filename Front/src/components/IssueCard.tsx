import { motion } from "framer-motion";
import { AlertTriangle, Info } from "lucide-react";

interface IssueCardProps {
  index: number;
  title: string;
  description: string;
  severity: "high" | "medium" | "low";
}

const severityConfig = {
  high: { icon: AlertTriangle, bg: "bg-destructive/10", border: "border-destructive/20", text: "text-destructive", label: "High" },
  medium: { icon: AlertTriangle, bg: "bg-warning/10", border: "border-warning/20", text: "text-warning", label: "Medium" },
  low: { icon: Info, bg: "bg-muted", border: "border-border", text: "text-muted-foreground", label: "Low" },
};

const IssueCard = ({ index, title, description, severity }: IssueCardProps) => {
  const config = severityConfig[severity];
  const Icon = config.icon;

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.6 + index * 0.15 }}
      className={`rounded-lg border p-4 ${config.bg} ${config.border}`}
    >
      <div className="flex items-start gap-3">
        <Icon className={`w-5 h-5 mt-0.5 shrink-0 ${config.text}`} />
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <h4 className="font-semibold text-sm text-foreground">{title}</h4>
            <span className={`text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full ${config.bg} ${config.text} border ${config.border}`}>
              {config.label}
            </span>
          </div>
          <p className="text-sm text-muted-foreground leading-relaxed">{description}</p>
        </div>
      </div>
    </motion.div>
  );
};

export default IssueCard;
