## Backend - AI Translation Quality & Brand Voice Checker

Backend Flask qui expose un endpoint `/analyze` et délègue l'analyse à un LLM local (Ollama) pour produire une évaluation détaillée de la qualité de traduction et de l'alignement avec le ton de marque.

### 1. Fonctionnalités

- **Endpoint santé**: `GET /health`
  - Vérifie que l'API est en ligne.
  - Retourne le nom du modèle configuré.
- **Endpoint analyse**: `POST /analyze`
  - **Input (JSON)** :
    ```json
    {
      "original_text": "Texte source à analyser",
      "translated_text": "Traduction à évaluer",
      "brand_tone": "Description du ton de marque (ex: \"Luxury / Elegant\")"
    }
    ```
  - **Output (JSON)** :
    ```json
    {
      "score": 78,
      "issues": [
        "Exemple de problème de ton",
        "Exemple de problème de nuance culturelle"
      ],
      "suggested_translation": "Traduction améliorée proposée par l'IA"
    }
    ```

### 2. Architecture logique

1. Le frontend envoie une requête `POST /analyze` au backend.
2. Le backend construit un **prompt expert marketing / localisation**.
3. Le backend appelle le serveur Ollama local via `POST /api/chat`.
4. Le LLM répond en **JSON structuré** (score, issues, suggested_translation).
5. Le backend parse la réponse et renvoie un JSON normalisé au frontend.

### 3. Prérequis

- **Python**: 3.10 ou supérieur recommandé.
- **Ollama** installé en local et en cours d'exécution.
  - Site officiel : `https://ollama.com`
  - Le serveur est supposé être accessible sur `http://localhost:11434`.
- Un modèle compatible chat installé dans Ollama, par exemple :
  - `llama3`, `llama3.1`, `mistral`, etc.

### 4. Installation

1. Cloner le repo (si ce n’est pas déjà fait) :

```bash
git clone <votre_repo> Datawords-Demo
cd Datawords-Demo/backend
```

2. Créer et activer un environnement virtuel (fortement recommandé) :

```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows PowerShell
# ou
source .venv/bin/activate  # macOS / Linux
```

3. Installer les dépendances Python :

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. Installer et démarrer Ollama (si ce n’est pas déjà fait) :

- Suivre les instructions officielles sur `https://ollama.com`.
- Télécharger un modèle, par exemple :

```bash
ollama pull llama3
```

### 5. Configuration

Les variables d’environnement suivantes sont supportées (facultatives) :

- **`OLLAMA_BASE_URL`** (par défaut: `http://localhost:11434`)
  - URL du serveur Ollama.
- **`OLLAMA_MODEL`** (par défaut: `llama3`)
  - Nom du modèle à utiliser.
- **`PORT`** (par défaut: `5001`)
  - Port HTTP sur lequel le backend Flask écoute.

Exemple (PowerShell) :

```powershell
$env:OLLAMA_MODEL = "llama3"
$env:PORT = "5001"
python app.py
```

### 6. Démarrer le serveur backend

Depuis le dossier `backend` avec l’environnement virtuel activé :

```bash
python app.py
```

Le serveur démarre par défaut sur `http://0.0.0.0:5001`.

### 7. Exemples d’appel API

- **Vérifier la santé :**

```bash
curl http://localhost:5001/health
```

- **Analyser une traduction :**

```bash
curl -X POST http://localhost:5001/analyze ^
  -H "Content-Type: application/json" ^
  -d "{
    \"original_text\": \"Unleash your wild side with our new luxury fragrance.\",
    \"translated_text\": \"Libérez votre côté sauvage avec notre nouveau parfum de luxe.\",
    \"brand_tone\": \"Luxury / Elegant\"
  }"
```

Réponse typique :

```json
{
  "score": 68,
  "issues": [
    "Le terme \"côté sauvage\" est un peu agressif pour un parfum de luxe.",
    "Le ton pourrait être plus raffiné pour le marché français."
  ],
  "suggested_translation": "Révélez votre élégance naturelle avec notre nouveau parfum de luxe."
}
```

### 8. Intégration avec le frontend

Depuis le frontend (Angular, React, Vite, etc.), il suffit d’appeler :

```text
POST http://localhost:5001/analyze
```

avec le corps JSON décrit plus haut.  
Le backend renvoie un objet simple à afficher :

- **score**: nombre de 0 à 100
- **issues**: liste de chaînes
- **suggested_translation**: texte

