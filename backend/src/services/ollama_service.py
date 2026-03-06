from typing import Any, Mapping

import ollama

from ..config import settings


class OllamaService:
    """
    Service responsable des appels au serveur Ollama via la librairie Python.
    """

    def call(self, prompt: str) -> str:
        """
        Appelle le modèle Ollama et renvoie la réponse texte brute.
        """
        try:
            client = ollama.Client(host=settings.ollama_base_url)
            raw_response = client.chat(
                model=settings.ollama_model,
                messages=[{"role": "user", "content": prompt}],
                format="json",
            )
        except Exception as exc:
            raise RuntimeError(f"Erreur de connexion à Ollama: {exc}") from exc

        try:
            if isinstance(raw_response, Mapping):
                message = raw_response.get("message") or {}
                content = message.get("content")
            else:
                # Selon la version du client, raw_response peut être un objet avec .message.content
                content = raw_response.message.content  # type: ignore[assignment]
        except Exception as exc:
            raise RuntimeError(
                f"Réponse inattendue d'Ollama: {raw_response!r}"
            ) from exc

        if not isinstance(content, str):
            raise RuntimeError(
                f"Contenu de réponse invalide d'Ollama: {raw_response!r}"
            )

        return content
