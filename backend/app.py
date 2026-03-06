import os
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import requests
from flask import Flask, jsonify, request


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")


app = Flask(__name__)


@dataclass
class AnalysisResult:
    score: int
    issues: List[str]
    suggested_translation: str


def build_prompt(original: str, translated: str, brand_tone: str) -> str:
    return f"""
You are an expert in marketing localization.

Your job:
- Compare the original marketing text and its translation.
- Evaluate:
  - translation accuracy
  - brand tone alignment
  - marketing effectiveness

Instructions:
- The brand tone is: "{brand_tone}".
- Be precise and critical, but constructive.
- Always answer in **valid JSON** following exactly this schema:
{{
  "score": <integer 0-100>,
  "issues": [
    "<short issue 1>",
    "<short issue 2>"
  ],
  "suggested_translation": "<one improved translation in target language>"
}}

Here is the content to analyze:

Original text (source language):
\"\"\"{original}\"\"\"

Translated text (target language):
\"\"\"{translated}\"\"\"
"""


def call_ollama(prompt: str) -> str:
    """
    Call the local Ollama server and return the raw text response.
    """
    url = f"{OLLAMA_BASE_URL.rstrip('/')}/api/chat"
    payload: Dict[str, Any] = {
        "model": OLLAMA_MODEL,
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
    Parse the JSON response from the LLM.
    As a safety net, we try to be tolerant: if parsing fails,
    we wrap the raw text into a generic 'issues' message.
    """
    import json

    try:
        parsed = json.loads(raw_text)
        score = int(parsed.get("score", 0))
        issues_field = parsed.get("issues", [])

        if isinstance(issues_field, str):
            issues = [issues_field]
        elif isinstance(issues_field, list):
            issues = [str(item) for item in issues_field]
        else:
            issues = [str(issues_field)]

        suggested = str(parsed.get("suggested_translation", "")).strip()

        return AnalysisResult(
            score=max(0, min(100, score)),
            issues=issues,
            suggested_translation=suggested or "Aucune suggestion fournie par le modèle.",
        )
    except Exception:
        # Mode dégradé : on renvoie le texte brut comme "issue"
        return AnalysisResult(
            score=0,
            issues=[
                "Impossible de parser une réponse structurée depuis le modèle.",
                f"Réponse brute du modèle : {raw_text[:500]}",
            ],
            suggested_translation="",
        )


def validate_payload(payload: Dict[str, Any]) -> Tuple[str, str, str]:
    errors = {}

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

    return original, translated, brand_tone


@app.route("/health", methods=["GET"])
def health() -> Any:
    return jsonify({"status": "ok", "model": OLLAMA_MODEL})


@app.route("/analyze", methods=["POST"])
def analyze() -> Any:
    """
    Corps attendu (JSON) :
    {
      "original_text": "...",
      "translated_text": "...",
      "brand_tone": "Luxury / Elegant"
    }
    """
    try:
        payload = request.get_json(force=True, silent=False) or {}
    except Exception:
        return (
            jsonify({"error": "Payload JSON invalide."}),
            400,
        )

    try:
        original, translated, brand_tone = validate_payload(payload)
    except ValueError as exc:
        return jsonify({"error": "Validation error", "details": exc.args[0]}), 400

    prompt = build_prompt(original, translated, brand_tone)

    try:
        raw = call_ollama(prompt)
        analysis = parse_analysis(raw)
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 502

    return jsonify(
        {
            "score": analysis.score,
            "issues": analysis.issues,
            "suggested_translation": analysis.suggested_translation,
            "raw_model_output_in_debug": False,
        }
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    app.run(host="0.0.0.0", port=port, debug=True)

