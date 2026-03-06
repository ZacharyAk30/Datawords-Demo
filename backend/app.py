from typing import Any, Dict

from flask import Flask, jsonify, request

from src.config import settings
from src.schemas import AnalysisResult
from src.services import analyze_translation, validate_payload


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
        input_data = validate_payload(payload)
    except ValueError as exc:
        return jsonify({"error": "Validation error", "details": exc.args[0]}), 400

    try:
        analysis: AnalysisResult = analyze_translation(input_data)
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 502

    body = analysis.to_dict()
    body["raw_model_output_in_debug"] = False

    return jsonify(body)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=settings.port,
        debug=settings.debug,
    )

