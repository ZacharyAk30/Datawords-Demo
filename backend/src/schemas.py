from dataclasses import dataclass, asdict
from typing import List


@dataclass
class AnalysisInput:
    """
    Données reçues en entrée pour l'analyse de traduction.
    """

    original_text: str
    translated_text: str
    brand_tone: str
    source_language: str = ""
    target_language: str = ""

@dataclass
class AnalysisResult:
    """
    Résultat structuré renvoyé par le modèle d'analyse.
    """
    score: int
    issues: List[str]
    suggested_translation: str

    def to_dict(self) -> dict:
        """
        Représentation sérialisable en JSON de l'analyse complète.
        """
        return {
            "score": self.score,
            "issues": self.issues,
            "suggested_translation": self.suggested_translation,
        }

