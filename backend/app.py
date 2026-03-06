from typing import Any, Dict

from flask import Flask, jsonify, request

from src.config import settings
from src.schemas import AnalysisResult
from src.services.analyse_translation_service import translation_service


app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health() -> Any:
    return jsonify({"status": "ok", "model": settings.ollama_model})


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
        return jsonify({"error": "Payload JSON invalide."}), 400

    try:
        input_data = translation_service.validate_payload(payload)
    except ValueError as exc:
        return jsonify({"error": "Validation error", "details": exc.args[0]}), 400

    try:
        analysis: AnalysisResult = translation_service.analyze(input_data)
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 502

    body = analysis.to_dict()

    return jsonify(body)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=settings.port,
        debug=settings.debug,
    )

