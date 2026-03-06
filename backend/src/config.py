import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """
    Configuration globale de l'application, lue depuis les variables
    d'environnement avec des valeurs par défaut raisonnables.
    """

    ollama_base_url: str
    ollama_model: str
    port: int
    debug: bool

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://ollama:11434"),
            ollama_model=os.getenv("OLLAMA_MODEL", "qwen3-coder:30b"),
            port=int(os.getenv("PORT", "5001")),
            debug=os.getenv("FLASK_DEBUG", "false").lower()
            in {"1", "true", "yes", "on"},
        )


settings = Settings.from_env()
