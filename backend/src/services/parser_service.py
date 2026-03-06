from typing import List, Optional
import json
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from json_repair import repair_json

from ..schemas import AnalysisResult

# Modèle pour le premier appel : score + problèmes uniquement
class _AnalysisOnlyModel(BaseModel):
    """
    Modèle pour la première réponse LLM : score et liste des problèmes.
    """

    score: int = Field(
        description="Overall translation quality score between 0 and 100."
    )

    issues: List[str] = Field(
        description="List of short and clear descriptions of the issues identified in the translation."
    )


# Modèle pour le deuxième appel : suggestion de traduction uniquement
class _SuggestionModel(BaseModel):
    """
    Modèle pour la deuxième réponse LLM : suggestion de traduction.
    """

    suggested_translation: str = Field(
        description="Based on the original text and the translation, and the issues identified, and the brand tone, the target country culture, suggest a translation that is more accurate and more aligned with the brand tone."
    )


class ParserService:
    """
    Service responsible for parsing LLM responses into business objects.
    """
    def __init__(self) -> None:
        self._parser_analysis = PydanticOutputParser(pydantic_object=_AnalysisOnlyModel)
        self._parser_suggestion = PydanticOutputParser(pydantic_object=_SuggestionModel)

    def get_format_instructions_analysis(self) -> str:
        """
        Instructions de format pour le premier appel LLM (score + issues uniquement).
        """
        return self._parser_analysis.get_format_instructions()

    def get_format_instructions_suggestion(self) -> str:
        """
        Instructions de format pour le deuxième appel LLM (suggested_translation uniquement).
        """
        return self._parser_suggestion.get_format_instructions()

    def parse_analysis(self, raw_text: str) -> tuple[int, List[str]]:
        """
        Parse la réponse du premier appel LLM (score + issues).
        Retourne (score, issues).
        """
        json_text = self._extract_json_snippet(raw_text)
        json_text = self._repair_json(json_text)
        try:
            structured: _AnalysisOnlyModel = self._parser_analysis.invoke(json_text)
            return (structured.score, structured.issues)
        except Exception:
            raise RuntimeError("Failed to parse LLM analysis output.")

    def parse_suggestion(self, raw_text: str) -> str:
        """
        Parse la réponse du deuxième appel LLM (suggested_translation).
        """
        json_text = self._extract_json_snippet(raw_text)
        json_text = self._repair_json(json_text)
        try:
            structured: _SuggestionModel = self._parser_suggestion.invoke(json_text)
            return structured.suggested_translation
        except Exception:
            raise RuntimeError("Failed to parse LLM suggestion output.")

    def _extract_json_snippet(self, text: str) -> str:
        """
        Extract the first JSON object using brace matching.
        """

        start = text.find("{")

        if start == -1:
            return text

        stack = 0

        for i in range(start, len(text)):
            if text[i] == "{":
                stack += 1
            elif text[i] == "}":
                stack -= 1

                if stack == 0:
                    return text[start : i + 1]

        return text[start:]

    def _repair_json(self, text: str) -> str:
        """
        Repair malformed JSON produced by LLMs.
        """
        try:
            return repair_json(text)
        except Exception:
            return text