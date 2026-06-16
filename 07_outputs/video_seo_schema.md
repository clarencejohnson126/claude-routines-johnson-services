# Video-SEO: VideoObject-Schema für die Startseite

**Stand:** 2026-06-15
**Geprüft am Live-DOM:** Startseite hatte **0 VideoObject-Schema** → Google konnte das Video nicht als Video erfassen.

## Fakten zum Video
- Datei: `https://johnson-services.de/wp-content/uploads/2026/06/jsvideo.mp4`
- Dauer: 8 Sekunden (`PT8S`)
- Auflösung: 1280×720
- Thumbnail (für `thumbnailUrl` + Poster): `https://johnson-services.de/wp-content/uploads/2026/06/jsvideo-thumb.jpg`
- Logo (publisher): `https://johnson-services.de/wp-content/uploads/2023/09/Johnson-Entruempelung-Logo-e1695050258143.png`

## Fertiges Snippet (ersetzt den Inhalt des Video-Code-Blocks)

Enthält jetzt: Video + Poster-Bild (Vorschau vor Play) + VideoObject-Strukturdaten.

```html
<div style="text-align:center;padding:24px 0;">
  <video controls playsinline preload="metadata"
    poster="https://johnson-services.de/wp-content/uploads/2026/06/jsvideo-thumb.jpg"
    style="width:100%;max-width:720px;height:auto;border-radius:14px;box-shadow:0 8px 28px rgba(0,0,0,.15);background:#000;"
    src="https://johnson-services.de/wp-content/uploads/2026/06/jsvideo.mp4#t=0.1"></video>
</div>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "Entrümpelung und Haushaltsauflösung in Mannheim | Johnson Services",
  "description": "Johnson Services übernimmt Entrümpelungen, Haushaltsauflösungen und Umzüge in Mannheim und der Region Rhein-Neckar. Festpreis, besenrein, zuverlässig seit 2011.",
  "thumbnailUrl": "https://johnson-services.de/wp-content/uploads/2026/06/jsvideo-thumb.jpg",
  "uploadDate": "2026-06-14T12:00:00+02:00",
  "duration": "PT8S",
  "contentUrl": "https://johnson-services.de/wp-content/uploads/2026/06/jsvideo.mp4",
  "publisher": {
    "@type": "Organization",
    "name": "Johnson Services",
    "logo": {
      "@type": "ImageObject",
      "url": "https://johnson-services.de/wp-content/uploads/2023/09/Johnson-Entruempelung-Logo-e1695050258143.png"
    }
  }
}
</script>
```

## Ehrliche Einordnung Video-SEO
1. **Selbstgehostetes Video + Schema** (dieser Weg): macht das Video für Google überhaupt erst als Video erfassbar. Effekt: kann als Video-Rich-Result erscheinen, hilft der Seiten-Relevanz. Real, aber moderat.
2. **YouTube-Upload + Embed** (stärkerer Hebel): Google indexiert YouTube-Videos sehr zuverlässig, zweite Suchfläche (YouTube-Suche selbst), Vorschaubild in den Suchergebnissen. Für echtes „Google greift Video auf" ist YouTube der stärkere Weg.

## Nach dem Einfügen
- Schema-Test: https://search.google.com/test/rich-results → URL `https://johnson-services.de/` → muss „VideoObject" erkannt zeigen.
- Re-Indexierung anstoßen (Indexing API / GSC „URL prüfen → Indexierung beantragen").
