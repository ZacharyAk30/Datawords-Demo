from ..schemas import AnalysisInput


class PromptService:
    """
    Service responsable de la génération des prompts pour le modèle.
    """

    def build_prompt(self, data: AnalysisInput, format_instructions: str) -> str:
        """
        Construit le prompt envoyé au modèle pour analyser la traduction.
        Les `format_instructions` proviennent du parser Pydantic afin de
        garantir un format de sortie compatible avec le modèle.
        """
        source_lang = f" (source language: {data.source_language})" if data.source_language else ""
        target_lang = f" (target language: {data.target_language})" if data.target_language else ""
        return f"""
        You are an expert in marketing localization.

        Your job:
        - Compare the original marketing text and its translation.
        - Evaluate:
          - translation accuracy
          - brand tone alignment
          - marketing effectiveness
          - cultural appropriateness

        CRITICAL OUTPUT RULES:
        - You MUST answer using ONLY a single valid JSON object.
        - DO NOT add any explanation before or after the JSON.
        - DO NOT use Markdown, DO NOT use ``` or code fences.
        - DO NOT add comments.
        - The response MUST be directly parseable as JSON.
        - The JSON MUST follow EXACTLY these format instructions:
        {format_instructions}

        Here is the content to analyze:

        The brand tone is: "{data.brand_tone}".
        {f"Source language: {data.source_language}." if data.source_language else ""}
        {f"Target language: {data.target_language}." if data.target_language else ""}

        Original text{source_lang}:
        \"\"\"{data.original_text}\"\"\"

        Translated text{target_lang}:
        \"\"\"{data.translated_text}\"\"\"
        """

