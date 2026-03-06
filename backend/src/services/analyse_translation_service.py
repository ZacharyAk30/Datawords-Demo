from typing import Any, Dict

from ..schemas import AnalysisInput, AnalysisResult
from .ollama_service import OllamaService
from .parser_service import ParserService
from .prompt_service import PromptService


class TranslationAnalysisService:
    """
    Service principal d'analyse de traduction, orchestrant les différents
    services métiers (prompt, appel modèle, parsing).
    """

    def __init__(
        self,
        prompt_service: PromptService,
        ollama_service: OllamaService,
        parser_service: ParserService,
    ) -> None:
        self._prompt_service = prompt_service
        self._ollama_service = ollama_service
        self._parser_service = parser_service

    def validate_payload(self, payload: Dict[str, Any]) -> AnalysisInput:
        """
        Valide le payload JSON brut et renvoie un objet d'entrée structuré.
        Accepte snake_case (original_text) ou camelCase (originalText) pour le frontend.
        Lève ValueError avec un dictionnaire d'erreurs si nécessaire.
        """
        errors: Dict[str, str] = {}

        original = (payload.get("original_text") or payload.get("originalText") or "").strip()
        translated = (payload.get("translated_text") or payload.get("translatedText") or "").strip()
        brand_tone = (payload.get("brand_tone") or payload.get("brandTone") or "").strip()
        source_language = (payload.get("source_language") or payload.get("sourceLanguage") or "").strip()
        target_language = (payload.get("target_language") or payload.get("targetLanguage") or "").strip()

        if not original:
            errors["original_text"] = "Le texte original est obligatoire."
        if not translated:
            errors["translated_text"] = "La traduction est obligatoire."
        if not brand_tone:
            errors["brand_tone"] = "Le ton de marque est obligatoire."

        if errors:
            raise ValueError(errors)

        return AnalysisInput(
            original_text=original,
            translated_text=translated,
            brand_tone=brand_tone,
            source_language=source_language,
            target_language=target_language,
        )

    def analyze(self, data: AnalysisInput) -> AnalysisResult:
        """
        Orchestration en deux appels LLM :
        1) Analyse : score et liste des problèmes uniquement.
        2) Suggestion : génération d'une traduction suggérée à partir de l'analyse.
        """
        # Premier appel : analyse (score + issues uniquement)
        format_analysis = self._parser_service.get_format_instructions_analysis()
        prompt_analysis = self._prompt_service.build_prompt(data, format_analysis)
        raw_analysis = self._ollama_service.call(prompt_analysis)
        score, issues = self._parser_service.parse_analysis(raw_analysis)

        # Deuxième appel : suggestion de traduction basée sur l'analyse
        format_suggestion = self._parser_service.get_format_instructions_suggestion()
        prompt_suggestion = self._prompt_service.build_suggestion_prompt(
            data, format_suggestion, score, issues
        )
        raw_suggestion = self._ollama_service.call(prompt_suggestion)
        suggested_translation = self._parser_service.parse_suggestion(raw_suggestion)

        return AnalysisResult(
            score=score,
            issues=issues,
            suggested_translation=suggested_translation,
        )


# instance partagée du service pour simplifier l'utilisation côté app
translation_service = TranslationAnalysisService(
    prompt_service=PromptService(),
    ollama_service=OllamaService(),
    parser_service=ParserService(),
)

