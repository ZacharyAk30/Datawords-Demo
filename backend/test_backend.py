import json

import requests


def main() -> None:
    url = "http://localhost:5001/analyze"

    payload = {
        "original_text": "Unleash your wild side with our new luxury fragrance.",
        "translated_text": "Libérez votre côté sauvage avec notre nouveau parfum de luxe.",
        "brand_tone": "Luxury / Elegant",
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
    except requests.RequestException as exc:
        print(f"❌ Erreur de connexion au backend: {exc}")
        return

    print(f"Status code: {response.status_code}")

    try:
        data = response.json()
    except json.JSONDecodeError:
        print("Réponse non JSON :")
        print(response.text)
        return

    print("Réponse JSON formatée :")
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

