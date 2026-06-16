# Spec 005 — TikTok / Motion Video Pipeline Agent

## Intent

Eine 10-Wochen-Pipeline für TikTok / Short Videos erstellen, die manuell umgesetzt werden kann. **Keine direkte TikTok-API-Automation.**

## Stil

Kein sprechender Creator · keine Fake-KI-Person · keine billigen AI-Avatare · echte Nahaufnahmen möglich · Nutzer kann als Person vorkommen, aber ohne direkt in die Kamera zu sprechen · Fokus auf Hände, Handschuhe, Arbeitskleidung, Logo, Bewegung, Kraft, Ordnung, Premium-Handwerk.

## Visual Style

Arbeitshose · Handschuhe · Johnson Services Logo · Nahaufnahme · Muskeln/Kraft subtil · Transporter (Mercedes-Benz Sprinter 310) · Kartons · Treppenhaus · Keller · Wohnungstür · Vorher/Nachher · Premium-Service-Gefühl · Produkt-Ad-Ästhetik.

## Pro Woche liefern (für jede der 10 Wochen)

Video-Titel · Hook · Shotlist · Voiceover-Text · Text-Overlays · Caption · Hashtags · benötigte Assets · Prompt für Higgsfield / Veo / Runway · manuelle Umsetzungsschritte.

## Tool-Status (real)

- Higgsfield MCP vorhanden (Nano Banana Pro / Seedance) — siehe Skill `johnson-higgsfield-video-ads-producer`.
- ElevenLabs (`ELEVENLABS_API_KEY` im Graph-`.env`) für deutschen Voiceover (Stimme Charlotte). Hinweis: Seedance halluziniert deutschen VO → VO separat in Post (CapCut/ffmpeg) legen.
- 87 echte Vorher/Nachher-Fotos: `../Johnson-Services/vorher_nachher images/`.

## Output

`07_outputs/video_plans/10_week_tiktok_motion_pipeline.md`

## Beispiel (Spec-Vorlage)

```
Titel: Diskret. Schnell. Sauber.
Hook: Wenn eine Wohnung schnell leer werden muss, zählt nicht Gerede. Es zählt Verlässlichkeit.
Shots:
1. Close-up: schwarze Handschuhe werden angezogen.
2. Close-up: Johnson Services Logo.
3. Close-up: schwere Wohnungstür öffnet sich.
4. Kurzer Shot: Kartons und Werkzeug.
5. Shot: leerer Raum nach Arbeit.
6. Text Overlay: Entrümpelung und Reinigung in Mannheim.
Voiceover: Manchmal muss eine Wohnung schnell leer werden. Johnson Services unterstützt bei Entrümpelung, Haushaltsauflösung und Reinigung in Mannheim und Umgebung.
```
