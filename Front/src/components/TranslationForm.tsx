import { useState } from "react";
import { motion } from "framer-motion";
import { Languages, ArrowRight, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

interface TranslationFormProps {
  onSubmit: (data: { originalText: string; translatedText: string; brandTone: string; sourceLanguage: string; targetLanguage: string }) => void;
  isLoading: boolean;
}

const BRAND_TONES = [
  "Luxury / Elegant",
  "Playful / Fun",
  "Corporate / Professional",
  "Bold / Edgy",
  "Minimalist / Clean",
  "Warm / Friendly",
  "Tech / Innovative",
];

const LANGUAGES = [
  "English", "French", "Spanish", "German", "Italian", "Portuguese",
  "Chinese", "Japanese", "Korean", "Arabic", "Dutch", "Russian",
];

const TranslationForm = ({ onSubmit, isLoading }: TranslationFormProps) => {
  const [originalText, setOriginalText] = useState("");
  const [translatedText, setTranslatedText] = useState("");
  const [brandTone, setBrandTone] = useState("");
  const [sourceLanguage, setSourceLanguage] = useState("English");
  const [targetLanguage, setTargetLanguage] = useState("French");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!originalText.trim() || !translatedText.trim() || !brandTone) return;
    onSubmit({ originalText, translatedText, brandTone, sourceLanguage, targetLanguage });
  };

  const loadExample = () => {
    setOriginalText("Unleash your wild side with our new luxury fragrance.");
    setTranslatedText("Libérez votre côté sauvage avec notre nouveau parfum de luxe.");
    setBrandTone("Luxury / Elegant");
    setSourceLanguage("English");
    setTargetLanguage("French");
  };

  const isValid = originalText.trim() && translatedText.trim() && brandTone;

  return (
    <motion.form
      onSubmit={handleSubmit}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      {/* Language selectors */}
      <div className="flex items-center gap-3">
        <div className="flex-1">
          <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-1.5 block">Source</label>
          <Select value={sourceLanguage} onValueChange={setSourceLanguage}>
            <SelectTrigger className="bg-card">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {LANGUAGES.map(l => <SelectItem key={l} value={l}>{l}</SelectItem>)}
            </SelectContent>
          </Select>
        </div>
        <ArrowRight className="w-4 h-4 text-muted-foreground mt-6 shrink-0" />
        <div className="flex-1">
          <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-1.5 block">Target</label>
          <Select value={targetLanguage} onValueChange={setTargetLanguage}>
            <SelectTrigger className="bg-card">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {LANGUAGES.map(l => <SelectItem key={l} value={l}>{l}</SelectItem>)}
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Original text */}
      <div>
        <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-1.5 block">
          Original Text
        </label>
        <Textarea
          value={originalText}
          onChange={e => setOriginalText(e.target.value)}
          placeholder="Enter the original marketing text..."
          className="min-h-[100px] bg-card resize-none"
        />
      </div>

      {/* Translated text */}
      <div>
        <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-1.5 block">
          Translation to Analyze
        </label>
        <Textarea
          value={translatedText}
          onChange={e => setTranslatedText(e.target.value)}
          placeholder="Enter the translation to evaluate..."
          className="min-h-[100px] bg-card resize-none"
        />
      </div>

      {/* Brand tone */}
      <div>
        <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-1.5 block">
          Brand Tone
        </label>
        <Select value={brandTone} onValueChange={setBrandTone}>
          <SelectTrigger className="bg-card">
            <SelectValue placeholder="Select brand tone..." />
          </SelectTrigger>
          <SelectContent>
            {BRAND_TONES.map(t => <SelectItem key={t} value={t}>{t}</SelectItem>)}
          </SelectContent>
        </Select>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-3 pt-2">
        <Button
          type="submit"
          disabled={!isValid || isLoading}
          className="flex-1 h-12 text-base font-semibold"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Analyzing...
            </>
          ) : (
            <>
              <Languages className="w-4 h-4 mr-2" />
              Analyze Translation
            </>
          )}
        </Button>
        <Button
          type="button"
          variant="outline"
          onClick={loadExample}
          className="h-12 text-sm"
        >
          Try Example
        </Button>
      </div>
    </motion.form>
  );
};

export default TranslationForm;
