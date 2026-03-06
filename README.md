# Datawords-Demo
Assignment 

Datawords Group partners with 1,500+ international brands to manage their content across 25 countries and 75+ languages. The company is undergoing a deep strategic transformation driven by AI.

Your mission:
Identify a high-value, AI-native use case that is directly relevant to Datawords' business and strategic positioning, and to Datawords' clients. Design and build a fully functional solution — end-to-end, powered by AI — that any user can test autonomously, without setup or assistance.

Find what makes the difference. Build it. Be ready to pitch it.


# Use Case : AI Translation Quality & Brand Voice Checker

## Concept

Un outil AI qui **analyse automatiquement une traduction marketing** et détecte :

* les erreurs de traduction
* les pertes de sens
* les problèmes de ton de marque
* les incohérences marketing

Puis l’AI :

* donne un **score de qualité**
* explique les problèmes
* propose **une meilleure traduction**
---

### 2️⃣ Très simple à comprendre

Input :
```
Texte original
Traduction
Ton de marque
```
Output :
```
Score de traduction
Problèmes détectés
Traduction améliorée
```
---
### 3️⃣ Très facile à démo
Tu colles un texte → résultat immédiat.
C’est parfait pour un assignment.
---
# Exemple concret
## Input
Original (English)
```
Unleash your wild side with our new luxury fragrance.
```
French translation
```
Libérez votre côté sauvage avec notre nouveau parfum de luxe.
```
Brand tone
```
Luxury / Elegant
```
---
## Output AI
```
Translation Score: 68 / 100
```
### Issues detected
1. Brand tone mismatch
The expression "côté sauvage" feels too aggressive for a luxury fragrance brand.
2. Cultural nuance
Luxury fragrance marketing in France typically uses more refined language.
---
### Suggested rewrite
```
Révélez votre élégance naturelle avec notre nouveau parfum de luxe.
```
---
# Architecture simple
```
User
 ↓
Angular interface
 ↓
Flask backend
 ↓
LLM
```
---
## Backend
Python + Flask.
Endpoint :
```
POST /analyze
```
Input
```
original_text
translated_text
brand_tone
```
Output
```
score
issues
suggested_translation
```
---
## LLM Prompt
```
You are an expert in marketing localization.
Compare the original marketing text and its translation.
Evaluate:
- translation accuracy
- brand tone alignment
- marketing effectiveness
Return:
1. Translation score (0-100)
2. Issues detected
3. Suggested improved translation
```