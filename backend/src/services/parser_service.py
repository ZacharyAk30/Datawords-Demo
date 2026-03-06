from typing import List, Optional
import json
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from json_repair import repair_json

from ..schemas import AnalysisResult

class _AnalysisModel(BaseModel):
    """
    Full Pydantic model representing the expected structured response from the LLM.
    """

    score: int = Field(
        description="Overall translation quality score between 0 and 100."
    )

    issues: List[str] = Field(
        description="List of short and clear descriptions of the issues identified in the translation."
    )

    suggested_translation: str = Field(
        description="Base on the original text and the translation, and the issues identified,and the brand tone,the target country culture, suggest a translation that is more accurate and more aligned with the brand tone."
    )


class ParserService:
    """
    Service responsible for parsing LLM responses into business objects.
    """
    def __init__(self) -> None:
        # Parser Pydantic réutilisable pour l'ensemble du service.
        self._parser = PydanticOutputParser(pydantic_object=_AnalysisModel)

    def get_format_instructions(self) -> str:
        """
        Instructions de format à fournir au LLM afin qu'il génère
        une sortie compatible avec le modèle Pydantic.
        """
        return self._parser.get_format_instructions()

    def parse(self, raw_text: str) -> AnalysisResult:
        """
        Parse LLM output into structured data.
        """

        json_text = self._extract_json_snippet(raw_text)
        json_text = self._repair_json(json_text)
        try:
            structured: _AnalysisModel = self._parser.invoke(json_text)
            return AnalysisResult(
                score=structured.score,
                issues=structured.issues,
                suggested_translation=structured.suggested_translation,
            )

        except Exception:
            raise RuntimeError("Failed to parse LLM output.")

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