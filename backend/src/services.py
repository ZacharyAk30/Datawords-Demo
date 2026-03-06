from __future__ import annotations

import json
from typing import Any, Dict, List

import requests

from .config import settings
from .schemas import AnalysisInput, AnalysisResult, Issue


def build_prompt(data: AnalysisInput) -> str:
    return f"""
You are an expert in marketing localization.

Your job:
- Compare the original marketing text and its translation.
- Evaluate:
  - translation accuracy
  - brand tone alignment
  - marketing effectiveness

Instructions:
- The brand tone is: "{data.brand_tone}".
- Be precise and critical, but constructive.
- Always answer in **valid JSON** following exactly this schema:
{{
  "score": <integer 0-100>,
  "issues": [
    {{
      "title": "<short issue title>",
      "level": "<low|medium|high>",
      "description": "<short explanation of the issue>"
    }}
  ],
  "suggested_translation": "<one improved translation in target language>"
}}

Here is the content to analyze:

Original text (source language):
\"\"\"{data.original_text}\"\"\"

Translated text (target language):
\"\"\"{data.translated_text}\"\"\"
"""


def call_ollama(prompt: str) -> str:
    """
    Appelle le serveur Ollama local et renvoie la réponse texte brute.
    """
    url = f"{settings.ollama_base_url.rstrip('/')}/api/chat"
    payload: Dict[str, Any] = {
        "model": settings.ollama_model,
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    try:
        response = requests.post(url, json=payload, timeout=120)
    except requests.RequestException as exc:
        raise RuntimeError(f"Erreur de connexion à Ollama: {exc}") from exc

    if response.status_code != 200:
        raise RuntimeError(
            f"Réponse invalide d'Ollama (status={response.status_code}): "
            f"{response.text[:500]}"
        )

    data = response.json()
    # Format typique: {"message": {"role": "...", "content": "..."}, ...}
    try:
        content = data["message"]["content"]
    except (KeyError, TypeError) as exc:
        raise RuntimeError(
            f"Payload inattendu depuis Ollama: {data}"
        ) from exc

    return content


def parse_analysis(raw_text: str) -> AnalysisResult:
    """
    Parse la réponse JSON du LLM. En cas d'échec, on renvoie un résultat
    dégradé avec les erreurs dans la liste des issues.
    """
    try:
        parsed = json.loads(raw_text)
        score = int(parsed.get("score", 0))
        issues_field = parsed.get("issues", [])

        issues: List[Issue] = []

        # On accepte plusieurs formats pour être tolérant :
        # - chaîne de caractères
        # - dict unique
        # - liste de chaînes
        # - liste de dicts
        if isinstance(issues_field, str):
            issues = [
                Issue(
                    title="Issue",
                    level="medium",
                    description=issues_field,
                )
            ]
        elif isinstance(issues_field, dict):
            issues = [
                Issue(
                    title=str(issues_field.get("title", "Issue")),
                    level=str(issues_field.get("level", "medium")),
                    description=str(
                        issues_field.get("description", issues_field)
                    ),
                )
            ]
        elif isinstance(issues_field, list):
            for item in issues_field:
                if isinstance(item, dict):
                    issues.append(
                        Issue(
                            title=str(item.get("title", "Issue")),
                            level=str(item.get("level", "medium")),
                            description=str(
                                item.get("description", item)
                            ),
                        )
                    )
                else:
                    issues.append(
                        Issue(
                            title="Issue",
                            level="medium",
                            description=str(item),
                        )
                    )
        else:
            issues = [
                Issue(
                    title="Issue",
                    level="medium",
                    description=str(issues_field),
                )
            ]

        suggested = str(parsed.get("suggested_translation", "")).strip()

        return AnalysisResult(
            score=max(0, min(100, score)),
            issues=issues,
            suggested_translation=suggested
            or "Aucune suggestion fournie par le modèle.",
        )
    except Exception:
        # Mode dégradé : on renvoie le texte brut comme une issue critique
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


def validate_payload(payload: Dict[str, Any]) -> AnalysisInput:
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


def analyze_translation(data: AnalysisInput) -> AnalysisResult:
    """
    Orchestration complète de l'appel au modèle pour analyser une traduction.
    """
    prompt = build_prompt(data)
    raw = call_ollama(prompt)
    return parse_analysis(raw)

