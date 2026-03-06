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
        Lève ValueError avec un dictionnaire d'erreurs si nécessaire.
        """
        errors: Dict[str, str] = {}

        original = (payload.get("original_text") or "").strip()
        translated = (payload.get("translated_text") or "").strip()
        brand_tone = (payload.get("brand_tone") or "").strip()

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
        )

    def analyze(self, data: AnalysisInput) -> AnalysisResult:
        """
        Orchestration complète de l'appel au modèle pour analyser une traduction.
        """
        format_instructions = self._parser_service.get_format_instructions()
        prompt = self._prompt_service.build_prompt(data, format_instructions)
        raw = self._ollama_service.call(prompt)
        return self._parser_service.parse(raw)


# instance partagée du service pour simplifier l'utilisation côté app
translation_service = TranslationAnalysisService(
    prompt_service=PromptService(),
    ollama_service=OllamaService(),
    parser_service=ParserService(),
)

