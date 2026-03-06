from typing import List, Optional
import json

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from ..schemas import AnalysisResult, Issue


class _IssueModel(BaseModel):
    """
    Pydantic model used to parse the LLM output.
    """

    title: str = Field(
        description="Short title describing the issue identified in the translation."
    )
    level: str = Field(
        description='Severity level of the issue. Must be one of: "low", "medium", "high".'
    )
    description: str = Field(
        description="Short and clear description of the issue."
    )


class _AnalysisModel(BaseModel):
    """
    Full Pydantic model representing the expected structured response from the LLM.
    """

    score: int = Field(
        description="Overall translation quality score between 0 and 100."
    )
    issues: List[_IssueModel] = Field(
        description="List of issues identified in the translation."
    )
    suggested_translation: str = Field(
        description="Improved translation proposed by the model. Must be in the Target language"
    )


class ParserService:
    """
    Service responsable du parsing de la réponse du modèle en objets métier.
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
        Parse la réponse structurée du LLM. En cas d'échec, on renvoie un
        résultat dégradé avec les erreurs dans la liste des issues.
        """     
        clean_text = self._extract_json_snippet(raw_text)
        try:
            structured: _AnalysisModel = self._parser.invoke(clean_text)

            issues: List[Issue] = [
                Issue(
                    title=item.title,
                    level=item.level,
                    description=item.description,
                )
                for item in structured.issues
            ]

            return AnalysisResult(
                score=max(0, min(100, structured.score)),
                issues=issues,
                suggested_translation=(
                    structured.suggested_translation.strip()
                    or "No suggestion provided by the model."
                ),
            )
        except Exception:
            # Mode dégradé : tenter d'extraire un résultat partiel depuis le JSON de sortie
            partial = self._try_partial_result(raw_text, clean_text)
            if partial is not None:
                return partial
            # Aucune donnée exploitable : renvoyer le résultat dégradé minimal
            return AnalysisResult(
                score=0,
                issues=[
                    Issue(
                        title="Parsing error",
                        level="high",
                        description="Impossible de parser une réponse structurée depuis le modèle.",
                    ),
                    Issue(
                        title="Raw model output",
                        level="medium",
                        description=f"Réponse brute du modèle : {raw_text[:500]}",
                    ),
                ],
                suggested_translation="",
            )

    def _try_partial_result(self, raw_text: str, clean_text: str) -> Optional[AnalysisResult]:
        """
        Si le parsing Pydantic a échoué, tente de lire le JSON brut et de construire
        un résultat partiel (score, issues, suggested_translation) si des champs sont présents.
        """
        data = None
        for candidate in (clean_text,clean_text.replace('"""', '"')):
            try:
                data = json.loads(candidate)
                if isinstance(data, dict):
                    break
            except (json.JSONDecodeError, TypeError):
                continue
        if not data or not isinstance(data, dict):
            return None

        issues: List[Issue] = []
        for item in data.get("issues") or []:
            if not isinstance(item, dict):
                continue
            title = item.get("title")
            level = item.get("level")
            desc = item.get("description")
            if isinstance(title, str) and isinstance(level, str) and isinstance(desc, str):
                issues.append(Issue(title=title, level=level, description=desc))

        score = data.get("score")
        if not isinstance(score, (int, float)):
            score = 0
        score = max(0, min(100, int(score)))

        suggested = data.get("suggested_translation")
        suggested_translation = (
            suggested.strip() if isinstance(suggested, str) and suggested.strip()
            else ""
        )

        # Aucun champ exploitable → pas de résultat partiel
        if not issues and score == 0 and not suggested_translation:
            return None

        # Ajouter une issue pour signaler la récupération partielle
        issues.insert(
            0,
            Issue(
                title="Partial parse",
                level="medium",
                description="The full structured response could not be parsed; the result was recovered from raw JSON.",
            ),
        )
        return AnalysisResult(
            score=score,
            issues=issues,
            suggested_translation=suggested_translation or "Aucune suggestion fournie par le modèle.",
        )

    def _extract_json_snippet(self, text: str) -> str:
        """
        Essaie d'extraire un objet JSON valide depuis un texte
        qui peut contenir du texte avant/après ou des blocs markdown.
        """
        if "```" in text:
            for part in text.split("```"):
                candidate = part.strip()
                if candidate.startswith("{"):
                    try:
                        json.loads(candidate)
                        return candidate
                    except json.JSONDecodeError:
                        continue

        # 2) Fallback : entre le premier '{' et le dernier '}'
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidate = text[start : end + 1]
            for repaired in (candidate, candidate.replace('"""', '"')):
                try:
                    json.loads(repaired)
                    return repaired
                except json.JSONDecodeError:
                    continue
        return text