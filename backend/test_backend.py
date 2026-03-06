import json
import requests


def main() -> None:
    base_url = "http://localhost:5001"

    # 1) Vérifier que le backend Flask tourne
    try:
        health = requests.get(f"{base_url}/health", timeout=5)
        print(f"/health -> {health.status_code} {health.text}")
    except requests.RequestException as exc:
        print(f"❌ Backend injoignable: {exc}")
        return

    # 2) Appeler /analyze
    url = f"{base_url}/analyze"
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